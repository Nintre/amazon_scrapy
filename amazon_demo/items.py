# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonDemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_title = scrapy.Field()
    product_asin = scrapy.Field()
    product_url = scrapy.Field()
    product_price = scrapy.Field()
    product_star = scrapy.Field()
    product_ratings = scrapy.Field()
    product_pic = scrapy.Field()
    product_sold_by_name = scrapy.Field()
    product_sold_by_url = scrapy.Field()
    product_category = scrapy.Field()
    product_overview = scrapy.Field()
    product_about_this_item = scrapy.Field()
    product_description = scrapy.Field()
    product_details = scrapy.Field()
    product_top_reviews = scrapy.Field()

    seller_name = scrapy.Field()
    seller_add = scrapy.Field()
    seller_country = scrapy.Field()
    seller_url = scrapy.Field()
    seller_id = scrapy.Field()
    seller_good_comment = scrapy.Field()
    seller_mid_comment = scrapy.Field()
    seller_bad_comment = scrapy.Field()
    seller_count_comment = scrapy.Field()
    seller_storefront_name = scrapy.Field()
    seller_storefront_id = scrapy.Field()
    seller_marketplace_id = scrapy.Field()
    seller_storefront_url = scrapy.Field()

    has_seller = scrapy.Field()





