# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from twisted.enterprise import adbapi
import config
from ITcast.models.tencent import Tencent


class ItcastPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'itcast':
            print(spider.name)
        return item


class TencentMysqlCreateTableAndSavePipeline(object):  # 创建 MySQL 数据表 article（且将数据保存至数据库表）
    def __init__(self):
        self.engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=True)
        base = declarative_base()
        self.Article = type('article', (base, Tencent), {'__tablename__': 'article'})
        # type(name, (object), dict):
        # 该方法可以自动创建新的类，类名为 name，继承自 object，类属性存放在 dict 中，可以指定各种属性
        base.metadata.create_all(self.engine)  # 使用 sqlalchemy orm 的方式自动创建数据表

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def process_item(self, item, spider):
        """
        向数据表中添加文章
        :param item:
        :param spider:
        :return: item
        """
        # 当前 item 中有一个字段为 list，不符合数据库对应字段类的要求
        # 插入mysql数据库的字段必须是数据库内对应字段的类型，否则会报错，所以在这里将1个（字符串的）列表类型转为字符串类型
        # 因为之前下载封面图的时候 scrapy 内部需要 cover_img_url 为 list，所以将其转为了 list，现在再转换回 str
        try:
            item['cover_img_url'] = item['cover_img_url'][0]
            item['content'] = str(item['content'])
            #
            self.session.add(self.Article(**item))
            self.session.commit()
        except Exception as e:
            with open('error_log.txt', 'w') as f:
                f.write(str(e))
                f.write(str(item))
            self.session.rollback()  # 防止出错所以进行预防性的回滚
            raise e
        return item

    def spider_closed(self, spider):
        self.session.close()


class TencentMysqlPipeline(object):
    """
    采用同步机制写入 MySQL
    缺点：当爬取速度超过 MySQL 写入速度的时候会造成阻塞
    """

    def __init__(self):
        self.conn = pymysql.connect(user=config.USER, password=config.PASSWORD, host=config.HOST, port=config.PORT,
                                    database=config.DATABASE, charset=config.CHARSET, use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if spider.name == 'tencent':
            insert_sql = """
            insert into positon(id, post_id, recruit_post_id, recruit_post_name, country_name, location_name, bg_name,
            product_name, category_name, responsibility, last_update_time, post_url,source_id,is_collect,is_valid) VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(insert_sql,
                                (item['id'], item['post_id'], item['recruit_post_id'], item['recruit_post_name'],
                                 item['country_name'], item['location_name'], item['bg_name'], item['product_name'],
                                 item['category_name'], item['responsibility'], item['last_update_time'],
                                 item['post_url'], item['is_collect'], item['is_valid']))
            self.conn.commit()
        return item


class TencentMySQLTwistedPipeline(object):
    """
    采用异步机制写入 MySQL:暂时会造成数据丢失，未解决
    """

    def __init__(self, db_pool):
        self.db_pool = db_pool

    def process_item(self, item, spider):  # 使用 twisted 将 mysql 的插入变成异步执行
        if spider.name == 'tencent':
            print(spider.name)
            query = self.db_pool.runInteraction(self.do_insert, item)
            query.addErrback(self.handle_error, item, spider)  # item、spider 可传可不传
        return item

    @classmethod
    def from_settings(cls, settings):
        db_parm = dict(host=config.HOST, db=config.DATABASE, user=config.USER, passwd=config.PASSWORD,
                       charset=config.CHARSET, cursorclass=MySQLdb.cursors.DictCursor, use_unicode=True)
        db_pool = adbapi.ConnectionPool("MySQLdb", **db_parm)
        return cls(db_pool)

    def handle_error(self, failure, item, spider):  # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):  # 执行具体的插入
        item['cover_img_url'] = item['cover_img_url'][0]
        insert_sql = """
                        insert into tencent(url, url_object_id, title, cover_img_url, cover_img_url_path, create_time, praise_nums, 
                        fav_nums, comment_nums, content, copyright_area, tags) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
        cursor.execute(insert_sql, (item['url'], item['url_object_id'], item['title'], item['cover_img_url'],
                                    item['cover_img_url_path'], item['create_time'], item['praise_nums'],
                                    item['fav_nums'], item['comment_nums'], item['content'],
                                    item['copyright_area'], item['tags']))
