import feedparser
from flask import Flask, jsonify

app = Flask(__name__)

# Полный список из 12 топовых источников по твоему ТЗ
RSS_FEEDS = [
    "https://www.efe.com/efe/america/9/rss",
    "http://feeds.reuters.com/reuters/latinAmericaNews",
    "https://en.mercopress.com/rss/latin-america",
    "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/america/portada",
    "https://rss.dw.com/rdf/rss-sp-top",
    "https://es.panampost.com/feed/",
    "https://insightcrime.org/feed/",
    "https://latinamericareports.com/feed",
    "https://www.bbc.com/mundo/topics/cl0905v04eet/index.xml", # Специально LatAm
    "https://www.france24.com/es/america-latina/rss",
    "https://cnnespanol.cnn.com/category/latinoamerica/feed/"
]

@app.route('/')
def get_news():
    results = []
    seen = set()
    
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            # Берем по 5 свежих новостей из каждого источника
            for entry in feed.entries[:5]:
                title = entry.title.strip()
                if title not in seen:
                    results.append({
                        'title': title,
                        'link': entry.link,
                        'description': entry.get('summary', entry.get('description', '')[:300]),
                        'source': url.split('/')[2]
                    })
                    seen.add(title)
        except:
            continue
            
    return jsonify(results)
