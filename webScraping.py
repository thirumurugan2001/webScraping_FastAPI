import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os

def WebScrap(url):
    try:
        def safe_extract_text(element, selector, class_name, strip_ranking=False):
            try:
                found = element.find(selector, class_=class_name)
                if found is None:
                    return 'N/A'
                text = found.text.strip()
                if strip_ranking:
                    text = re.sub(r'^\d+\.\s*', '', text)
                return text
            except Exception:
                return 'N/A'

        def scrape_imdb_top_movies(url):
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                movie_items = soup.find_all('li', class_='ipc-metadata-list-summary-item')
                
                if not movie_items:
                    print("No movie items found. The page structure might have changed.")
                    return None
                
                movies_data = []
                for idx, item in enumerate(movie_items, 1):
                    try:
                        title = safe_extract_text(item, 'h3', 'ipc-title__text', strip_ranking=True)
                        metadata_items = item.find_all('span', class_='cli-title-metadata-item')
                        year = metadata_items[0].text if len(metadata_items) > 0 else 'N/A'
                        duration = metadata_items[1].text if len(metadata_items) > 1 else 'N/A'
                        content_rating = metadata_items[2].text if len(metadata_items) > 2 else 'N/A'
                        
                        url_element = item.find('a', class_='ipc-title-link-wrapper')
                        movie_url = "https://www.imdb.com" + url_element['href'] if url_element and 'href' in url_element.attrs else 'N/A'
                        
                        movies_data.append({
                            'Rank': idx,
                            'Title': title,
                            'Year': year,
                            'Duration': duration,
                            'Content Rating': content_rating,
                            'URL': movie_url
                        })
                    except Exception as e:
                        print(f"Error processing movie #{idx}: {str(e)}")
                        continue
                
                if not movies_data:
                    print("No movie data was successfully extracted.")
                    return None
                
                return pd.DataFrame(movies_data)
            except Exception as e:
                print("Error in scrape_imdb_top_movies:", str(e))
                return None
        
        def save_to_excel(df):
            try:
                if df is None or df.empty:
                    print("No data to save")
                    return None
                
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                file_path = os.path.join(desktop_path, "IMDB_Top_Movies.xlsx")

                df.to_excel(file_path, index=False)
                print(f"Data successfully saved to: {file_path}")
                return file_path
            except Exception as e:
                print(f"Error saving to Excel: {str(e)}")
                return None

        df = scrape_imdb_top_movies(url)
        file_path = save_to_excel(df)
        return {
            "status Code": 200 if file_path else 500,
            "status": "success" if file_path else "failed",
            "message": "Data successfully scraped and saved to Excel file" if file_path else "Scraping failed or no data found",
            "file_path": file_path
        }
        
    except Exception as e:
        print("Error in WebScrap function:", str(e))
        return {
            "status Code": 500,
            "status": "failed",
            "message": "An error occurred during web scraping",
            "file_path": None
        }
