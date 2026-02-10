import feedparser
from flask import Flask, jsonify
import re

app = Flask(__name__)

RSS_FEEDS = [
    "http://feeds.reuters.com/reuters/latinAmericaNews", "https://www.bloomberglinea.com/rss/",
    "https://www.bnamericas.com/en/rss", "https://insightcrime.org/feed/",
    "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/america/portada",
    "https://apnews.com/hub/latin-america?format=rss", "https://www.infobae.com/america/rss/",
    "https://www.riotimesonline.com/feed/", "https://cnnespanol.cnn.com/category/latinoamerica/feed/",
    "https://en.mercopress.com/rss/latin-america", "https://www.france24.com/es/america-latina/rss",
    "https://www.prensa-latina.cu/index.php?option=com_content&view=featured&format=feed&type=rss"
]

@app.route('/')
def get_news():
    raw_pool = []
    seen_titles = set()
    
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            # ГЛУБИНА: Берем 10 последних, чтобы не пропустить важное
            for entry in feed.entries[:10]:
                title = entry.title.strip().lower()
                # ВНУТРЕННЯЯ ОЧИСТКА: если два сайта написали один и тот же заголовок - берем один
                if title not in seen_titles:
                    raw_pool.append({
                        "title": entry.title.strip(),
                        "link": entry.link,
                        "image": entry.get('media_content', [{}])[0].get('url') or "https://via.placeholder.com/600x400.png?text=LATAM+NEWS"
                    })
                    seen_titles.add(title)
        except Exception: continue
    
    # СОРТИРОВКА И ЛИМИТ: Отдаем только 20 самых свежих кандидатов для Make.com
    # Это экономит твои кредиты: Make проверит 20 штук вместо 120
    return jsonify(raw_pool[:20])
