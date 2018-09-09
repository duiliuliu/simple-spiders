# -*- coding： utf-8 -*-
# author：pengr

import sys
sys.path.append('..')

from crawler.spider import Spider
from crawler.writter import DataWriter
from lxml import html


writter = DataWriter('data.txt')


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
    spider = Spider(
        'https://movie.douban.com/subject/26810318/comments?start=0&limit=20&sort=new_score&status=P',
        getUrl_func=geturl, getData_func=getdata, level=6)
    spider.start_crawl()
