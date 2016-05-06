import re
import urllib
import urllib.request

def saveData(data, savePath):
    f = open(savePath, 'a')
    try:
        f.write(data)
    except:
        pass
    f.close()

cnt = 1
rule_joke = r'<div class="content">(?:.|[\r\n])*?</div>'
savePath = 'E:\qb_jokes.txt'
url_header = 'http://www.qiushibaike.com/8hr/page/'
url_tail = 1

while 1:
    url = url_header + str(url_tail)
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

    jokes = re.compile(rule_joke)
    try:
        joke = jokes.findall(data.decode("UTF-8"))
    except:
        print("Find jokes error!\n")
        continue
    
    for j in joke:
        j_split = j.split("<")[1].split(">")[1]
        print(str(cnt) + j_split + "\n")
        saveData(str(cnt) + j_split + "\n", savePath)
        cnt += 1
    url_tail += 1
    
