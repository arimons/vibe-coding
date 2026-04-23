import requests
from bs4 import BeautifulSoup

def extract_sephora_product_info(url: str) -> dict:
    """
    세포라 상품 URL에서 브랜드명과 상품명을 추출합니다.
    """
    # 봇 차단을 우회하기 위해 일반적인 브라우저의 User-Agent를 사용합니다.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # data-at 속성을 이용하여 요소 찾기
        brand_tag = soup.find(attrs={"data-at": "brand_name"})
        product_tag = soup.find(attrs={"data-at": "product_name"})
        
        brand_name = brand_tag.text.strip() if brand_tag else None
        product_name = product_tag.text.strip() if product_tag else None
        
        return {
            "brand_name": brand_name,
            "product_name": product_name
        }
        
    except requests.exceptions.RequestException as e:
        print(f"URL 요청 중 에러 발생: {e}")
        return {"brand_name": None, "product_name": None}

if __name__ == "__main__":
    test_url = "https://www.sephora.com/product/the-dewy-skin-cream-P441101?skuId=2406866&icid2=jumbo%20size%20beauty_us_skugrid_ufe:p441101:product"
    
    print("스크래핑 진행 중...")
    result = extract_sephora_product_info(test_url)
    
    print(f"브랜드명: {result.get('brand_name')}")
    print(f"상품명: {result.get('product_name')}")
