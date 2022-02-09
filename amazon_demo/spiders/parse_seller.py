import re

from bs4 import BeautifulSoup


def get_business_name_add_country(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        business_detail = soup.select('ul > li > span')
        business_name = business_detail[0].get_text()
        business_add = business_detail[1].get_text(',')
        seller_country = business_add[-2:]

        # 去除冗余
        seller_name = business_name.replace('Business Name:', '')
        seller_add = business_add.replace('Business Address:,', '')

        return seller_name, seller_add, seller_country
    except Exception as e:
        print('get_business_name_add_country错误: %s' % e)


def get_business_id_url(sold_by_url):
    try:
        sold_by_id = sold_by_url.replace('https://www.amazon.com/sp?seller=', '')
        return sold_by_url, sold_by_id
    except Exception as e:
        print('get_business_id_url错误: %s' % e)


def get_business_comment(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        # 选取出好评中评差评和计数四部分，#表示的意思是id，.表示的是class
        comment = soup.select('#feedback-summary-table')

        if not comment:
            # 一般来说进去了卖家页面，公司和公司地址是有的
            return '', '', '', ''

        # 再取出包含<span>标签的数据
        comments = comment[0].select("tr > td > span")

        # 将tag类型转换为str
        paragraphs = []
        for x in comments:
            paragraphs.append(str(x))
        # 将list[str]转换为str然后用正则取出数据
        paragraphs1 = ','.join(paragraphs)
        comments_data = re.findall('>(.*?)</span>', paragraphs1)

        # 切片取出各自数据
        good_comment = comments_data[0:4]
        mid_comment = comments_data[4:8]
        bad_comment = comments_data[8:12]
        count_comment = comments_data[12:16]

        # 转化为正常的格式
        good_comment = list_2_str(good_comment)
        mid_comment = list_2_str(mid_comment)
        bad_comment = list_2_str(bad_comment)
        count_comment = delete_comma(count_comment)
        count_comment = list_2_str(count_comment)

        return good_comment, mid_comment, bad_comment, count_comment
    except Exception as e:
        print('get_business_comment错误: %s' % e)


def list_2_str(lt):
    return ','.join(lt)


def delete_comma(lt):
    new_lt = []
    for k in lt:
        new_k = k.replace(',', '')
        new_lt.append(new_k)
    return new_lt


def get_business_storefront(html):
    try:
        # 获取商家店面链接，名字，id
        business_storefront = re.findall('href="(.*?)">(.*?) storefront</a>', html)
        if business_storefront is None:
            business_storefront = re.findall('href="(.*?)">(.*?) 店铺</a>', html)

        business_storefront = business_storefront[0]
        business_storefront_url = business_storefront[0]
        business_storefront_id = re.findall('me=(.*)', business_storefront_url)[0]
        marketplace_id = re.findall('marketplaceID=(.*?)&', business_storefront_url)[0]
        business_storefront_name = business_storefront[1]

        return business_storefront_name, business_storefront_id, marketplace_id, business_storefront_url
    except Exception as e:
        print('get_business_storefront错误: %s' % e)

