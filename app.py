import feedparser
from flask import Flask, jsonify
import re
from datetime import datetime

app = Flask(__name__)

RSS_FEEDS = [
    "https://www.efe.com/efe/america/9/rss", "http://feeds.reuters.com/reuters/latinAmericaNews",
    "https://en.mercopress.com/rss/latin-america", "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/america/portada",
    "https://rss.dw.com/rdf/rss-sp-top", "https://es.panampost.com/feed/",
    "https://insightcrime.org/feed/", "https://latinamericareports.com/feed",
    "https://www.bbc.com/mundo/topics/cl0905v04eet/index.xml", "https://www.france24.com/es/america-latina/rss",
    "https://cnnespanol.cnn.com/category/latinoamerica/feed/", "https://www.infobae.com/america/rss/"
]

def upgrade_image_quality(url):
    if not url: return None
    url = re.sub(r'/\d+x\d+/', '/', url) # Убираем /100x80/
    quality_filters = ["-80x80", "_thumb", "_small", "-100x100"]
    for f in quality_filters:
        url = url.replace(f, "")
    return url.strip("() ") # Очистка от скобок (защита от ошибки Render 46)

def get_rotating_feeds():
    # Группируем по 4 источника. Каждые 4 часа меняем группу.
    hour = datetime.utcnow().hour
    batch_index = (hour // 4) % 3 # 0, 1 или 2
    start = batch_index * 4
    end = start + 4
    return RSS_FEEDS[start:end]

@app.route('/')
def get_news():
    results = []
    seen = set()
    active_feeds = get_rotating_feeds()
    
    for url in active_feeds:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:2]: # Берем по 2 новости для макс. экономии
                title = entry.title.strip()
                if title not in seen:
                    # Ищем картинку в разных тегах
                    img = None
                    if 'media_content' in entry: img = entry.media_content[0]['url']
                    elif 'description' in entry:
                        match = re.search(r'src="([^"]+)"', entry.description)
                        if match: img = match.group(1)
                    
                    results.append({
                        'title': title,
                        'link': entry.link,
                        'description': entry.get('summary', '')[:300],
                        'image': upgrade_image_quality(img),
                        'source': url.split('/')[2]
                    })
                    seen.add(title)
        except: continue
    return jsonify(results)
