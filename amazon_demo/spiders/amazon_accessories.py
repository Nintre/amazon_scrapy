import scrapy

from amazon_demo.items import AmazonDemoItem

from amazon_demo.spiders.parse_product import get_product_title, get_product_price, get_product_picture, \
    get_product_url_asin, get_star_ratings, get_sold_by_name_url_id, get_product_category, get_product_attribute, \
    get_product_about_this_item, get_product_description, get_product_details_table, get_product_information_table, get_top_reviews

from amazon_demo.spiders.parse_seller import get_business_name_add_country, get_business_id_url, get_business_comment, get_business_storefront


class AmazonAccessoriesSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['www.amazon.com']
    start_urls = ['https://www.amazon.com/s?i=electronics-intl-ship&amp;bbn=16225009011&amp;rh=n%3A281407%2Cn%3A172532&amp;dc&amp;qid=1642677859&amp;rnid=281407&amp;ref=sr_nr_n_1']
    p = 1

    # def start_requests(self):
    #     yield scrapy.Request('https://www.amazon.com/s?rh=n%3A172532&fs=true&page=1&ref=sr_pg_1', self.my_parse)

    def parse(self, response, **kwargs):
        print('====第%d页' % self.p)
        print(response.url)
        print(response.status)

        verification = response.xpath('//div[@class="a-box a-color-offset-background"]//form')
        if verification is not None:
            yield scrapy.Request(url=response.url, callback=self.parse)

        page_size = response.xpath('//span[@class="s-pagination-item s-pagination-disabled"]/text()').get()
        page_size = int(page_size)
        print("page_size", page_size)

        asin_list = response.xpath('//div[@class="s-main-slot s-result-list s-search-results sg-row"]//div[@data-asin]')

        for i in range(len(asin_list)):
            asin = asin_list[i].css('::attr(data-asin)').get()
            if asin != '':
                print(asin)
                product_url = 'https://www.amazon.com/dp/' + asin
                yield scrapy.Request(url=product_url, callback=self.product_parse)

        self.p += 1
        # < 11 是爬取10页内容
        if self.p < (page_size + 1):
            next_url = 'https://www.amazon.com/s?rh=n%3A172532&fs=true' + '&page=' + str(self.p) + '&ref=sr_pg_' + str(
                self.p)
            yield scrapy.Request(url=next_url, callback=self.parse)

    def product_parse(self, response):
        print("商品url:", response.url)
        print(response.status)

        item = AmazonDemoItem()

        product_title = get_product_title(response.text)
        item['product_title'] = product_title

        product_price = get_product_price(response.text)
        item['product_price'] = product_price

        product_pic = get_product_picture(response)
        item['product_pic'] = product_pic

        product_url, product_asin = get_product_url_asin(response)
        item['product_url'] = product_url
        item['product_asin'] = product_asin

        (star, ratings) = get_star_ratings(response.text)
        item['product_star'] = star
        item['product_ratings'] = ratings

        product_sold_by_name, product_sold_by_url, product_sold_by_id = get_sold_by_name_url_id(response)
        item['product_sold_by_name'] = product_sold_by_name
        item['product_sold_by_url'] = product_sold_by_url

        product_category = get_product_category(response)
        item['product_category'] = product_category

        product_overview = get_product_attribute(response.text)
        item['product_overview'] = str(product_overview)

        product_about_this_item = get_product_about_this_item(response)
        item['product_about_this_item'] = product_about_this_item

        product_description = get_product_description(response.text)
        item['product_description'] = product_description

        product_details = get_product_details_table(response.text)
        product_details = get_product_information_table(response.text, product_details)
        item['product_details'] = product_details

        product_top_reviews = get_top_reviews(response.text)
        item['product_top_reviews'] = product_top_reviews

        if product_sold_by_id != '':
            item['has_seller'] = 1
            seller_url = 'https://www.amazon.com/sp?' + 'seller=' + product_sold_by_id
            yield scrapy.Request(url=seller_url, callback=self.seller_parse, meta={'item': item})
        else:
            item['has_seller'] = 0
            yield item

    def seller_parse(self, response):
        print("商家url:", response.url)
        print(response.status)

        item = response.meta['item']

        seller_name, seller_add, seller_country = get_business_name_add_country(response.text)
        item['seller_name'] = seller_name
        item['seller_add'] = seller_add
        item['seller_country'] = seller_country

        seller_url, seller_id = get_business_id_url(response.url)
        item['seller_url'] = seller_url
        item['seller_id'] = seller_id

        seller_good_comment, seller_mid_comment, seller_bad_comment, seller_count_comment = get_business_comment(
            response.text)
        item['seller_good_comment'] = seller_good_comment
        item['seller_mid_comment'] = seller_mid_comment
        item['seller_bad_comment'] = seller_bad_comment
        item['seller_count_comment'] = seller_count_comment

        seller_storefront_name, seller_storefront_id, seller_marketplace_id, seller_storefront_url = get_business_storefront(
            response.text)
        item['seller_storefront_name'] = seller_storefront_name
        item['seller_storefront_id'] = seller_storefront_id
        item['seller_marketplace_id'] = seller_marketplace_id
        item['seller_storefront_url'] = seller_storefront_url

        yield item
