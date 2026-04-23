import sys
import importlib
if 'scraper' in sys.modules:
    importlib.reload(sys.modules['scraper'])

import os
import glob
import json
import streamlit as st
import pandas as pd
from scraper import scrape_sephora_product

st.set_page_config(page_title="Sephora Premium Scraper", layout="wide")

def load_saved_results():
    if not os.path.exists('saved_scrapes'):
        return []
    files = glob.glob('saved_scrapes/*.json')
    files.sort(key=os.path.getmtime, reverse=True)
    return files

def render_result(data):
    st.title(data.get('product_name', 'Unknown Product'))
    st.caption(f"by {data.get('brand', 'Unknown Brand')}")
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        images = data.get('images', [])
        if images:
            # Show first image large, rest as 3-column grid
            st.image(images[0], use_column_width=True)
            if len(images) > 1:
                st.caption(f"📸 {len(images)} images total")
                cols_per_row = 3
                rows = [images[1:][i:i+cols_per_row] for i in range(0, len(images[1:]), cols_per_row)]
                for row in rows:
                    grid = st.columns(cols_per_row)
                    for idx, img in enumerate(row):
                        with grid[idx]:
                            st.image(img, use_column_width=True)
        else:
            st.warning("No images collected.")

            
    with col2:
        st.write("### Product Details")
        st.metric(label="Price", value=data.get('price', 'N/A'))
        st.metric(label="Size",  value=data.get('size',  'N/A'))

        # Rating: rating is stored as a string like "4.90"
        rating_raw = data.get('rating')
        review_count_total = data.get('review_count_total')
        if rating_raw:
            try:
                rating_float = float(rating_raw)
                stars = "⭐" * round(rating_float)
                label = f"{stars}  {rating_float}"
                if review_count_total:
                    label += f"  ({review_count_total} reviews)"
                st.write(f"**Rating:** {label}")
            except Exception:
                pass

        url = data.get('url', '')
        if url:
            st.markdown(f"**URL:** [{url}]({url})")

        st.caption(f"Collected: {data.get('scraped_at', '').split('T')[0]}")

        ingredients = data.get('ingredients', '')
        if ingredients:
            st.write("**Ingredients:**")
            st.write(ingredients)

            
    st.divider()
    
    revs = data.get('reviews', [])
    st.subheader(f"Customer Reviews ({len(revs)})")
    
    if revs and isinstance(revs[0], dict):
        for r in revs:
            with st.container():
                rating_width = r.get('rating', '')
                stars = "⭐⭐⭐⭐⭐"
                if '80%' in rating_width: stars = "⭐⭐⭐⭐"
                elif '60%' in rating_width: stars = "⭐⭐⭐"
                elif '40%' in rating_width: stars = "⭐⭐"
                elif '20%' in rating_width: stars = "⭐"

                st.markdown(f"**{stars} | {r.get('title', 'No Title')}**")
                st.caption(f"{r.get('username', 'Anonymous')}  {r.get('date', '')}")
                st.write(r.get('body', 'No review body.'))
                st.markdown("---")
    else:
        st.warning("No structured reviews found. Please run a new extraction.")

def main():
    st.sidebar.title("Sephora Scraper")
    mode = st.sidebar.radio("Navigation", ["New Scrape", "View Saved Results"])
    
    if mode == "New Scrape":
        url = st.text_input("Enter Sephora Product URL:", "https://www.sephora.com/product/stem-clinical-recovery-serum-P521628?skuId=2966935")
        review_count = st.slider("Target Number of Reviews", min_value=1, max_value=200, value=20, step=1)
        
        if st.button("Start Extraction"):
            if url:
                with st.spinner("Extracting data via DOM evaluation..."):
                    try:
                        result = scrape_sephora_product(url, target_review_count=review_count)
                        st.success(f"Extraction successful! {len(result['images'])} images · {len(result['reviews'])} reviews")
                        if result.get('_reviews_file'):
                            st.caption(f"📄 Reviews saved → `{result['_reviews_file']}`")

                        st.session_state['current_result'] = result
                    except Exception as e:
                        st.error(f"Error during scraping: {str(e)}")
            else:
                st.warning("Please enter a valid URL.")
                
        if 'current_result' in st.session_state:
            render_result(st.session_state['current_result'])
            
    else:
        st.title("Saved Extraction Archives")
        saved_files = load_saved_results()
        if not saved_files:
            st.info("No saved records found in /saved_scrapes.")
        else:
            selected_file = st.selectbox("Select an archive to display", saved_files, format_func=lambda x: os.path.basename(x))
            if selected_file:
                with open(selected_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                render_result(data)

if __name__ == "__main__":
    main()
