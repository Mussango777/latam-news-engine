import feedparser
from flask import Flask, jsonify
import re

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
    # Чистим ссылку от "мыла" и скобок (защита от ошибки Render 46)
    url = re.sub(r'/\d+x\d+/', '/', url)
    filters = ["-80x80", "_thumb", "_small", "-100x100"]
    for f in filters:
        url = url.replace(f, "")
    return url.strip("() ")

@app.route('/')
def get_news():
    results = []
    seen = set()
    # В ТЕСТОВОМ РЕЖИМЕ: проверяем все источники сразу
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                entry = feed.entries[0] # Берем только 1 самую свежую новость
                title = entry.title.strip()
                if title not in seen:
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
