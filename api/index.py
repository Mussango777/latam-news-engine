import feedparser
from flask import Flask, jsonify

app = Flask(__name__)

# Список твоих источников
RSS_FEEDS = [
    "https://www.efe.com/efe/america/9/rss",
    "http://feeds.reuters.com/reuters/latinAmericaNews",
    "https://en.mercopress.com/rss/latin-america",
    "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/america/portada",
    "https://rss.dw.com/rdf/rss-sp-top",
    "https://es.panampost.com/feed/",
    "https://insightcrime.org/feed/",
    "https://latinamericareports.com/feed"
]

@app.route('/')
def home():
    return "<h1>Vercel работает!</h1><p>Новости тут: <a href='/news'>/news</a></p>"

@app.route('/news')
@app.route('/get_news')
def get_news():
    results = []
    seen = set()
    
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            # Берем по 5 свежих новостей
            for entry in feed.entries[:5]:
                title = entry.title.strip()
                if title not in seen:
                    results.append({
                        'title': title,
                        'link': entry.link,
                        'description': entry.get('summary', entry.get('description', '')[:200]),
                        'source': url.split('/')[2]
                    })
                    seen.add(title)
        except:
            continue
            
    return jsonify(results)

# Для Vercel важно, чтобы переменная называлась app
# Блок if __name__ == "__main__" здесь не обязателен, но и не мешает
