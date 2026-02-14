import requests
import os
from datetime import datetime, timedelta

def check_news():
    telegram_token = os.environ['TELEGRAM_TOKEN']
    chat_id = os.environ['CHAT_ID']
    newsapi_key = os.environ['NEWSAPI_KEY']
    
    # CUSTOMIZE YOUR TOPICS HERE
    topics = [
        'KRN Heaters and Exchangers',
        'Kaynes Technology',
        'India Defence'
        'India Power'
        'Quality Power Ltd'
    ]
    
    print(f"🔍 Checking news at {datetime.now()}")
    print(f"Chat ID: {chat_id}")
    
    for topic in topics:
        print(f"\n{'='*50}")
        print(f"Checking: {topic}")
        
        # Fetch news from last 24 hours (changed from 3 hours to get more results)
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': topic,
            'apiKey': newsapi_key,
            'language': 'en',
            'sortBy': 'publishedAt',
            'from': (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%d'),
            'pageSize': 3
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            print(f"NewsAPI Status Code: {response.status_code}")
            
            if response.status_code != 200:
                print(f"❌ NewsAPI Error: {response.text}")
                continue
                
            data = response.json()
            
            if data.get('status') != 'ok':
                print(f"❌ API returned error: {data.get('message', 'Unknown error')}")
                continue
            
            articles = data.get('articles', [])
            print(f"Found {len(articles)} articles")
            
            if len(articles) == 0:
                print("No articles found for this topic")
                continue
            
            # Send to Telegram
            for i, article in enumerate(articles[:2], 1):  # Max 2 per topic
                title = article.get('title', 'No title')
                description = article.get('description', '')
                article_url = article.get('url', '')
                source = article.get('source', {}).get('name', 'Unknown')
                
                print(f"\n  Article {i}: {title[:50]}...")
                
                # Format message
                message = f"📰 <b>{title}</b>\n\n"
                
                if description:
                    desc = description[:150]
                    if len(description) > 150:
                        desc += "..."
                    message += f"{desc}\n\n"
                
                message += f"🔗 <a href='{article_url}'>Read full article</a>\n"
                message += f"📅 {source}"
                
                # Send to Telegram
                telegram_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
                telegram_response = requests.post(telegram_url, json={
                    'chat_id': chat_id,
                    'text': message,
                    'parse_mode': 'HTML',
                    'disable_web_page_preview': False
                }, timeout=10)
                
                print(f"  Telegram Status Code: {telegram_response.status_code}")
                
                if telegram_response.status_code == 200:
                    print(f"  ✅ Sent successfully")
                else:
                    print(f"  ❌ Failed: {telegram_response.text}")
                    
        except Exception as e:
            print(f"❌ Error: {type(e).__name__}: {e}")
    
    print(f"\n{'='*50}")
    print(f"✅ News check completed at {datetime.now()}")

if __name__ == "__main__":
    check_news()
