import time
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

articles = [] # Store articles here

# First and last article on armenpress.am are here
first_article_number = 368328
last_article_number = 1250000

# Draw random articles
article_numbers = np.random.choice(a=np.arange(first_article_number, last_article_number), size=2500, replace=False)

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0'})


for article_number in article_numbers:
    try:
        url = f"https://armenpress.am/hy/article/{article_number}"  # URL of article
        page = session.get(url, timeout=10)  # Send a request to the page


        if page.status_code == 200: # Only continue if request is successful
            doc = BeautifulSoup(page.text, 'html.parser') # Get the html of the website

            # Search for the article content
            article_path = doc.body.div.div.main.article.find('div', {'class' : 'nra prose ti cba ay xd pb yc ob yd y wb lc xb r da yua'})
            article_content = article_path.find_all('p')

            # Store the article text here
            full_text = ''

            # Add every p tag content to full_text
            for p_tag in article_content:
                full_text += p_tag.text

            # Search for the category of the article
            category = 'Unknown'
            category_path = doc.body.div.div.main.article.nav.div
            if category_path.p.text == "Բաժին":
                category = category_path.div.a.text.strip() # Clean spaces from the beginning


            # Search for the title of the article
            title_path = doc.body.div.div.main.article.div.h1
            title = title_path.text

            # Append all info to articles list
            articles.append({
                'title': title,
                'text': full_text,
                'category': category,
                'source': url
            })

            # Wait a bit before sending a new request
            time.sleep(2)

        # Stop sending requests for a while if rate limited
        elif page.status_code == 403 or page.status_code == 429:
            print('Rate limited, stopping for 60s.')
            time.sleep(60)
            continue


    # Skip article if something goes wrong
    except Exception as e:
        print(f"Failed on {article_number}: {e}")
        continue

    # Save every 100 articles in case of interruptions.
    if len(articles) % 100 == 0 and len(articles) > 0:
        pd.DataFrame(articles).to_csv('../raw/armenpress_articles.csv', index=False)
        print(f"Saved {len(articles)} articles")