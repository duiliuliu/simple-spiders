from crawler.spider import Spider
from crawler.writter import DataWrite
from lxml import html


def get_url(content):
    content = html.fromstring(content)
    return {'url': link for link in content.xpath('//a/@href')}


writter = DataWrite(filename='./source/data',
                    headers=['name'], type='csv', encoding='gbk')


def get_data(content):
    content = html.fromstring(content)
    data = {}
    try:
        data['name'] = content.xpath(
            '//div[@id="artical"]/div/text()')[0].strip()
    except Exception as e:
        raise e
    writter.write_buffer(data, flush_num=100)


if __name__ == '__main__':
    start_request = {
        'url': 'http://xiushibaike',
        'request_type': 'get'
    }
    spider = Spider(start_request, getUrl_func=get_url, getData_func=get_data)
    spider.start_crawl()
