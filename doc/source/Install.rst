安装使用
=================

``pip install simple-spiders``

You should construst project.py to suit your needs

::

    from crawler.spider import Spider
    from crawler.writter import DataWriter

    spider = Spider(
        'https://movie.douban.com/subject/26810318/comments?start=0&limit=20&sort=new_score&status=P')
    spider.start_crawl()

``python project.py``

``Ctrl-C to stop``