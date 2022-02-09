import re
import urllib.parse

from bs4 import BeautifulSoup


def get_product_title(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        # 商品标题
        product_title = soup.find('span', id='productTitle').get_text().strip()

        return product_title
    except Exception as e:
        print('get_product_title错误: %s' % e)


def get_product_price(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        # 商品价格
        product_price = soup.find('div', id='corePrice_desktop')
        if product_price is None:
            product_price = soup.find('div', id='corePriceDisplay_desktop_feature_div').find(
                'span', class_='a-offscreen').get_text()
        else:
            product_price = product_price.find('td', class_='a-span12').find('span',
                                                                             class_='a-offscreen').get_text()

        return product_price
    except Exception as e:
        print('get_product_price错误: %s' % e)


def get_product_picture(response):
    try:
        product_price = response.xpath('//div[@id="imgTagWrapperId"]//img').css('::attr(src)').get()
        return product_price
    except Exception as e:
        print('get_product_price错误: %s' % e)


def get_product_url_asin(response):
    try:
        product_url = response.url
        product_asin = urllib.parse.urlsplit(product_url).path
        product_asin = product_asin[4:]
        return product_url, product_asin
    except Exception as e:
        print('get_product_asin错误: %s' % e)


def get_star_ratings(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        # 星star 可能搜索不到，在顶栏，特殊URL：https://www.amazon.com/dp/B07885679R
        star = soup.find('span', id='acrPopover')
        if star is None:
            star = ""
        else:
            star = star.find('a', class_='a-popover-trigger a-declarative').find('span', class_='a-icon-alt')
            star = star.get_text()
        # ratings
        ratings = soup.find('span', id='acrCustomerReviewText')
        if ratings is None:
            ratings = ""
        else:
            ratings = ratings.get_text()

        return star, ratings
    except Exception as e:
        print('get_star_ratings错误: %s' % e)


def get_sold_by_name_url_id(response):
    try:
        product_sold_by_name = response.xpath('//a[@id="sellerProfileTriggerId"]/text()').get()
        product_sold_by_url = response.xpath('//a[@id="sellerProfileTriggerId"]').css('::attr(href)').get()
        product_sold_by_id = get_product_sold_by_id(product_sold_by_url)
        return product_sold_by_name, product_sold_by_url, product_sold_by_id
    except Exception as e:
        print('get_sold_by_name_url错误: %s' % e)


def get_product_sold_by_id(product_sold_by_url):
    try:
        if product_sold_by_url:
            seller_id = re.findall('seller=(.*?)&', product_sold_by_url)[0]
            return seller_id
        else:
            return ''
    except Exception as e:
        print('get_product_sold_by_id错误: %s' % e)


def get_product_category(response):
    try:
        category_main_list = response.xpath('//ul[@class="a-unordered-list a-horizontal a-size-small"]//a[@class="a-link-normal a-color-tertiary"]/text()').getall()
        category_list = []
        for c in category_main_list:
            c = c.strip()
            category_list.append(c)
        product_category = ','.join(category_list)
        return product_category
    except Exception as e:
        print('get_product_category错误: %s' % e)


def get_product_attribute(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        # 商品属性
        product_attribute_origin = soup.find('div', id='productOverview_feature_div').find('table',
                                                                                           class_='a-normal a-spacing-micro')
        if product_attribute_origin is None:
            product_attribute = ''
        else:
            product_attribute_origin = product_attribute_origin.find_all('span', class_='a-size-base')
            product_attribute_li = []
            for item in product_attribute_origin:
                item = item.get_text().strip()
                product_attribute_li.append(item)
            product_attribute = {}
            for i in range(len(product_attribute_li) - 1):
                if i % 2 == 0:
                    product_attribute[product_attribute_li[i]] = product_attribute_li[i + 1]

            product_attribute = str(product_attribute)
        return product_attribute
    except Exception as e:
        print('get_product_attribute错误: %s' % e)


def get_product_about_this_item(response):
    try:
        product_about_this_item = []
        product_about_this_item_list = response.xpath(
            '//ul[@class="a-unordered-list a-vertical a-spacing-mini"]//span[@class="a-list-item"]/text()').getall()
        for a in product_about_this_item_list:
            if a == ' ' or a == '\n':
                continue
            a.strip()
            product_about_this_item.append(a)
        product_about_this_item = ','.join(product_about_this_item)
        return product_about_this_item
    except Exception as e:
        print('get_product_about_this_item错误: %s' % e)


def get_product_description(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        # product_description
        product_description = soup.find('div', id='productDescription')
        if product_description is None:
            product_description = ''
        else:
            product_description = product_description.get_text().replace('\n', '')
        return product_description
    except Exception as e:
        print('get_product_description错误: %s' % e)


def get_product_details_table(html1):
    try:
        soup = BeautifulSoup(html1, "html.parser")
        details_origin = soup.find('div', id='detailBullets_feature_div')
        if details_origin is None:
            product_details = ''
        else:
            product_details = details_origin.find_all('span', class_='a-list-item')
            product_details_list = []
            for item in product_details:
                item = item.get_text().replace('\n', '').strip().replace(' ', '')
                product_details_list.append(item)
            product_details = ' || '.join(product_details_list)
        return product_details

    except Exception as e:
        print('get_product_details_table错误: %s' % e)


def get_product_information_table(html1, details):
    try:
        if details is not None:
            return details
        soup = BeautifulSoup(html1, "html.parser")
        details_origin = soup.find('table', id='productDetails_techSpec_section_1')
        details_origin1 = soup.find('table', id='productDetails_detailBullets_sections1')
        if details_origin and details_origin1 is None:
            product_details = ''
        else:
            if details_origin is None:
                details_origin = details_origin1
            product_details_key = details_origin.find_all('th')
            product_details_value = details_origin.find_all('td')
            product_details_key_value = {}
            for i in range(len(product_details_key)):
                key = product_details_key[i].get_text().replace('\n', '').strip()
                value = product_details_value[i].get_text().replace('\n', '').strip()
                product_details_key_value.update({key: value})
            product_details = str(product_details_key_value)
        return product_details

    except Exception as e:
        print('get_product_information_table错误: %s' % e)


def get_top_reviews(html1):
    try:
        soup = BeautifulSoup(html1, "html.parser")
        top_reviews_origin = soup.find('div', id='cm-cr-dp-review-list')
        if top_reviews_origin is None:
            top_reviews = ''
        else:
            top_reviews_origin = top_reviews_origin.find_all('div', class_='a-section celwidget')
            top_reviews_list = []
            for item in top_reviews_origin:
                item = item.get_text().replace('\n', '').strip()
                top_reviews_list.append(item)
            top_reviews = ' || '.join(top_reviews_list)
        return top_reviews

    except Exception as e:
        print('get_top_reviews错误: %s' % e)

