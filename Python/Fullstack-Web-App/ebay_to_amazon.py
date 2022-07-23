from selenium.common.exceptions import NoSuchElementException, WebDriverException
from datetime import datetime
from utils import initialize_driver, get_ebay_store_items, send_keep_alive
from classes import Result, AmazonItem, Query
import time

NEW_CONDITION = "&rt=nc&LH_ItemCondition=3"
LOCATION_US = "&rt=nc&LH_PrefLoc=3"
GOOGLE_SEARCH = f"https://www.google.com/search?q="
AMAZON_PREFIX = 'https://www.amazon.com'
ITEMS_PER_PAGE = '&_ipg=200'
KEEPALIVE_INTERVAL = 5

def is_item_on_amazon(item_title,asins, driver, logger):
    try:
        logger.info(f"Googling item: {item_title}")
        driver.get(GOOGLE_SEARCH + item_title)
        links = driver.find_elements_by_tag_name("a")
        hrefs = [link.get_attribute('href') for link in links]
        for href in hrefs:
            if str(href).startswith(AMAZON_PREFIX):
                index = href.find("/dp/")
                if index < 0:
                    return False
                asin = href[index + 4:index + 14]
                if asin in asins:
                    logger.info(f"ASIN {asin} was already located and exists in results")
                    return False
                logger.info(f"Found item on amazon: {asin}")
                driver.get(href)
                unavailable = driver.find_elements_by_xpath("//span[contains(text(), 'Currently unavailable.')]")
                if unavailable:
                    logger.info("Item is not available on Amazon, moving on.")
                    return False
                try:
                    title = driver.find_element_by_id("productTitle").text
                except NoSuchElementException:
                    return False
                amazonItem = AmazonItem(amazon_title=title, amazon_asin=asin, amazon_link=href)
                return amazonItem
        logger.info("Could not find item on Amazon, moving on.")
        return False
    except WebDriverException as exception:
        logger.error(exception.msg)
        logger.error("Driver crashed while checking if item is on amazon, restarting and trying again")
        driver.quit()
        driver = initialize_driver()
        is_item_on_amazon(item_title, driver, logger)


def is_criteria_met(ebay_store_items, driver, settings, logger):
    results = []
    now = datetime.now()
    last_keepalive = time.time()
    for item in ebay_store_items:
        recent_sales = 0
        sold_in_recent_time = False
        sold_in_most_recent_time = False
        if send_keep_alive(last_keepalive, logger):
            last_keepalive = time.time()
        try:
            driver.get(item.href)
            try:
                sold_button = driver.find_element_by_class_name("vi-txt-underline")
                filtered_sold_string = filter(str.isdigit, sold_button.text)
                numeric_sold_string = "".join(filtered_sold_string)
                try:
                    times_sold = int(numeric_sold_string)
                except:
                    logger.warning(f"Couldn't parse times sold string: {sold_button.text} for item: {item.href}")
                    continue
                if times_sold < settings.num_of_sales_in_recent_days:
                    continue
                sold_button.click()
                table = driver.find_element_by_class_name('app-table__table')
                rows = table.find_elements_by_tag_name('tr')
                if len(rows) < settings.num_of_sales_in_recent_days + 1:
                    continue
                diff = 0
                i = 1
                while diff <= settings.num_of_days_of_recent_sales and i < len(rows):
                    row = rows[i]
                    cells = row.find_elements_by_tag_name('td')
                    datetimestr = cells[-1].text
                    timestr = datetimestr.replace(' at', '')[0:-6]
                    try:
                        date_time_obj = datetime.strptime(timestr, '%d %b %Y %H:%M:%S')
                        diff = (now - date_time_obj).days
                    except:
                        logger.warning('Couldnt parse datetime string')
                    if diff < settings.num_of_days_of_most_recent_sales:
                        sold_in_most_recent_time = True
                    if diff < settings.num_of_days_of_recent_sales:
                        recent_sales += 1
                    if recent_sales >= settings.num_of_sales_in_recent_days:
                        sold_in_recent_time = True
                    i += 1
                if sold_in_recent_time and sold_in_most_recent_time:
                    asins = [result.amazon_asin for result in results]
                    amazon_item = is_item_on_amazon(item.title,asins, driver, logger)
                    if amazon_item:
                        item.sold = times_sold
                        result = Result(ebay_url=item.href, ebay_title=item.title,
                                        amazon_title=amazon_item.amazon_title,
                                        amazon_asin=amazon_item.amazon_asin, amazon_link=amazon_item.amazon_link,
                                        lifetime_sales=item.sold, recent_sales=recent_sales)
                        results.append(result)
                        logger.info(
                            f"Found new result and added to results objects list."
                            f" Ebay Details: {item.href},{item.title}.\n Amazon Details:{amazon_item.amazon_title},"
                            f"{amazon_item.amazon_asin},{amazon_item.amazon_link}."
                            f" Lifetime sales: {item.sold} Recent Sales: {recent_sales}")
            except NoSuchElementException:
                continue
        except WebDriverException as exception:
            logger.error(exception.msg)
            logger.error("Driver crashed during check if criteria is met, restarting and trying again")
            driver.quit()
            driver = initialize_driver()
            is_criteria_met(ebay_store_items, driver, settings, logger)
    return results


