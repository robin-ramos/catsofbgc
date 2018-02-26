from InstagramAPI import InstagramAPI
from datetime import datetime as dt
import pandas as pd
import time

username = 'nicobaguio'
password = 'f6M24tyVRCmm'

if 'ig_api' not in globals():
    ig_api = InstagramAPI(username, password)

    ig_api.login()

if 'cat_posts' not in globals():
    cat_posts = []
    has_more_posts = True
    max_id = ""

    while has_more_posts:
        ig_api.getHashtagFeed('catsofbgc', maxid=max_id)
        if ig_api.LastJson['more_available'] is not True:
            has_more_posts = False
            print('End of Feed')

        max_id = ig_api.LastJson.get('next_max_id', '')
        cat_posts.extend(ig_api.LastJson['items'])
        time.sleep(2)

texts = []
links = []
times = []


def ig_link(code):
    return f'https://www.instagram.com/p/{code}/'


for c, post in enumerate(cat_posts):
    if post['caption'] is not None:
        text = post['caption']['text']
        time = dt.utcfromtimestamp(post['caption']['created_at_utc'])

    else:
        text = ''
        time = dt.utcfromtimestamp(
            post['preview_comments'][0]['created_at_utc']
        )

    texts.append(text)
    times.append(time)
    links.append(ig_link(post['code']))

main_df = pd.DataFrame({
    'text': texts,
    'time': times,
    'link': links
})
