import argparse
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

def extract_sephora_data(url: str):
    try:
        with sync_playwright() as p:
            # 봇 차단을 피하기 위해 headless 모드로 브라우저 실행
            browser = p.chromium.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled", "--disable-web-security"]
            )
            context = browser.new_context(
                viewport={"width": 1280, "height": 800},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            # 추가적인 봇 탐지 우회 적용 (stealth)
            stealth_sync(page)
            
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            # 브라우저가 렌더링한 최종 HTML을 가져와 BeautifulSoup으로 파싱
            html = page.content()
            soup = BeautifulSoup(html, 'html.parser')
            
            # 1. 브랜드명
            brand_tag = soup.select_one('[data-at="brand_name"]')
            brand = brand_tag.text.strip() if brand_tag else "N/A"
            
            # 2. 상품명
            product_tag = soup.select_one('[data-at="product_name"]')
            product_name = product_tag.text.strip() if product_tag else "N/A"
            
            # 3. 가격
            price_tag = soup.select_one('[data-comp="Price "] b')
            price = price_tag.text.strip() if price_tag else "N/A"
            
            # 4-1. 별점
            rating_tag = soup.select_one('[data-comp="StarRating "]')
            rating = rating_tag.get('aria-label') if rating_tag else "N/A"
            
            # 4-2. 리뷰 수
            reviews_tag = soup.select_one('[data-at="number_of_reviews"]')
            review_count = reviews_tag.text.strip() if reviews_tag else "N/A"
            
            # 결과 출력
            print("="*40)
            print(f"🛍️ 브랜드명 : {brand}")
            print(f"📦 상품명   : {product_name}")
            print(f"💰 가격     : {price}")
            print(f"⭐ 별점     : {rating}")
            print(f"📝 리뷰 수  : {review_count}")
            print("="*40)
            
            browser.close()
            
    except Exception as e:
        print(f"❌ URL 데이터를 가져오는 중 에러가 발생했습니다: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="세포라 상품 정보 추출기")
    parser.add_argument("url", type=str, help="추출할 세포라 상품의 URL")
    
    args = parser.parse_args()
    
    print("데이터를 추출 중입니다... (Playwright 사용)")
    extract_sephora_data(args.url)