def get_ebay_items(ebay_url, driver, settings, logger):
    try:
        driver.get(ebay_url)
        ebay_items_elems = driver.find_elements_by_class_name("s-item__link")
        ebay_items_links = []
        for elem in ebay_items_elems:  # TODO [0:query.num_of_items_from_url]
            if settings.num_of_ebay_items != "All":
                if len(ebay_items_links) >= int(settings.num_of_ebay_items):
                    break
            try:
                if len(elem.text) > 0:
                    ebay_items_links.append(elem.get_attribute("href"))  # build a list of their links
            except:
                continue
        logger.info(f"Got {len(ebay_items_links)} items from provided url.")
        return ebay_items_links
    except WebDriverException as exception:
        logger.error(exception.msg)
        logger.error("Driver crashed while getting ebay items, restarting driver and trying again")
        driver.quit()
        driver = initialize_driver()
        get_ebay_items(ebay_url, driver, settings, logger)


# main logic flow
def run_ebay_query(ebay_url, driver, query_settings, logger):
    query = Query()
    logger.info("Started eBay query")
    last_keepalive = time.time()
    settings = query_settings
    ebay_items = get_ebay_items(ebay_url + NEW_CONDITION + LOCATION_US, driver, settings, logger)  # list of hrefs
    temp_results = []
    for count, item in enumerate(ebay_items):
        if send_keep_alive(last_keepalive, logger):
            last_keepalive = time.time()
        try:
            driver.get(item)
            seller_elem = driver.find_element_by_class_name('mbg-nw')
            seller_name = f"{seller_elem.text}"
            if seller_name not in query.sellers:
                query.sellers.append(seller_name)
                logger.info(
                    f"Getting store items of seller:{seller_elem.text}, who is {count + 1} out of {len(ebay_items)}")
                seller_elem.click()
                driver.find_element_by_link_text("Items for sale").click()
                driver.get(driver.current_url + NEW_CONDITION + LOCATION_US + ITEMS_PER_PAGE)
                ebay_store_items = get_ebay_store_items(driver=driver,
                                                        num_of_results=settings.num_of_seller_top_selling,
                                                        logger=logger)
                logger.info(f"Got {len(ebay_store_items)} items from {seller_name} store.")
                results = is_criteria_met(ebay_store_items=ebay_store_items,
                                          driver=driver, settings=settings, logger=logger)
                logger.info(f"Got {len(results)} items that meet the set criteria.")
                temp_results.append(results)
            else:
                logger.info(f"Seller {seller_name} was already queried, moving on to next seller.")
        except WebDriverException as exception:
            logger.error(exception.msg)
            logger.error("Driver crashed during main logic, restarting driver and moving on to next item.")
            driver.quit()
            driver = initialize_driver()
            continue
    final_results = [item for results in temp_results for item in results]
    return final_results
