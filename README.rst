simple Spider
=============

| |python -> 3.4+|
| |coverage -> 37%|
| |build -> passing|

::

          _                 _         _____       _     _           
         (_)               | |       / ____|     (_)   | |          
      ___ _ _ __ ___  _ __ | | ___  | (___  _ __  _  __| | ___ _ __ 
     / __| | '_ ` _ \| '_ \| |/ _ \  \___ \| '_ \| |/ _` |/ _ \ '__|
     \__ \ | | | | | | |_) | |  __/  ____) | |_) | | (_| |  __/ |   
     |___/_|_| |_| |_| .__/|_|\___| |_____/| .__/|_|\__,_|\___|_|   
                     | |                   | |                      
                     |_|                   |_|                      

`中文 <./Readme-zh.md>`__

Overview
--------

A simple web crawling
framework.\ `Document <https://duiliuliu.github.io/simple-spiders/>`__

Getting Started
---------------

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

Referenced Libraries
--------------------

-  Using `requests <https://github.com/requests/requests>`__ as
   htmlDownloader
-  Using `lxml <https://github.com/lxml/lxml>`__ as default htmlParser
-  Using `csv <http://www.python-csv.org>`__ provide feature that export
   file as csv type
-  Using `xlwt <http://www.python-excel.org/>`__ provide feature that
   export file as excel type
-  Using `xlsxwriter <https://xlsxwriter.readthedocs.io>`__ provide
   feature that export file as xexcel type

Usage
-----

Project structure
-----------------

::

    - crawler/
        - __init__.py
        - test/
          - htmlDownloder_test
          - htmlParser_test
          - requestManager_test
          - writter_test
          - logger_test
          - spider_test
          
        - htmlDownloder
        - htmlParser
        - requestManager
        - writter
        - logger
        - spider

    - main.py

License
-------

This project is published open source under [|license|\ ] agreement.
Please maintain the open source release after modification and sign the
name of the original author. Thank you for your respect

If you need to apply this project for commercial purposes, please
contact me( `@pengr <https://github.com/duiliuliu>`__ ) separately to
obtain commercial authorization

.. |python -> 3.4+| image:: ./images/python-3.4+-green.svg
.. |coverage -> 37%| image:: https://img.shields.io/badge/coverage-37%25-yellowgreen.svg
.. |build -> passing| image:: ./images/build-passing-orange.svg
.. |license| image:: ./images/license-LGPL--3.0-orange.svg
