import requests
import time
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0'})

tech_articles = [] # Store the tech articles here

# Only 1k articles from the tech category
first_article_number_tech = 6000
last_article_number_tech  = 7000

for article_number_tech in range(first_article_number_tech, last_article_number_tech):

    full_text = ''
    title = ''

    try:
        url = f'https://tech.news.am/arm/news/{article_number_tech}/' # Article URL
        page = session.get(url, timeout=10)

        if page.status_code == 200:
            doc = BeautifulSoup(page.text, 'html.parser') # Get the HTML

            # ========= ARTICLE CONTENT ==========
            # Scrape the article content
            article_path = doc.find('div', {'class' : 'bodycontainer'})
            article_p_tags = article_path.find_all('p')

            for p_tag in article_p_tags:
                full_text += p_tag.text

            # ========= TITLE ==========
            # Scrape the article title
            title_path = doc.find('div', {'id' : 'opennewstext'})
            title = title_path.h1.text

            # Store everything here
            tech_articles.append({
                'title': title,
                'text': full_text,
                'category': 'Tech',
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
    if len(tech_articles) % 50 == 0 and len(tech_articles) > 0:
        pd.DataFrame(tech_articles).to_csv('../../raw/tech_news_am.csv', index=False)
        print(f"Saved {len(tech_articles)} articles")