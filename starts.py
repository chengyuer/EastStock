import  scrapy
from  scrapy import cmdline
#pycharm执行风格
# cmdline.execute(["scrapy","runspider","./example/spiders/myspider_redis.py"])

#cmdline.execute(["scrapy","crawl","ctospider"])
# cmdline.execute(["scrapy","crawl","stockSpider",'-o','ip.csv'])
cmdline.execute(["scrapy","runspider",r"D:\pythonProject\CrawlProject21\stockRedis\example\spiders\dmoz.py",'-o','stock.csv'])
#正统方法
#cookie。每链接一次，TCP 断开,再链接不行。
#selenium登陆，保持会话，