import requests
import json
import sys
import time

def get_posts():
    url = "http://localhost:8080"
    api_url = url + "/api/posts"
    r = requests.get(api_url)
    if r.status_code == 200 or 201:
        posts = json.loads(r.text)
        print(posts)

def posts_timed():
	while True:
		get_posts()
		time.sleep(3)

posts_timed()
