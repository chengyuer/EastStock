# -*- coding: utf-8 -*-
import scrapy
import lxml
import lxml.etree
from stock import items
import requests
from bs4 import BeautifulSoup
import aip
from aip import AipNlp

""" 你的 APPID AK SK """
APP_ID = '10253494'
API_KEY = 'NAh5KkgrKTPyxzUBewCAakvm'
SECRET_KEY = 'nTrHzPhh0CQP9H9Idz3jftsji9NgVdvF'

aipNlp = AipNlp(APP_ID, API_KEY, SECRET_KEY)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
}

class StockspiderSpider(scrapy.Spider):
    name = 'StockSpider3.0'
    allowed_domains = ['istock.jrj.com.cn']

    def start_requests(self):
        file = open('stockNameNum.txt')
        stocks = file.readlines()
        requestsList = []
        for stock in stocks[:5]:
            myItem = items.StockItem()
            stock = stock.replace("\n", "")
            stockList = stock.split(" # ")
            num = stockList[1]
            name = stockList[0]
            myItem['name'] = name
            myItem['num'] = num
            requestsList.append(scrapy.Request(url='http://istock.jrj.com.cn/list,'+num+',p1.html',meta={'meta':myItem},headers=headers))
        return requestsList


    def parse(self, response):
        myItem = response.meta['meta']
        myTree = lxml.etree.HTML(response.body.decode('gbk'))
        trList = myTree.xpath('//tr[@name="titlehb"]')
        sentimentScore = 0
        confidenceScore = 0
        positiveScore = 0
        negativeScore = 0
        for tr in trList:
            url = tr.xpath('./td[@class="tl"]/a/@href')[0]
            comment = self.parse_comment(url)
            comment = comment.replace("\u200b","")
            comment = comment.replace("\n","")
            comment = comment.replace("\xa0","")
            comment = comment.replace("\u4260","")
            result = aipNlp.sentimentClassify(comment)
            print(result)
            if result.get('items'):
                sentiment = result['items'][0]['sentiment']
                confidence = result['items'][0]['confidence']
                positive_prob = result['items'][0]['positive_prob']
                negative_prob = result['items'][0]['negative_prob']
                if sentiment>1:
                    sentimentScore+=1
                elif sentiment<1:
                    sentimentScore-=1
                confidenceScore+=confidence
                positiveScore+=positive_prob
                negativeScore+=negative_prob
                print('score:'+str(sentimentScore))
        myItem['sentimentScore'] = sentimentScore
        myItem['confidenceScore'] = confidenceScore/len(trList)
        myItem['positiveScore'] = positiveScore/len(trList)
        myItem['negativeScore'] = negativeScore/len(trList)
        yield myItem


    def parse_comment(self,url):
        html = requests.get(url, headers=headers).content
        soup = BeautifulSoup(html.decode('gbk'), 'html5lib')
        mainDiv = soup.find('div', class_='main')
        comment = mainDiv.find('div').get_text()
        return comment

