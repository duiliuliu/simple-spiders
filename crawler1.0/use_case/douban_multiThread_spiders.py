# -*- coding： utf-8 -*-
# author：pengr


def 多线程爬取示例():
    '''
    simple-spiders多线程爬取案列 本篇案列带你完成下列任务：

        1. 创建一个simple-spiders项目

        2. 创建爬取网站的spider

        3. 存储爬取到的数据 
        
        4. 以多线程方式启动


    导入库

    >>>
    from crawler.spider import Spider
    from crawler.writter import DataWriter
    from lxml import html

    创建写入对象

    >>>
    writter = DataWriter('data_multi_process.txt')

    URL解析函数实现

    >>>
    def geturl(response):
        body = html.fromstring(response['text'])
        if response['level'] == 1:
            urls = [{'url': 'https://movie.douban.com/subject/26810318/comments' +
                    url} for url in body.xpath('//*[@id="paginator"]/a/@href')]
        else:
            urls = [{'url': 'https://movie.douban.com/subject/26810318/comments' +
                    url} for url in body.xpath('//*[@id="paginator"]/a[3]/@href')]

        return urls

    Data解析函数实现

    >>>
    def getdata(response):
        body = html.fromstring(response['text'])
        comments = body.xpath('//*[@id="comments"]/div/div[2]/p/span/text()')
        writter.write_buffer([comments])

    main函数实现, level表示可深入URL的层级，以下是通过网页深度抓取，所以可以for i in range(1,100,20)来模拟6个初始网页进行抓取，也可以只提供第一个URL，然后设置level为6进行深度抓取

    >>>
    if __name__ == '__main__':
        requests = []
        for i in range(0, 100, 20):
            requests.append({
                'url': 'https://movie.douban.com/subject/26810318/comments?start={}&limit=20&sort=new_score&status=P'.format(i)
            })
        spider = Spider(requests,
                        getUrl_func=geturl, getData_func=getdata, level=1)
        spider.start_multiThread_crawl(4)
    '''