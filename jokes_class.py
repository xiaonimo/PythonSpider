import re
import urllib
import urllib.request

class getJoke:
    def __init__(self):
        self.joke_cnt = 1
        self.url_tail = 1
        self.save_path = 'E:\qb_jokes.txt'
        self.rule_joke = r'<div class="content">((?:.|[\r\n])*?)</div>'
        self.url_header = r'http://www.qiushibaike.com/8hr/page/'

    def saveJoke(self):
        joke_file = open(self.savePath, 'w')
        try:
            joke_file.write(self.data)
        except:
            pass
        joke_file.close()

    def extractJoke(self):
        url = self.url_header + str(self.url_tail)
        request = urllib.request.Request(url, headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/'
                             '537.36 (KHTML, like Gecko)\ Chrome/'
                             '50.0.2657.3 Safari/537.36'
        })

        try:
            html = urllib.request.urlopen(request)
            data = html.read()
        except:
            print('Parser Html Error!')
            return

        jokes = re.compile(self.rule_joke)
        try:
            joke = jokes.findall(data.decode("UTF-8"))
        except:
            print("Find jokes error!\n")
            return

        return joke

# j = getJoke()
# for n in range(1, 10):
	# j.url_tail = n
	# jokes = j.extractJoke()
	# print(str(len(jokes)) + '\n')