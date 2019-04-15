from crawler.spider import Spider
from crawler.writter import DataWriter
from lxml import html


writter = DataWriter('data.txt')


def geturl(response):
    # 自定义URL解析函数，对下一页的URL进行提取。观察网站结构可以看出：
    #    首页与其他页的下一页不是同一个xpath路径，根据不同的网络层级进行解析
    body = html.fromstring(response['text'])
    if response['level'] == 1:
        urls = [{'url': 'https://movie.douban.com/subject/26810318/comments' +
                 url} for url in body.xpath('//*[@id="paginator"]/a/@href')]
    else:
        urls = [{'url': 'https://movie.douban.com/subject/26810318/comments' +
                 url} for url in body.xpath('//*[@id="paginator"]/a[3]/@href')]
    return urls


def getdata(response):
    # 自定义data解析函数，对我们所需要的数据进行提取。
    body = html.fromstring(response['text'])
    comments = body.xpath('//*[@id="comments"]/div/div[2]/p/span/text()')
    writter.write_buffer([comments])


spider = Spider(
    'https://movie.douban.com/subject/26810318/comments?start=0&limit=20&sort=new_score&status=P',
    getUrl_func=geturl, getData_func=getdata, level=6)
spider.start_crawl()
