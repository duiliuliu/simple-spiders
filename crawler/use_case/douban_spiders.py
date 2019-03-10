# -*- coding： utf-8 -*-
# author：pengr

def 简单示例():
    '''
    simple-spiders实战小案例
    本篇案列带你完成下列任务：

        1. 创建一个simple-spiders项目

        2. 编写爬取网站的spider

        3. 存储爬取到的数据

    首先我们创建简单的simple-spider项目，创建一个spiders.py(文件命名随意)

        '引入我们需要的库'

        >>> from crawler.spider import Spider

        >>> from crawler.writter import DataWriter

        '创建爬虫'

        >>> spider = Spider(
            'https://movie.douban.com/subject/26810318/comments?start=0&limit=20&sort=new_score&status=P')
        
        >>> spider.start_crawl()
        
        这样我们就通过simple-spiders 简单建立了一个爬虫

    通常，对于所有爬取的数据我们是有所甄别的，而且也并不是获取所有网站中的URL再次进行爬取
    而是对于特定的URL，添加进队列。这个时候，我们可以自定义解析URL的函数与解析数据的函数，然后传入spider()中

    如：
    '''

def 自定义解析函数示例():
    '''
    导入库

    >>>
     from crawler.spider import Spider
     from crawler.writter import DataWriter
     from lxml import html

    创建写入对象

    >>>
     writter = DataWriter('data.txt')

    自定义URL解析

    >>>
     def geturl(response):
         #自定义URL解析函数，对下一页的URL进行提取。观察网站结构可以看出：
         #    首页与其他页的下一页不是同一个xpath路径，根据不同的网络层级进行解析
         body = html.fromstring(response['text'])
         if response['level'] == 1:
             urls = [{'url': 'https://movie.douban.com/subject/26810318/comments' +
                     url} for url in body.xpath('//*[@id="paginator"]/a/@href')]
         else:
             urls = [{'url': 'https://movie.douban.com/subject/26810318/comments' +
                     url} for url in body.xpath('//*[@id="paginator"]/a[3]/@href')]
         return urls

    自定义Data解析

    >>>
     def getdata(response):
        #自定义data解析函数，对我们所需要的数据进行提取。
        body = html.fromstring(response['text'])
        comments = body.xpath('//*[@id="comments"]/div/div[2]/p/span/text()')
        writter.write_buffer([comments])


    进行构建spider,传入我们自定义的解析函数进行解析
    level表示可深入URL的层级，以下是通过网页深度抓取，所以可以for i in range(1,100,20)来模拟6个初始网页进行抓取，也可以只提供第一个URL，然后设置level为6进行深度抓取
    
    >>> 
     spider = Spider(
         'https://movie.douban.com/subject/26810318/comments?start=0&limit=20&sort=new_score&status=P',
         getUrl_func=geturl, getData_func=getdata, level=6)
     spider.start_crawl()

    '''

    
