import requests
import os
from datetime import datetime, timedelta

def check_news():
    telegram_token = os.environ['8163566013:AAGehpA1nK4aolluEExhe7fkOHsyRGs4q0s']
    chat_id = os.environ['8584955447']
    newsapi_key = os.environ['f090d56584434f3683ea5636b486416b']
    
    # CUSTOMIZE YOUR TOPICS HERE
    topics = [
        'artificial intelligence',
        'climate change',
        'SpaceX'
    ]
    
    print(f"🔍 Checking news at {datetime.now()}")
    
    for topic in topics:
        print(f"\nChecking: {topic}")
        
        # Fetch news from last 3 hours
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': topic,
            'apiKey': newsapi_key,
            'language': 'en',
            'sortBy': 'publishedAt',
            'from': (datetime.now() - timedelta(hours=3)).strftime('%Y-%m-%d'),
            'pageSize': 2
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            articles = response.json().get('articles', [])
            
            # Send to Telegram
            for article in articles[:2]:  # Max 2 per topic
                title = article.get('title', 'No title')
                description = article.get('description', '')
                article_url = article.get('url', '')
                source = article.get('source', {}).get('name', 'Unknown')
                
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
                
                if telegram_response.status_code == 200:
                    print(f"✅ Sent: {title[:50]}")
                else:
                    print(f"❌ Failed to send: {title[:50]}")
                    
        except Exception as e:
            print(f"❌ Error checking {topic}: {e}")
    
    print(f"\n✅ News check completed at {datetime.now()}")

if __name__ == "__main__":
    check_news()
