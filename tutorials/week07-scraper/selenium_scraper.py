import os
import json
import time
import re
from datetime import datetime
from urllib.parse import urlparse, parse_qs

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import subprocess

def get_chrome_main_version():
    """Dynamically detect the installed Chrome version on Windows."""
    try:
        cmd = r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
        output = subprocess.check_output(cmd, shell=True).decode()
        version = re.search(r'(\d+)\.', output).group(1)
        return int(version)
    except Exception:
        try:
            # Fallback for some systems
            cmd = r'reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome" /v version'
            output = subprocess.check_output(cmd, shell=True).decode()
            version = re.search(r'(\d+)\.', output).group(1)
            return int(version)
        except:
            return None

def close_popup(driver, selector, label="popup", timeout=5):
    """Wait for and close a popup if it appears."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
        )
        element.click()
        print(f"  ✓ Closed {label}")
        return True
    except TimeoutException:
        return False
    except Exception as e:
        print(f"  Error closing {label}: {e}")
        return False

def scrape_sephora_product(url, target_review_count=20):
    sku_id = url.split("skuId=")[-1].split("&")[0] if "skuId=" in url else ""
    
    print(f"Starting Selenium (undetected-chromedriver) for: {url}")
    
    options = uc.ChromeOptions()
    # options.add_argument("--headless") # 필요시 주석 해제
    options.add_argument("--window-size=1280,800")
    
    # Initialize driver with detected version
    main_version = get_chrome_main_version()
    print(f"  Detected Chrome version: {main_version}")
    
    try:
        driver = uc.Chrome(options=options, version_main=main_version)
    except Exception as e:
        print(f"  Error starting UC with version {main_version}: {e}. Trying default...")
        driver = uc.Chrome(options=options)
    
    try:
        # Step 0: Initial navigation to homepage to get cookies/session
        print("Navigating to homepage first for session...")
        driver.get("https://www.sephora.com")
        
        # Wait a bit for page to load and cookies to settle
        time.sleep(4)
        
        # Optional: Scroll a bit to look human
        driver.execute_script("window.scrollTo(0, 200);")
        time.sleep(1)

        # Step 0.1: Now navigate to actual product page
        print(f"Navigating to product page: {url}")
        driver.get(url)
        
        # Wait longer for product page to fully load and avoid instant detection
        time.sleep(5)
        
        # Step 1: Handle popups
        print("Handling popups...")
        # Location popup
        close_popup(driver, '[data-at="modal_close"]', "location popup", timeout=5)
        time.sleep(1)
        # Sign-in popup
        close_popup(driver, '[data-at="close_button"]', "sign-in popup", timeout=5)
        
        # Step 2: Extract product info via JavaScript (same logic as Playwright)
        print("Extracting product info...")
        product_info = driver.execute_script("""
            const bTags = Array.from(document.querySelectorAll('b'));
            const priceEl = bTags.find(b => b.innerText && b.innerText.trim().startsWith('$'));
            const price = priceEl ? priceEl.innerText.trim() : '';

            const spans = Array.from(document.querySelectorAll('span'));
            const sizeEl = spans.find(s => s.innerText && s.innerText.trim().startsWith('Size:'));
            const size = sizeEl ? sizeEl.innerText.replace('Size:', '').trim() : '';

            const brand        = document.querySelector('[data-at="brand_name"]')?.innerText.trim() || '';
            const product_name = document.querySelector('[data-at="product_name"]')?.innerText.trim() || '';

            let rating = null;
            const starEl = document.querySelector('[data-at="star_rating_style"]');
            if (starEl) {
                const style = starEl.getAttribute('style') || '';
                const m = style.match(/width:\\s*([\\d.]+)%/);
                if (m) rating = (parseFloat(m[1]) / 100 * 5).toFixed(2);
            }

            const revCountEl = document.querySelector('[data-at="number_of_reviews"]');
            const review_count = revCountEl ? revCountEl.innerText.trim().replace(/[^0-9]/g, '') : '';

            return { brand, product_name, price, size, rating, review_count };
        """)
        
        brand        = product_info.get("brand", "") or "N/A"
        product_name = product_info.get("product_name", "") or "N/A"
        price        = product_info.get("price", "") or "N/A"
        size         = product_info.get("size", "") or "N/A"
        rating       = product_info.get("rating")
        review_count_total = product_info.get("review_count")
        
        # Clean URL
        parsed = urlparse(url)
        sku_param = parse_qs(parsed.query).get("skuId", [""])[0]
        clean_url = f"https://www.sephora.com{parsed.path}?skuId={sku_param}" if sku_param else f"https://www.sephora.com{parsed.path}"
        
        # Ingredients (Regex from source)
        ingredients = ""
        try:
            page_source = driver.page_source
            anchor_pos = page_source.find(f'"displayName":"{sku_id}')
            if anchor_pos == -1:
                anchor_pos = page_source.find(f'"skuId":"{sku_id}"')
            window = page_source[max(0, anchor_pos - 200): anchor_pos + 8000] if anchor_pos != -1 else page_source
            m = re.search(r'"ingredientDesc"\s*:\s*"((?:[^"\\]|\\.)*)"', window)
            if m:
                ingredients = (m.group(1)
                               .replace("<br>", "\n")
                               .replace("\\u003cbr\\u003e", "\n")
                               .strip())
        except Exception:
            pass

        # Step 3: Images (Carousel)
        print("Collecting images...")
        images = []
        try:
            see_all_btns = driver.find_elements(By.CSS_SELECTOR, '[data-at="see_all_images_btn"]')
            if see_all_btns:
                see_all_btns[0].click()
                time.sleep(2)
                
                seen = set()
                # Simplified image collection for Selenium
                for _ in range(15): # Max 15 images
                    srcs = driver.execute_script("""
                        const modal = document.querySelector('[role="dialog"]') || document.querySelector('[aria-modal="true"]');
                        const scope = modal || document;
                        const sources = scope.querySelectorAll('div[data-comp*="ProductImage"] picture source');
                        return Array.from(sources).map(s => s.getAttribute('srcset')).filter(Boolean);
                    """)
                    
                    for srcset in srcs:
                        for p in srcset.split(','):
                            if '2x' in p:
                                src = p.trim().split(' ')[0]
                                if src.startswith("/"): src = "https://www.sephora.com" + src
                                if src not in seen:
                                    seen.add(src)
                                    images.append(src)
                    
                    # Next button
                    try:
                        next_btn = driver.find_element(By.CSS_SELECTOR, 'button[data-at="carousel_next_btn"]')
                        if next_btn.is_enabled():
                            next_btn.click()
                            time.sleep(0.5)
                        else:
                            break
                    except:
                        break
                
                # Close modal
                driver.execute_script("document.body.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape'}));")
                time.sleep(0.5)
        except Exception as e:
            print(f"  Image collection error: {e}")

        # Step 4: Reviews
        print("Extracting reviews...")
        reviews = []
        # Scroll to reviews
        driver.execute_script("""
            const section = document.querySelector('[data-at="review_container"]');
            if (section) section.scrollIntoView({behavior: 'instant', block: 'center'});
        """)
        time.sleep(2)
        
        while len(reviews) < target_review_count:
            # Click "Read more" buttons
            driver.execute_script("""
                document.querySelectorAll('button').forEach(b => {
                    if (b.innerText && b.innerText.includes('Read more')) b.click();
                });
            """)
            time.sleep(0.5)
            
            extracted = driver.execute_script("""
                const cards = Array.from(document.querySelectorAll('div[data-comp*="Review Review BaseComponent"]'));
                return cards.map(c => {
                    const rating = c.querySelector('[data-at="star_rating_style"]')?.getAttribute('style') || '';
                    const username = c.querySelector('[data-at="review_username"]')?.innerText.trim() || '';
                    const date = c.querySelector('[data-at="review_date"]')?.innerText.trim() || '';
                    const title = c.querySelector('h3')?.innerText.trim() || '';
                    let body = '';
                    const h3 = c.querySelector('h3');
                    if (h3 && h3.nextElementSibling) body = h3.nextElementSibling.innerText.trim();
                    return { rating, username, date, title, body };
                });
            """)
            
            new_found = False
            for r in extracted:
                if r not in reviews:
                    reviews.append(r)
                    new_found = True
            
            if len(reviews) >= target_review_count or not new_found:
                break
                
            # Next page
            try:
                next_page = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Next page"]')
                if next_page.is_enabled():
                    next_page.click()
                    time.sleep(1.5)
                else:
                    break
            except:
                break

        # Result construction
        result = {
            "url": clean_url,
            "scraped_at": datetime.now().isoformat(),
            "brand": brand,
            "product_name": product_name,
            "price": price,
            "size": size,
            "rating": rating,
            "review_count_total": review_count_total,
            "sku": sku_id,
            "images": images,
            "ingredients": ingredients,
            "reviews": reviews[:target_review_count],
        }
        
        # Save files
        safe_name = "".join(c for c in product_name if c.isalnum() or c == " ").strip().replace(" ", "_") or "sephora_product"
        date_str = datetime.now().strftime("%Y%m%d")
        base_name = f"saved_scrapes/{safe_name}_{date_str}"
        os.makedirs("saved_scrapes", exist_ok=True)
        
        json_file = f"{base_name}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
            
        result["_filename"] = json_file
        print(f"Data saved to {json_file}")
        return result

    finally:
        driver.quit()

if __name__ == "__main__":
    test_url = "https://www.sephora.com/product/stem-clinical-recovery-serum-P521628?skuId=2966935"
    data = scrape_sephora_product(test_url, 5)
    print(json.dumps(data, indent=2, ensure_ascii=False))
