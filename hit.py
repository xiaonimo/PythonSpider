import re
import urllib
import urllib.request
from collections import deque

def savePic(data, save_path):
    try:
        f = open(save_path, 'wb')
        f.write(data)
        f.close()
    except:
        f.close()
        pass
    f.close()

cnt = 1
queue = deque()
visited = set()
rule_url = r'href="(.+?)"'
rule_pic = r'<img.*?src="(.*?)".*?>'
save_path = r'E:\hit_pic'
url_header = 'http://www.cs.hit.edu.cn'
queue.append('http://www.cs.hit.edu.cn/')

while queue:
    url_tail = queue.popleft()
    if (url_header in url_tail):
        url = url_tail
    elif url_tail[:4] == '/?q=':
        url = url_header + url_tail
    else:
        continue
    if url in visited:
        continue

    visited |= {url}
    request = urllib.request.Request(url, headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)\
             Chrome/50.0.2657.3 Safari/537.36'
    })
    
    try:
        html = urllib.request.urlopen(request)
        data = html.read()
    except:
        print('Parser Html Error!')
        continue

    try:
        links = re.compile(rule_url)
        link = links.findall(data.decode("UTF-8"))
    except:
        print("Data decode error!\n")
        continue
    
    for x in link:
        if (x not in visited) and (x not in queue) and (len(queue) < 50):
            queue.append(x)
            #print(x)
    # print(url + "\n")


    pics = re.compile(rule_pic)
    try:
        pic_path = pics.findall(data.decode("UTF-8"))
    except:
        print("Find pics error!\n")
        continue

    for j in pic_path:
        try:
            if url_header in j:
                pic_url = j
            else:
                pic_url = url_header + j
            request = urllib.request.Request(pic_url, headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1) \
            AppleWebKit/537.36 (KHTML, like Gecko)\
             Chrome/50.0.2657.3 Safari/537.36'
    })
            html = urllib.request.urlopen(request)
            data = html.read()
        except:
            continue
        if '?' in j:
            name = j.split(r'?')[0].split(r'/').pop()
        else:
            name = j.split(r'/').pop()
        print(save_path +'\\' + name)
        savePic(data, save_path +'\\' + name)
    
