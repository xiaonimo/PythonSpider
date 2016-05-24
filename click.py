import re
import urllib
import urllib.request

class csdn_click:
    def __init__(self):
        self.coding = 'UTF-8'
        self.url = 'http://blog.csdn.net/u011651743/article/list/200'
        self.rule_title = r'<span class="link_title"><a.*?>((?:.|[\r\n])*?)</a></span>'
        self.rule_click = r'<span class="link_view".*?><a.*?>.*?</a>((?:.|[\r\n])*?)</span>'
        self.rule_comment = r'<span class="link_comments".*?><a.*?>.*?</a>((?:.|[\r\n])*?)</span>'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) \
                        AppleWebKit/537.36 (KHTML, like Gecko)\
                         Chrome/50.0.2657.3 Safari/537.36'
        }

    def request(self):
        request = urllib.request.Request(self.url, headers=self.headers)
        return request

    def getData(self):
        try:
            html = urllib.request.urlopen(self.request())
            data = html.read()
            return data.decode(self.coding)
        except:
            print("Get data error!")
            return None

    def extractData(self):
        try:
            data = self.getData()
            titles = re.compile(self.rule_title)
            title = titles.findall(data)
            clicks = re.compile(self.rule_click)
            click = clicks.findall(data)
            comments = re.compile(self.rule_comment)
            comment = comments.findall(data)
            dataList = [title, click, comment]
            return dataList
        except:
            print('Extract data error!')

    def show(self):
        dataList = self.extractData()
        for n in range(len(dataList[0])):
            print(str(n) + "\n" + dataList[0][n] + "view-" + dataList[1][n] + "\n\tcomments-" + dataList[2][n])

click = csdn_click()
click.show()