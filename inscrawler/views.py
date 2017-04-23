from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .page import global_variables
from .models import Visitor
from .page.insCrawler import Crawler

# Create your views here.

#首页
def index(request):

    if request.META.get('HTTP_X_FORWARDED_FOR'):  # 有代理
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']          # 无代理

    # 获取浏览器本地语言
    language = request.META['HTTP_ACCEPT_LANGUAGE'].split(';')[0].split(',')[1]
    if language:
        print("language:" + str(language))
        if language in global_variables.chinese:
            global_language = '简体中文'
        else:
            global_language = 'English'

    # 默认的语言 English
    else:
        global_language = 'English'

    # 测试英语界面用
    Visitor.objects.create(ip=ip)

    # 获取参数传递的语言
    language_now = request.GET.get('language')
    if language_now:
        global_language = language_now

    # 设置session 有效期两个礼拜
    request.session['language'] = global_language
    change_global_language(global_language)
    content = {'url_base':request.path}
    content.update({'subtitle':'Instagram'})
    # 根据视图转发相应的地址
    if global_language == 'English':
        return render(request,'inscrawler/index-en.html',content)
    return render(request,'inscrawler/index.html',content)    #首页视图


# 爬取主函数
def ins(request):

    # 检查是否盗链以及获取对应的language
    language_now = check_lan(request)
    if not language_now:
        return HttpResponseRedirect(reverse('index'))
    content = {'subtitle': 'Instagram'}
    content.update({'url_base':request.path})

    # 从request获取语言
    if request.GET.get('language'):
        language_now = request.GET['language']

    # 获取表单传值url
    url_real = request.POST.get('url')

    #如果地址为空
    if not url_real:
        if language_now=='English':
            error = 'The url is empty,please try again.'
            content.update({'error_message': error})
            return render(request,'inscrawler/instagram-en.html',content)
        error = '地址不能为空，请重新输入'
        content.update({'error_message': error})
        return render(request, 'inscrawler/instagram.html', content)


    # 分析url
    url = url_real.split('/')
    #instagram crawler
    if(len(url) > 1 and url[2] == 'www.instagram.com'):
        # 帖子地址
        if(len(url) >= 6 and url[3] == 'p'):
            crawler = Crawler()
            url_crawler = crawler.scrapeUrl(url_real)
            content.update({'url':url_crawler})
        elif(len(url)==5):
            username = url[3]
            print('username: ' + username)
            crawler = Crawler()
            #获取userInfo
            userinfo = crawler.fetch_user(username)
            print('userinfo: ' + str(userinfo))
            if userinfo['user'] == 'error':
                if language_now== 'English':
                    content.update({'error_message':userinfo['user_en']})
                    return render(request,'inscrawler/instagram-en.html',content)
                content.update({'error_message': userinfo['user']})
                return render(request,'inscrawler/instagram.html',content)
            else:
                content.update({'userinfo':userinfo})
            message = crawler.media_gen(username,None)
            if message.get('error_message'):
                if language_now == 'English':
                    content.update({'error_message': message.get('error_message_en')})
                    return render(request,'inscrawler/instagram-en.html',content)
                content.update({'error_message': message.get('error_message')})
                return render(request, 'inscrawler/instagram.html', content)
            # 判断是否还有图片信息
            if message.get('max_id'):
                content.update({'max_id': message['max_id']})
                content['username'] = username
            content.update({'urls': message['urls']})

        # 返回正常信息
        if language_now =='English':
            return render(request,'inscrawler/instagram-en.html',content)
        return render(request,'inscrawler/instagram.html',content)

    else:
        if language_now == 'English':
            error = 'Address input error, please retry it.'
            content.update({'error_message': error})
            return render(request,'inscrawler/instagram-en.html',content)

        error = '地址输入错误，请重新输入'
        content.update({'error_message' : error})
        return render(request, 'inscrawler/instagram.html', content)


# 下一页
def ins2(request,max_id,username):
    language_now = check_lan(request)
    if not language_now:
        return HttpResponseRedirect(reverse('index'))

    # 从url获取语言
    if request.GET.get('language'):
        language_now = request.GET['language']

    crawler = Crawler()
    userinfo = crawler.fetch_user(username)
    content = {}
    content.update({'url_base':request.path})

    if userinfo['user'] == 'error':
        if language_now=='English':
            content.update({'error_message': userinfo['user_en']})
            return render(request,'inscrawler/instagram-en.html',content)
        content.update({'error_message': userinfo['user']})
        return render(request, 'inscrawler/instagram.html', content)
    else:
        content.update({'userinfo': userinfo})
    message = crawler.media_gen(username, max_id)   # 如果 max_id 错误，就会报500错误
    if message.get('error_message'):
        if language_now=='English':
            content.update({'error_message': message.get('error_message_en')})
            return render(request,'inscrawler/instagram-en.html'.content)
        content.update({'error_message':message.get('error_message')})
        return render(request, 'inscrawler/instagram.html', content)
    # 判断是否还有图片信息
    if message.get('max_id'):
        content.update({'max_id': message['max_id']})
        content['username'] = username
    content.update({'urls': message['urls']})
    if language_now == 'English':
        return render(request,'inscrawler/instagram-en.html',content)
    return render(request, 'inscrawler/instagram.html', content)


def file(request):
    content = {'url_base':request.path}
    language_now = check_lan(request)

    if request.GET.get('language'):
        language_now = request.GET['language']
        change_global_language(language_now)
    print(language_now)
    if not language_now:
        return HttpResponseRedirect(reverse('index'))
    if language_now == 'English':
        return render(request,'inscrawler/file-en.html',content)
    return render(request,'inscrawler/file.html',content)


def donate(request):
    content = {'url_base':request.path}
    language_now = check_lan(request)
    if not language_now:
        return HttpResponseRedirect(reverse('index'))
    if language_now=='English':
        return render(request,'inscrawler/donate-en.html',content)
    return render(request,'inscrawler/donate.html',content)


def page_not_found(request):
    return render(request, '404.html')


def page_error(request):
    return render(request, '500.html')


def change_global_language(language_now):
    global_variables.language_now = language_now
    # if language_now in global_variables.language:
    #     global_variables.language.remove(language_now)


def check_lan(request):
    language_now = request.session.get('language')
    if not language_now:
        change_global_language('English')
        return False
    else:
        change_global_language(language_now)
        return language_now