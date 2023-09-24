import requests
url = 'http://www.baidu.com/'
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
}
response = requests.get(url, headers=headers)
print(response.status_code)
from lxml import etree
html = etree.HTML(response.text)
news_list = html.xpath(
            '//ul[@class="s-hotsearch-content"]/li'
        )
print(news_list)

for li in news_list:
    content = li.xpath('a/span[1]/text()')
    print(content)