import re
import urllib
import urllib.request

cnt = 1
url = 'http://blog.csdn.net/u011651743/article/list/200'
rule_title = r'<span class="link_title"><a.*?>((?:.|[\r\n])*?)</a></span>'
rule_click = r'<span class="link_view".*?><a.*?>.*?</a>((?:.|[\r\n])*?)</span>'
rule_comment = r'<span class="link_comments".*?><a.*?>.*?</a>((?:.|[\r\n])*?)</span>'
request = urllib.request.Request(url, headers = {
            'username':'958456112@qq.com',
            'password':'tongtong666',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1) \
            AppleWebKit/537.36 (KHTML, like Gecko)\
             Chrome/50.0.2657.3 Safari/537.36'
    })

try:
    html = urllib.request.urlopen(request)
    data = html.read()

    titles = re.compile(rule_title)
    title = titles.findall(data.decode('UTF-8'))
    clicks = re.compile(rule_click)
    click = clicks.findall(data.decode('UTF-8'))
    comments = re.compile(rule_comment)
    comment = comments.findall(data.decode('UTF-8'))

    for n in range(len(title)):
        print(str(cnt)+"\n"+title[n]+"view-"+click[n]+"\n\tcomments-"+comment[n])
        cnt += 1
except:
    print('error')


