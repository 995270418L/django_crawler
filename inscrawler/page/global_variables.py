'''全局变量的设置'''

language = ['简体中文','English']
language_now = ''
chinese = ['zh-cn','zh-CN','zh-TW','cn','CN','zh','cn']
def setting(request):
    return {'language':language,'language_now':language_now}