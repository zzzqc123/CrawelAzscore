# -*- coding: utf-8 -*-

import pymysql
from twisted.enterprise import adbapi


class AzscoreTwistedPipeline(object):
    def __init__(self, host, user, password, db):
        params = dict(
            host=host,
            user=user,
            password=password,
            db=db,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )
        # 使用Twisted中的adbapi获取数据库连接池对象
        self.dbpool = adbapi.ConnectionPool('pymysql', **params)

    @classmethod
    def from_crawler(cls, crawler):
        # 获取settings文件中的配置
        host = crawler.settings.get('HOST')
        user = crawler.settings.get('USER')
        password = crawler.settings.get('PASSWORD')
        db = crawler.settings.get('DB')
        return cls(host, user, password, db)

    def process_item(self, item, spider):
        # 使用数据库连接池对象进行数据库操作,自动传递cursor对象到第一个参数
        query = self.dbpool.runInteraction(self.do_insert, item)
        print(f'正在插入/更新 {item["tournament"]} 联赛赛程的数据...')
        # 设置出错时的回调方法,自动传递出错消息对象failure到第一个参数
        query.addErrback(self.on_error, spider)
        return item

    def do_insert(self, cursor, item):
        source, sport, region, tour, home, away, begin_time = item["dataSourceCode"], item["sportName"], item["regionName"], item["tournament"], item["home"],item["away"], item["beginTime"]

        sql = f'''insert into match_schedule(id,source,sport,region,tour,home,away,begin_time) 
        values((SELECT id FROM match_schedule AS m WHERE m.source='{source}' 
        AND m.sport='{sport}'
        AND m.region='{region}'
        AND m.tour='{tour}' 
        AND m.home='{home}'
        AND m.away='{away}'
        AND m.begin_time={begin_time}),
        '{source}','{sport}','{region}','{tour}','{home}','{away}',{begin_time}) 
        ON DUPLICATE KEY UPDATE insert_time=NOW()
        '''

        cursor.execute(sql)

    def on_error(self, failure, spider):
        spider.logger.error(failure)
