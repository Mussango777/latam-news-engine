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
    "https://news.google.com/rss/search?q=when:24h+site:apnews.com+Latin+America&hl=en-US&gl=US&ceid=US:en"
]

@app.route('/get_news')
def get_news():
    seen_titles = set()
    combined_news = []
    
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]:
                title = entry.title.strip()
                if title not in seen_titles:
                    combined_news.append({
                        'title': title,
                        'link': entry.link,
                        'description': entry.get('summary', entry.get('description', '')),
                        'source': url.split('/')[2]
                    })
                    seen_titles.add(title)
        except:
            continue
            
    return jsonify(combined_news)

if __name__ == '__main__':
    app.run()
