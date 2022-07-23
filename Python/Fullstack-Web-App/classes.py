class Result:
    def __init__(self, ebay_title, ebay_url, amazon_title, amazon_asin,amazon_link,lifetime_sales,recent_sales):
        self.ebay_title = ebay_title
        self.ebay_url = ebay_url
        self.amazon_title = amazon_title
        self.amazon_asin = amazon_asin
        self.amazon_link = amazon_link
        self.lifetime_sales = lifetime_sales
        self.recent_sales = recent_sales

class AmazonItem:
    def __init__(self,amazon_title,amazon_asin,amazon_link):
        self.amazon_title = amazon_title
        self.amazon_asin = amazon_asin
        self.amazon_link=amazon_link

class EbayItem:
    def __init__(self, href, title="", sold=0):
        self.href = href
        self.title = title
        self.sold = sold

class Query:
    def __init__(self):
        self.sellers = []
