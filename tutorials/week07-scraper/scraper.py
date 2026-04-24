import os
import json
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync


def close_popup(page, selector, label="popup"):
    try:
        btn = page.locator(selector)
        if btn.count() > 0:
            btn.first.click(timeout=3000)
            print(f"  ✓ Closed {label}")
            return True
    except Exception:
        pass
    return False


def scrape_sephora_product(url, target_review_count=20):
    sku_id = url.split("skuId=")[-1].split("&")[0] if "skuId=" in url else ""

    user_data_dir = os.path.join(os.getcwd(), "playwright_profile")
    if not os.path.exists(user_data_dir):
        os.makedirs(user_data_dir)

    with sync_playwright() as p:
        try:
            # launch_persistent_context는 browser와 context를 한 번에 생성합니다.
            context = p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                headless=False, 
                channel="chrome",
                args=["--disable-blink-features=AutomationControlled"],
                ignore_default_args=["--enable-automation"],
                viewport={"width": 1280, "height": 800},
            )
        except Exception:
            context = p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                headless=False,
                args=["--disable-blink-features=AutomationControlled"],
                ignore_default_args=["--enable-automation"],
                viewport={"width": 1280, "height": 800},
            )

        page = context.new_page()
        stealth_sync(page)

        # ── Step 0: Warm up (Homepage visit for cookies) ──────────────────
        print("Warm up: Visiting homepage for session cookies...")
        try:
            page.goto("https://www.sephora.com", wait_until="domcontentloaded", timeout=60000)
            time.sleep(3)
            page.evaluate("window.scrollTo(0, 300)")
            time.sleep(1)
        except Exception as e:
            print(f"  Warm up error (ignored): {e}")

        # ── Step 0.1: Navigate to target product ─────────────────────────
        print(f"Navigating to product page: {url}")
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            time.sleep(4)
        except Exception as e:
            print(f"  Navigation error: {e}")

        # ── Step 1: Dismiss popups (Explicit Wait) ───────────────────────
        print("Handling popups...")
        def wait_and_close(p, selector, label):
            try:
                p.wait_for_selector(selector, state="visible", timeout=5000)
                p.locator(selector).first.click()
                print(f"  ✓ Closed {label}")
                time.sleep(1)
            except:
                pass

        wait_and_close(page, '[data-at="modal_close"]', "location popup")
        wait_and_close(page, '[data-at="close_button"]', "sign-in popup")

        # ── Step 2: Product info from DOM ─────────────────────────────────
        print("Extracting product info from DOM...")
        product_info = page.evaluate("""() => {
            // Price: first <b> tag containing a $ sign
            const bTags = Array.from(document.querySelectorAll('b'));
            const priceEl = bTags.find(b => b.innerText && b.innerText.trim().startsWith('$'));
            const price = priceEl ? priceEl.innerText.trim() : '';

            // Size: span whose text starts with 'Size:'
            const spans = Array.from(document.querySelectorAll('span'));
            const sizeEl = spans.find(s => s.innerText && s.innerText.trim().startsWith('Size:'));
            const size = sizeEl ? sizeEl.innerText.replace('Size:', '').trim() : '';

            // Brand / Product name
            const brand        = document.querySelector('[data-at="brand_name"]')?.innerText.trim() || '';
            const product_name = document.querySelector('[data-at="product_name"]')?.innerText.trim() || '';

            // Rating: parse width% from star fill element → 5 * (width/100)
            let rating = null;
            const starEl = document.querySelector('[data-at="star_rating_style"]');
            if (starEl) {
                const style = starEl.getAttribute('style') || '';
                const m = style.match(/width:\\s*([\\d.]+)%/);
                if (m) rating = (parseFloat(m[1]) / 100 * 5).toFixed(2);
            }

            // Total review count
            const revCountEl = document.querySelector('[data-at="number_of_reviews"]');
            const review_count = revCountEl ? revCountEl.innerText.trim().replace(/[^0-9]/g, '') : '';

            return { brand, product_name, price, size, rating, review_count };
        }""")

        brand        = product_info.get("brand", "") or "N/A"
        product_name = product_info.get("product_name", "") or "N/A"
        price        = product_info.get("price", "") or "N/A"
        size         = product_info.get("size", "") or "N/A"
        rating       = product_info.get("rating")       # string like "4.90"
        review_count = product_info.get("review_count") # string like "126"

        # Clean URL: keep only product path + skuId
        from urllib.parse import urlparse, parse_qs
        parsed     = urlparse(url)
        sku_param  = parse_qs(parsed.query).get("skuId", [""])[0]
        clean_url  = f"https://www.sephora.com{parsed.path}?skuId={sku_param}" if sku_param else f"https://www.sephora.com{parsed.path}"

        # Ingredients: source JSON fallback (page source, anchored to skuId)
        ingredients = ""
        try:
            import re
            html = page.content()
            anchor_pos = html.find(f'"displayName":"{sku_id}')
            if anchor_pos == -1:
                anchor_pos = html.find(f'"skuId":"{sku_id}"')
            window = html[max(0, anchor_pos - 200): anchor_pos + 8000] if anchor_pos != -1 else html
            m = re.search(r'"ingredientDesc"\s*:\s*"((?:[^"\\]|\\.)*)"', window)
            if m:
                ingredients = (m.group(1)
                               .replace("<br>", "\n")
                               .replace("\\u003cbr\\u003e", "\n")
                               .strip())
        except Exception:
            pass

        print(f"  brand={brand}, price={price}, size={size}, rating={rating}, reviews={review_count}")



        # ── Step 3: Image gallery carousel (page still at top) ────────────
        print("Opening image gallery carousel...")
        images = []
        try:
            see_all = page.locator('[data-at="see_all_images_btn"]')
            if see_all.count() > 0:
                loop_count = 8
                try:
                    count_text = see_all.locator("span").first.text_content(timeout=1500)
                    loop_count = int("".join(filter(str.isdigit, count_text)))
                except Exception:
                    pass
                print(f"  Gallery total: {loop_count}")

                see_all.click()
                time.sleep(2)

                seen = set()
                # Loop EXACTLY loop_count times — don't stop early on video frames
                for step in range(loop_count + 1):
                    # IMPORTANT: scope query to the gallery modal dialog only
                    # to avoid picking up images from 'You May Also Like' sections
                    srcs = page.evaluate("""() => {
                        const modal = document.querySelector('[role="dialog"]') ||
                                      document.querySelector('[aria-modal="true"]');
                        const scope = modal || document;
                        const imgs = scope.querySelectorAll('div[data-comp*="ProductImage"] picture source');
                        const res = [];
                        for (const s of imgs) {
                            const srcset = s.getAttribute('srcset') || '';
                            for (const p of srcset.split(',')) {
                                if (p.includes('2x')) res.push(p.trim().split(' ')[0]);
                            }
                        }
                        return res;
                    }""")

                    for src in srcs:
                        if src and src not in seen:
                            seen.add(src)
                            if src.startswith("/"): src = "https://www.sephora.com" + src
                            images.append(src)
                    # NOTE: no early break on "no new image" — video slides return empty, 
                    # but we must keep clicking Next to get to the next photo slide

                    next_btn = page.locator('button[data-at="carousel_next_btn"]')
                    if next_btn.count() > 0:
                        try:
                            next_btn.click(timeout=1500)
                            time.sleep(0.7)
                        except Exception:
                            break
                    else:
                        break

                images = list(dict.fromkeys(images))
                print(f"  Collected {len(images)} images")
                try:
                    page.keyboard.press("Escape")
                    time.sleep(0.5)
                except Exception:
                    pass
            else:
                print("  See All button not found.")
        except Exception as e:
            print(f"  Carousel error: {e}")

        # ── Step 4: Reviews ───────────────────────────────────────────────
        print("Extracting reviews...")
        # Scroll directly to the reviews section if possible
        page.evaluate("""() => {
            const reviewSection = document.querySelector('div[data-comp*="Review Review BaseComponent"]')
                                || document.querySelector('[data-at="review_container"]');
            if (reviewSection) {
                reviewSection.scrollIntoView({ behavior: 'instant', block: 'center' });
            } else {
                window.scrollTo(0, document.body.scrollHeight * 0.65);
            }
        }""")
        time.sleep(2.5)  # extra time for React lazy-load

        reviews = []
        while len(reviews) < target_review_count:
            page.evaluate("""() => {
                document.querySelectorAll('button').forEach(b => {
                    if (b.innerText && b.innerText.includes('Read more')) b.click();
                });
            }""")
            time.sleep(0.4)

            extracted = page.evaluate("""() => {
                // Boundary: only collect reviews before the Pagination nav
                const pagination = document.querySelector('ul[data-comp*="Pagination Pagination BaseComponent"]');
                const allCards = Array.from(document.querySelectorAll('div[data-comp*="Review Review BaseComponent"]'));

                let cards = allCards;
                if (pagination && allCards.length > 0) {
                    cards = allCards.filter(card =>
                        (pagination.compareDocumentPosition(card) & Node.DOCUMENT_POSITION_PRECEDING) !== 0
                    );
                    // Fallback: if filter wiped everything out, use all cards
                    if (cards.length === 0) cards = allCards;
                }

                return cards.map(c => {
                    const rEl = c.querySelector('[data-at="star_rating_style"]');
                    const rating = rEl ? rEl.getAttribute('style') : '';

                    const uEl = c.querySelector('[data-at="review_username"]');
                    const username = uEl ? uEl.innerText.trim() : '';

                    const dEl = c.querySelector('[data-at="review_date"]');
                    const date = dEl ? dEl.innerText.trim() : '';

                    // Title from h3
                    const h3 = c.querySelector('h3');
                    const title = h3 ? h3.innerText.trim() : '';

                    // Body: sibling div after h3, or largest text block in card
                    let body = '';
                    if (h3 && h3.nextElementSibling) {
                        body = h3.nextElementSibling.innerText.trim();
                    }
                    if (!body) {
                        // Walk all text nodes — pick longest that isn't metadata
                        const walker = document.createTreeWalker(c, NodeFilter.SHOW_TEXT);
                        let node;
                        while ((node = walker.nextNode())) {
                            const t = node.textContent.trim();
                            if (t.length > body.length && t !== title && t !== username && t !== date && t.length > 20) {
                                body = t;
                            }
                        }
                    }

                    return { rating, username, date, title, body };
                });
            }""")

            found_new = False
            for r in extracted:
                if (r["username"] or r["body"]) and r not in reviews:
                    reviews.append(r)
                    found_new = True

            if len(reviews) >= target_review_count:
                break
            if not found_new:
                print("  No new reviews, stopping.")
                break

            next_clicked = page.evaluate("""() => {
                const n = document.querySelector('button[aria-label="Next page"]');
                if (n && !n.disabled) { n.click(); return true; }
                return false;
            }""")
            if not next_clicked:
                print("  No more review pages.")
                break
            time.sleep(1.5)

        context.close()

        result = {
            "url":               clean_url,
            "scraped_at":        datetime.now().isoformat(),
            "brand":             brand,
            "product_name":      product_name,
            "price":             price,
            "size":              size,
            "rating":            rating,
            "review_count_total": review_count,
            "sku":               sku_id,
            "images":            images,
            "ingredients":       ingredients,
            "reviews":           reviews[:target_review_count],
        }

        safe_name = "".join(c for c in product_name if c.isalnum() or c == " ").strip() or "sephora_product"
        safe_name = safe_name.replace(" ", "_")
        date_str  = datetime.now().strftime("%Y%m%d")
        base_name = f"saved_scrapes/{safe_name}_{date_str}"

        os.makedirs("saved_scrapes", exist_ok=True)

        # ── JSON (full data) ──────────────────────────────────────────────
        json_file = f"{base_name}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        # ── Plain text reviews (for LLM analysis) ────────────────────────
        txt_file = f"{base_name}_reviews.txt"
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write(f"{brand} - {product_name}\n")
            f.write(f"URL: {clean_url}\n")
            f.write(f"Rating: {rating}  Reviews: {review_count}\n")
            f.write("=" * 60 + "\n\n")
            for i, r in enumerate(reviews[:target_review_count], 1):
                if r.get("title"):
                    f.write(f"[{i}] {r['title']}\n")
                else:
                    f.write(f"[{i}]\n")
                if r.get("body"):
                    f.write(f"{r['body']}\n")
                f.write("\n")

        result["_filename"]     = json_file
        result["_reviews_file"] = txt_file
        print(f"Saved JSON    → {json_file}")
        print(f"Saved reviews → {txt_file}")
        return result



if __name__ == "__main__":
    test_url = "https://www.sephora.com/product/stem-clinical-recovery-serum-P521628?skuId=2966935"
    data = scrape_sephora_product(test_url, 5)
    print(json.dumps(data, indent=2, ensure_ascii=False))
