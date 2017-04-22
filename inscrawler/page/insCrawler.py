'''instagram crawler'''

import requests
import json
import re
from bs4 import BeautifulSoup

# from . import config
# cookie 应该保存到数据库里面
config = {
    'BASE_URL' : 'https://www.instagram.com/',
    'LOGIN_URL' : 'https://www.instagram.com/accounts/login/ajax/',
    'LOGOUT_URL' : 'https://www.instagram.com/accounts/logout/',
    'MEDIA_URL' : 'https://www.instagram.com/{0}/media',
    'STORIES_URL' : 'https://i.instagram.com/api/v1/feed/user/{0}/',
    'STORIES_UA' :'Instagram 9.5.2 (iPhone7,2; iPhone OS 9_3_3; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/420+',
    'STORIES_COOKIE' : 'ds_user_id={0}; sessionid={1};',
}
class Crawler(object):

    def __init__(self):
        self.session = requests.Session()

    def scrapeUrl(self, url):
        resp = self.session.get(url)
        print("url: " + url)
        share_data = resp.text.split('window._sharedData = ')[1].split(';</script>')[0]
        print(json.loads(share_data)['entry_data']['PostPage'][0]['graphql']['shortcode_media'])
        try:
            media = json.loads(share_data)['entry_data']['PostPage'][0]['media']
        except (KeyError,TypeError):
            media = json.loads(share_data)['entry_data']['PostPage'][0]['graphql']['shortcode_media']
        is_video = media['is_video']
        url = {}
        if is_video :
            url.update({"url":media['video_url']})
            url.update({'is_video':'is_video'})
        else:
            url.update({'url':media['display_url']})
        url.update({'userinfo':media['owner']})
        return url


    def scrapePerson(self,username,max_id=None):
        '''crawls through cookies and get user's media url'''
        # executor =concurrent.futures.ThreadPoolExecutor(max_workers=10)    # 多线程
        print('scrape start ...')
        # 开始爬取用户所有图片
        for item in self.media_gen(username,max_id):
            url.append(item['url'])
        return url


    def fetch_user(self,username):
        '''fetch user's metadata'''
        print('fetch user')
        resp = self.session.get(config['MEDIA_URL'].format(username))
        user = {}
        if resp.status_code == 200:
            try:
                user['user'] = json.loads(resp.text)['items'][0]['user']  # 用户信息
            except (TypeError,KeyError,IndexError):
                uers['error'] = 'error'
                user['user'] = '该用户为私密用户，如需要个人图片/视频，可联系站长获取。'
                user['user_en'] = 'The user is a private user, such as the need for personal pictures / video, can contact the webmaster to obtain.'
        elif resp.status_code == 404:
            user['error'] = 'error'
            user['user'] = '用户不存在，请确认后重新提交。'
            user['user_en'] = 'The user does not exist, please confirm and resubmit'
        return user

    def media_gen(self,username,max_id=None):
        """Generator of all user's media"""
        print('media_gen start')
        media = {}
        try:
            media = self.fetch_media_json(username, max_id)
        except ValueError:
            media['error_message'] = 'max_id错误，请重试!'
            media['error_message_en'] = 'max_id parameter error,please retry it.'
            return media
        urls = []
        for item in media['items']:
            urls.append(item[item['type'] + 's']['standard_resolution']['url'].split('?')[0])
        url = [self.set_media_url(url) for url in urls]
        message= {}
        message['urls'] = url
        if media.get('more_available'):
            max_id = media['items'][-1]['id']
            message['max_id'] = max_id
        return message

    def fetch_media_json(self, username, max_id):
        """Fetches the user's media metadata"""
        print('fetch_media_json')
        url = config['MEDIA_URL'].format(username)

        if max_id is not None:
            url += '?&max_id=' + max_id

        resp = self.session.get(url)

        if resp.status_code == 200:
            media = json.loads(resp.text)

            if not media['items']:
                raise ValueError('User {0} is private'.format(username))

            return media
        else:
            raise ValueError('User {0} does not exist'.format(username))

        #起过滤图片的作用
    def set_media_url(self, item):
        """Sets the media url"""
        # item['url'] = item[item['type'] + 's']['standard_resolution']['url'].split('?')[0]
        # remove dimensions to get largest image （获取最大的图片）
        item= re.sub(r'/s\d{3,}x\d{3,}/', '/', item)
        # get non-square image if one exists 原版系统（佩服佩服）
        item = re.sub(r'/c\d{1,}.\d{1,}.\d{1,}.\d{1,}/', '/', item)
        return item

    # 图片 清洗样例
    # https://scontent.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/c180.0.719.719/17881007_267580456985875_5757861933298483200_n.jpg
    # https://scontent.cdninstagram.com/t51.2885-15/sh0.08/e35/17881007_267580456985875_5757861933298483200_n.jpg


    # main调用函数
    def main(self,username,max_id=None):
        print('crawler start')
        try:
            media = self.media_gen(username,max_id)
        except ConnectionError:
            print('连接重置，请再试一次')
        print(media['urls'])
        print(media['max_id'])

#
# if __name__ == "__main__":
#     url_video = "https://www.instagram.com/p/BSX8ZfSg7ev/"
#     url_img = 'https://www.instagram.com/p/BS6eMlxgBpV/'
#     crawler = Crawler()
#     real_url = crawler.scrapeUrl(url_video)

# if __name__ == '__main__':
#     crawler = Crawler()
#     crawler.main('gem0816',None)