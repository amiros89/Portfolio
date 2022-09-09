from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium import webdriver
from datetime import datetime
from classes import Result,EbayItem
import os
from amazoncaptcha import AmazonCaptcha
import time
import requests
from consts import KEEPALIVE_INTERVAL,LOCAL_RUN

def initialize_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--enable-javascript")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-dev-shm-usage")
    if LOCAL_RUN:
        chrome_options.add_argument('--headless')
    chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_PATH')
    driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), chrome_options=chrome_options)

    return driver

def send_keep_alive(last_keepalive,logger):
    if not LOCAL_RUN:
        now = time.time()
        delta = (now - last_keepalive) / 60
        if delta > KEEPALIVE_INTERVAL:
            logger.info(f"Pinging app after {KEEPALIVE_INTERVAL} minutes since last web activity")
            try:
                requests.get("https://elocator.herokuapp.com/")
            except Exception as e:
                logger.warning(f"Could not get response from app: {e}")
                return False
            return True
    return False

def get_ebay_items(amazon_products, driver,logger):
    driver = driver
    logger.info("eBay scraper initialized")
    amazon_titles = amazon_products.keys()
    now = datetime.now()
    # prods = {}
    results = []
    for amazon_title in amazon_titles:  # for each of the title returned from get_amazon_items method, search for the title in ebay
        try:
            # candidates = {}
            driver.get("http://www.ebay.com")
            driver.find_element_by_id("gh-ac").send_keys(amazon_title)
            driver.find_element_by_id("gh-btn").click()
            # no_results = '//*[@id="s0-14-11-6-3-save_search1-answer-17"]/div[1]/h3'
            # if driver.find_elements_by_xpath(no_results):
            #     logger.info(msg=f"Found no results on eBay for {amazon_title}")
            #     continue
            ebay_links_elems = driver.find_elements_by_class_name("s-item__link")
            ebay_links = []
            for i in range(2, 12):  # hardcoded as per Sapir's request - look for the 10 first items in the page
                try:
                    if len(ebay_links_elems[i].text) > 0:
                        ebay_links.append(ebay_links_elems[i].get_attribute("href"))  # build a list of their links
                except:
                    logger.warning("Unknown error when parsing hrefs")
                    continue
            for link in ebay_links:  # for each of the links in the list built in the previous foor loop, check the sales table
                sales_in_last_month = 0
                sold_in_last_month = False
                sold_in_last_week = False
                driver.get(link)
                try:
                    ebay_title = driver.find_element_by_id("itemTitle").text
                    sold = driver.find_element_by_class_name("vi-txt-underline")
                    sold.click()
                    table_header = driver.find_elements_by_xpath(
                        f"/html/body/div[4]/div[1]/div[2]/table/tr[1]/th[4]/span/span")
                    try:
                        if table_header.pop().text != "Date of purchase":
                            td = "td[5]"
                        else:
                            td = "td[4]"
                        diff = 0
                        row = 2
                        while diff <= 30:
                            try:
                                date = driver.find_elements_by_xpath(
                                    f"/html/body/div[4]/div[1]/div[2]/table/tr[{row}]/{td}/div/span/span")
                            except:
                                date = driver.find_elements_by_xpath(
                                    f"/html/body/div[4]/div[1]/div[2]/table/tr[{row}]/{td}/span/span")
                            try:
                                datetimestr = date.pop().text[0:-6]
                            except IndexError:
                                logger.warning(
                                    "Could not parse date time string, exiting from sales in last month query and moving on.")
                                continue
                            timestr = datetimestr.replace(' at', '')
                            date_time_obj = datetime.strptime(timestr, '%d %b %Y %H:%M:%S')
                            diff = (now - date_time_obj).days
                            if diff > 30:
                                break
                            if diff < 7:
                                sold_in_last_week = True
                            if diff < 30:
                                sales_in_last_month += 1
                            if sales_in_last_month >= 5:
                                sold_in_last_month = True
                            row += 1
                    except IndexError:
                        logger.warning("Could not find Date of Purchase text in item sales tables, moving on...")
                        continue
                    if sold_in_last_month and sold_in_last_week:  # if the item matches the hot item criteria, create a result object with its detail and append it to the results list
                        # candidates[ebay_title] = sales_in_last_month
                        # add item to candidates dictionary with the number of sales in last 30 days
                        # find number of sales by iterating over table rows with date <= 30 days before current date
                        # add the value in Quantity column to the dictionary key value
                        # iterate over candidates dictionary values to find the one with the highest number of sales
                        # add the winning candidate to the final results
                        # logger.info(
                        #     f"Found product that meets the criteria: {ebay_title}:{amazon_title},{amazon_products.get(amazon_title)}")
                        result = Result(ebay_url=link, ebay_title=ebay_title, amazon_title=amazon_title,
                                        amazon_asin=amazon_products.get((amazon_title)))
                        results.append(result)
                        logger.info("Found new result and added to results objects list")
                except NoSuchElementException:
                    logger.warning("Could not find eBay title element")
                    continue
            # if candidates: # irrelevant, we don't want to look for the top seller
            #     top_seller = ""
            #     sales = list(candidates.values())
            #     sales.sort()
            #     top_seller_sales = sales[-1]
            #     for key, value in candidates.items():
            #         if top_seller_sales == value:
            #             top_seller = key
            #     prods[top_seller] = {amazon_title: amazon_products.get(amazon_title)}
        except WebDriverException:
            logger.error("Driver crashed, restarting.")
            driver = initialize_driver()
            continue
    return results

