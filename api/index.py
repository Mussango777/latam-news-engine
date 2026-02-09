import feedparser
from flask import Flask, jsonify
import re

app = Flask(__name__)

# Список источников новостей Латинской Америки
RSS_FEEDS = [
    "https://www.efe.com/efe/america/9/rss",
    "http://feeds.reuters.com/reuters/latinAmericaNews",
    "https://en.mercopress.com/rss/latin-america",
    "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/america/portada",
    "https://rss.dw.com/rdf/rss-sp-top",
    "https://es.panampost.com/feed/",
    "https://insightcrime.org/feed/",
    "https://latinamericareports.com/feed",
    "https://www.bbc.com/mundo/topics/cl0905v04eet/index.xml",
    "https://www.france24.com/es/america-latina/rss",
    "https://cnnespanol.cnn.com/category/latinoamerica/feed/"
]

def extract_image(entry):
    """Функция для поиска ссылки на изображение в данных новости."""
    # 1. Ищем в стандартных тегах (media:content или enclosure)
    if 'media_content' in entry:
        return entry.media_content[0]['url']
    if 'links' in entry:
        for link in entry.links:
            if 'image' in link.get('type', ''):
                return link.get('href')
    
    # 2. Поиск картинки внутри HTML-описания (тег <img>)
    description = entry.get('summary', entry.get('description', ''))
    img_match = re.search(r'<img [^>]*src="([^"]+)"', description)
    if img_match:
        return img_match.group(1)
    
    return None

@app.route('/')
def get_news():
    results = []
    seen = set()
    
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                title = entry.title.strip()
                if title not in seen:
                    results.append({
                        'title': title,
                        'link': entry.link,
                        'description': entry.get('summary', entry.get('description', '')[:500]),
                        'image': extract_image(entry),
                        'source': url.split('/')[2],
                        'debug': 'v2' # Поле для проверки деплоя
                    })
                    seen.add(title)
        except:
            continue
            
    return jsonify(results)
