import feedparser
import tweepy
import json
import os

# Configuration
RSS_FEED_URL = "https://rss.app/feeds/eA6gjQ0GqyNrRCvk.xml"
POSTED_FILE = "posted_articles.json"

# Clés API Twitter (on va récupérer via secrets GitHub)
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

# Authentification Twitter
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# Charger les articles déjà postés
if os.path.exists(POSTED_FILE):
    with open(POSTED_FILE, "r") as f:
        posted_links = set(json.load(f))
else:
    posted_links = set()

# Parser le flux RSS
feed = feedparser.parse(RSS_FEED_URL)

new_links = []
for entry in feed.entries:
    link = entry.link
    title = entry.title
    if link not in posted_links:
        tweet = f"{title} {link}"
        try:
            api.update_status(tweet)
            print(f"Tweet publié : {tweet}")
            new_links.append(link)
        except Exception as e:
            print(f"Erreur publication : {e}")

# Mettre à jour la liste des articles postés
posted_links.update(new_links)
with open(POSTED_FILE, "w") as f:
    json.dump(list(posted_links), f)