def get_amazon_items(url, driver,logger):  # get unique asins from the provided link and number of pages
    hrefs = []
    titles = []
    asins = []
    products = {}
    # TODO wrap this block as utility method - get links from amazon page
    for i in range(1, 1 + 1):
        logger.info(f"Started scraping page number {i}")
        url = f"{url}&page={i}"
        driver.get(url)
        links = driver.find_elements_by_tag_name("a")
        if len(links) <= 3:
            logger.info("Got to Captcha page, solving...")
            captcha = AmazonCaptcha.fromdriver(driver)
            solution = captcha.solve()
            time.sleep(2)
            try:
                elem = driver.find_element_by_xpath('//*[@id="captchacharacters"]')
                logger.info("Captcha element found, sending solution")
                elem.send_keys(solution)
                driver.find_element_by_xpath(
                    '/html/body/div/div[1]/div[3]/div/div/form/div[2]/div/span/span/button').click()
            except:
                logger.error("Failed to found Captcha element, refreshing...")
                driver.refresh()
        # TODO wrap this block as utiility method - get items from amazon links
        links = driver.find_elements_by_tag_name("a")
        if len(links) <= 3:
            logger.error("Scraping Amazon has failed, aborting...")
            break
        for link in links:
            href = str(link.get_attribute("href"))
            index = href.find("/dp/")
            review = href.find("customerReviews")
            from_query = href.find("qid")
            if index != -1 and review == -1 and from_query != -1:
                asin = href[index + 4:index + 14]
                if asin not in asins:
                    asins.append(asin)
                    hrefs.append(href)
        logger.info(f"Finished scraping page number {i} successfully")
    # TODO - wrap this as utility method - get unique items
    size_of_hrefs = len(hrefs)
    i = 0
    logger.info(f"Started grabbinb Amazon titles of {size_of_hrefs} products")
    while i < size_of_hrefs:
        driver.get(hrefs[i])
        try:
            product_title = driver.find_element_by_id("productTitle").text
            if len(product_title) > 79:
                product_title = str(product_title)[0:76] + '...'
            titles.append(product_title)
            i += 1
        except NoSuchElementException:
            logger.warning("Could not found product title, removing from hrefs and asins list")
            hrefs.pop(i)
            asins.pop(i)
            size_of_hrefs = size_of_hrefs - 1
            continue
    for i in range(len(asins)):
        products[titles[i]] = asins[i]
    logger.info(f"Finished scraping Amazon. found {len(products)} unique products from provided link")
    return products

def get_ebay_store_items(driver, num_of_results,logger):
    items = []
    total_items = 0
    # hardcoded to be no more than 10*200 = 2000 items
    last_keepalive = time.time()
    for i in range(10):
        results = driver.find_elements_by_class_name('sresult')
        total_items+=len(results)
        logger.info(f"Finding results, page {i+1} out of possible 10.")
        for result in results:
            if send_keep_alive(last_keepalive, logger):
                last_keepalive = time.time()
            try:
                title = result.find_element_by_class_name('vip').text
            except NoSuchElementException:
                logger.warning("Adult only item, moving on to next item.")
                continue
            href = result.find_element_by_class_name('vip').get_attribute('href')
            item = EbayItem(href=href, title=title)
            items.append(item)
            # if user selected other than 'All' we will stop here and get only num_of_results items from the store
            if num_of_results != 50 and len(items) == num_of_results:
                break
        try:
            driver.find_element_by_class_name('next').click()
        except NoSuchElementException:
            logger.info(f"Reached end of items list in store, got a total of {total_items} items, moving on to check which meet the set criteria")
            break
    return items

