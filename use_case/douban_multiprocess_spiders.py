# -*- coding： utf-8 -*-
# author：pengr

import sys
sys.path.append('..')

from crawler.spider import Spider
from crawler.writter import DataWriter
from lxml import html


writter = DataWriter('data_multi_process.txt')


def geturl(response):
    body = html.fromstring(response['text'])
    if response['level'] == 1:
        urls = [{'url': 'https://movie.douban.com/subject/26810318/comments' +
                 url} for url in body.xpath('//*[@id="paginator"]/a/@href')]
    else:
        urls = [{'url': 'https://movie.douban.com/subject/26810318/comments' +
                 url} for url in body.xpath('//*[@id="paginator"]/a[3]/@href')]

    return urls


def getdata(response):
    body = html.fromstring(response['text'])
    comments = body.xpath('//*[@id="comments"]/div/div[2]/p/span/text()')
    writter.write_buffer([comments])


if __name__ == '__main__':
    requests = []
    for i in range(0, 100, 20):
        requests.append({
            'url': 'https://movie.douban.com/subject/26810318/comments?start={}&limit=20&sort=new_score&status=P'.format(i)
        })
    spider = Spider(requests,
                    getUrl_func=geturl, getData_func=getdata, level=6)
    spider.start_multiProcess_crawl(4)
