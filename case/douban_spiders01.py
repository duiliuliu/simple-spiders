from crawler.spider import Spider
from crawler.writter import DataWriter
from lxml import html


spider = Spider(
    'https://movie.douban.com/subject/26810318/comments?start=0&limit=20&sort=new_score&status=P')
spider.start_crawl()
