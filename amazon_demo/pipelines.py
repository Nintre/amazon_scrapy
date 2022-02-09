# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class AmazonDemoPipeline:
    def process_item(self, item, spider):
        return item


class MysqlPipeline:

    def __init__(self, host, user, password, database, port):
        # self.cursor = cursor
        # self.db = db
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('HOSTNAME'),
            port=crawler.settings.get('PORT'),
            database=crawler.settings.get('DATABASE'),
            user=crawler.settings.get('USERNAME'),
            password=crawler.settings.get('PASSWORD')
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database,
                                  charset='utf8mb4', port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        try:
            product_sql = "insert into `scrapy_products`(`product_title`,`product_asin`,`product_url`,`product_price`,`product_star`,`product_ratings`,`product_pic`,`product_sold_by_name`,`product_sold_by_url`,`product_category`,`product_overview`,`product_about_this_item`,`product_description`,`product_details`,`product_top_reviews`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.cursor.execute(product_sql, (
                item['product_title'], item['product_asin'], item['product_url'], item['product_price'],
                item['product_star'], item['product_ratings'], item['product_pic'], item['product_sold_by_name'],
                item['product_sold_by_url'], item['product_category'], item['product_overview'],
                item['product_about_this_item'], item['product_description'], item['product_details'],
                item['product_top_reviews']))
            self.db.commit()
        except Exception as e:
            print("product_sql insert err:", e)
            self.db.rollback()
        if item['has_seller'] == 1:
            try:
                seller_sql = "insert into `scrapy_sellers`(`seller_name`,`seller_add`,`seller_country`,`seller_url`,`seller_id`,`seller_good_comment`,`seller_mid_comment`,`seller_bad_comment`,`seller_count_comment`,`seller_storefront_name`,`seller_storefront_id`,`seller_marketplace_id`,`seller_storefront_url`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                self.cursor.execute(seller_sql,
                                    (
                                        item['seller_name'], item['seller_add'], item['seller_country'],
                                        item['seller_url'],
                                        item['seller_id'], item['seller_good_comment'], item['seller_mid_comment'],
                                        item['seller_bad_comment'],
                                        item['seller_count_comment'], item['seller_storefront_name'],
                                        item['seller_storefront_id'],
                                        item['seller_marketplace_id'], item['seller_storefront_url']))
                self.db.commit()
            except Exception as e:
                print("seller_sql insert err:", e)
                self.db.rollback()
        return item
