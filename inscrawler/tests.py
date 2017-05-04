
# Create your tests here.

import requests
import json

class Test(object):

    def __init__(self,username=None):
        self.session = requests.Session()
        self.username = username
        self.fetch_json_url = 'https://www.instagram.com/{0}/media'

    def fetch_media_json(self):
        print('start fetch media json')
        url = self.fetch_json_url.format(self.username)
        resp = self.session.get(url)
        print('response text: ')
        print(resp.text)
        media = json.loads(resp.text)
        return media
    def fetch_media_gen(self):
        media = self.fetch_media_json()
        print('media items: ')
        print(media['items'])
        urls = []
        for item in media['items']:
            urls.append(item[item['type'] + 's']['standard_resolution']['url'].split('?')[0])
        print('urls')
        print(urls)

if __name__ == '__main__':
    usernmae = 'amitsurti'
    test = Test(usernmae)
    test.fetch_media_gen()