# product_title = main_list[i].xpath('.//span[@class="a-size-base-plus a-color-base a-text-normal"]/text()').get()
# product_price = main_list[i].xpath('.//span[@class="a-offscreen"]/text()').get()
# product_pic = main_list[i].xpath('.//img[@class="s-image"]').css('::attr(src)').get()

# item['product_title'] = product_title
# item['product_price'] = product_price
# item['product_pic'] = product_pic


# product_sold_by_name = response.xpath('//a[@id="sellerProfileTriggerId"]/text()').get()
# product_sold_by_url = response.xpath('//a[@id="sellerProfileTriggerId"]').css('::attr(href)').get()
# product_sold_by_id = get_product_sold_by_id(product_sold_by_url)


# item = response.meta['item']

# asin_list = response.selector.re('<div data-asin="(.*)" data-index')
# asin_list = [x.strip() for x in asin_list if x.strip() != '']

# main_list = response.xpath('//div[@class="s-expand-height s-include-content-margin s-latency-cf-section s-border-bottom s-border-top"]')

# category_main_list = response.xpath('//ul[@class="a-unordered-list a-horizontal a-size-small"]//a[@class="a-link-normal a-color-tertiary"]/text()').getall()
#         category_list = []
#         for c in category_main_list:
#             c = c.strip()
#             category_list.append(c)
#         product_category = ','.join(category_list)

'https://www.amazon.com/s?i=specialty-aps&bbn=16225009011&rh=n%3A%2116225009011%2Cn%3A281407&ref=nav_em__nav_desktop_sa_intl_accessories_and_supplies_0_2_5_2'

'https://www.amazon.com/s?i=electronics-intl-ship&bbn=16225009011&rh=n%3A281407%2Cn%3A172532&dc&qid=1642669617&rnid=281407&ref=sr_nr_n_1'
'https://www.amazon.com/s?i=electronics-intl-ship&bbn=16225009011&rh=n%3A281407%2Cn%3A172435&dc&qid=1642669617&rnid=281407&ref=sr_nr_n_2'
'https://www.amazon.com/s?i=electronics-intl-ship&bbn=16225009011&rh=n%3A281407%2Cn%3A2407755011&dc&qid=1642669617&rnid=281407&ref=sr_nr_n_3'










