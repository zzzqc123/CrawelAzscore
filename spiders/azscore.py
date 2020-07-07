# -*- coding: utf-8 -*-
import time
import scrapy
import random
from pprint import pprint
from Azscore.items import AzscoreItem


class AzscoreSpider(scrapy.Spider):
    name = 'azscore'
    allowed_domains = ['azscore.com']
    start_urls = ['https://www.azscore.com/']

    def parse(self, response):
        all_url = []
        urls = response.xpath('//section[@class="section--left"]/ul/li/ul')
        for ulx in urls[:-8]:
            # time.sleep(random.random())
            uls = ulx.xpath('./li/a/@href').extract()
            # pprint(uls)
            for ul in uls:
                url = f"https://azscore.com{ul}/fixtures"
                # print(url)
                all_url.append(url)

        print(f'{"-" * 20}共{len(all_url)}个联赛地址{"-" * 20}')

        for url2 in all_url:
            # time.sleep(random.random())
            yield scrapy.Request(url2, callback=self.parse_results)

    def parse_results(self, response):
        region = response.xpath('//div[@class="league-info__value"]/text()').extract_first()
        # print(region)

        tournament = response.xpath('//h4[@class="v-text v-text--h4"]/text()').extract_first()
        # print(f"{tournament} \n {'-'*100}")

        base_node = response.xpath('//ul[@class="match-status match-status--cards-floated"]/li')
        if base_node:
            for node in base_node:
                item = AzscoreItem()
                item["sportName"] = "Soccer"
                item["dataSourceCode"] = "azscore"
                item["regionName"] = region
                item["tournament"] = tournament
                item["home"] = node.xpath('./a/span[1]/span[2]/text()').extract_first()
                item["away"] = node.xpath('./a/span[2]/span[2]/text()').extract_first()

                t1 = node.xpath('./div/span[1]/span/text()').extract_first().strip()
                t2 = node.xpath('./div/span[2]/span/text()').extract_first().strip()
                d, m, y = t1.split("/")
                # 合并时间
                dt = f"20{y}-{m}-{d} {t2}:00"
                # 时间数组
                timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
                # 13位的时间戳
                item["beginTime"] = int(time.mktime(timeArray)) * 1000

                # print(item["dataSourceCode"], item["sportName"], item["regionName"], item["tournament"], item["home"],
                #       item["away"], item["beginTime"])
                yield item

        else:
            print(f"{'-'*10}此{tournament}联赛暂没新赛程{'-'*9}->{response.url}")
