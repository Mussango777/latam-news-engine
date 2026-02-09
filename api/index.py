import feedparser
from flask import Flask, jsonify

app = Flask(__name__)

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
                    # Поиск картинки в разных форматах RSS
                    img_url = None
                    if 'media_content' in entry:
                        img_url = entry.media_content[0]['url']
                    elif 'links' in entry:
                        for link in entry.links:
                            if 'image' in link.get('type', ''):
                                img_url = link.get('href')
                    
                    results.append({
                        'title': title,
                        'link': entry.link,
                        'description': entry.get('summary', entry.get('description', '')[:300]),
                        'image': img_url,
                        'source': url.split('/')[2]
                    })
                    seen.add(title)
        except:
            continue
            
    return jsonify(results)
