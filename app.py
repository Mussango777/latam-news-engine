import feedparser
from flask import Flask, jsonify

app = Flask(__name__)

# 1. ГЛАВНАЯ СТРАНИЦА - для проверки
@app.route('/')
def home():
    return "<h1>Бот в эфире!</h1><p>Проверь данные тут: <a href='/news'>/news</a></p>"

# 2. СТРАНИЦА С НОВОСТЯМИ (сделали короткий адрес /news для надежности)
@app.route('/news')
@app.route('/get_news')
def get_news():
    results = []
    seen = set()
    
    # Список лент
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

    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
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

if __name__ == '__main__':
    app.run()
