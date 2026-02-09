import feedparser
from flask import Flask, jsonify

app = Flask(__name__)

# Теперь новости будут прямо тут! Никаких лишних папок и слэшей.
@app.route('/')
def get_news_fast():
    results = []
    seen = set()
    RSS_FEEDS = [
        "https://www.efe.com/efe/america/9/rss",
        "http://feeds.reuters.com/reuters/latinAmericaNews",
        "https://en.mercopress.com/rss/latin-america",
        "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/america/portada",
        "https://rss.dw.com/rdf/rss-sp-top"
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
                        'description': entry.get('summary', entry.get('description', '')[:200])
                    })
                    seen.add(title)
        except:
            continue
            
    return jsonify(results)

if __name__ == '__main__':
    app.run()
