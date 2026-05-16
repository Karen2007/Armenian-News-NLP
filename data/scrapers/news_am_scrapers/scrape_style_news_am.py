import requests
import time
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0'})

style_articles = [] # Store the style articles here

# Only 1k articles from the style category
first_article_number_style = 113000
last_article_number_style  = 114000

for article_number_style in range(first_article_number_style, last_article_number_style):

    full_text = ''
    title = ''

    try:
        url = f'https://style.news.am/arm/news/{article_number_style}/' # Article URL
        page = session.get(url, timeout=10)

        if page.status_code == 200:
            doc = BeautifulSoup(page.text, 'html.parser') # Get the HTML

            # ========= ARTICLE CONTENT ==========
            # Scrape the article content
            article_path = doc.find('div', {'id' : 'opennewstext'})
            article_p_tags = article_path.find_all('p')

            for p_tag in article_p_tags:
                full_text += p_tag.text

            # ========= TITLE ==========
            # Scrape the article title
            title_path = doc.find('div', {'id' : 'opennews'})
            title = title_path.h1.text

            # Store everything here
            style_articles.append({
                'title': title,
                'text': full_text,
                'category': 'Style',
                'source': url
            })

            time.sleep(2)


        # Stop sending requests for a while if rate limited
        elif page.status_code == 403 or page.status_code == 429:
            print('Rate limited, stopping for 60s.')
            time.sleep(60)
            continue

    except Exception as e:
        print(f'Error occurred: {e}')

    # Save every 50 articles in case of interruptions.
    if len(style_articles) % 50 == 0 and len(style_articles) > 0:
        pd.DataFrame(style_articles).to_csv('../../raw/style_news_am.csv', index=False)
        print(f"Saved {len(style_articles)} articles")

# Save the final articles
pd.DataFrame(style_articles).to_csv('../../raw/style_news_am.csv', index=False)
