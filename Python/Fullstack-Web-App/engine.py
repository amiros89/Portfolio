from datetime import datetime
from db_classes import db, Query, Product,User
from mail import send_query_ended
import os
import loggerFactory
from utils import initialize_driver, get_ebay_items, get_amazon_items
from ebay_to_amazon import run_ebay_query



# TODO make this configurable from user settings page / query settings

def run_query(query_id):
    logger = loggerFactory.SingleFileLogger(
        path=os.getcwd() + f'/logs/{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.log',
        logging_level="INFO", reset=True)
    session=db.create_scoped_session()
    query = session.query(Query).filter_by(id=query_id).first()
    logger.info("Query request recieved and found")
    driver = initialize_driver()
    logger.info("Selenium Chrome Driver Started")
    if query.type == "ebay":
        results = run_ebay_query(query.ebay_url, driver,query.settings,logger)
    else:
        amazon_products = get_amazon_items(query.ebay_url, driver, logger)
        logger.info("Got list of Amazon products, moving to scrape eBay")
        results = get_ebay_items(amazon_products, driver, logger)
        logger.info("Got final list of items from eBay, closing Selenium Chrome driver and processing results.")
    driver.quit()
    query.num_of_products = len(results)
    query.end_time = datetime.utcnow()
    query.status = "Completed"
    logger.info("Query completed successfully")
    i = 1
    if len(results) > 0:
        for item in results:
            new_product = Product()
            new_product.query_id = query
            new_product.id = i
            new_product.asin = item.amazon_asin
            new_product.ebay_title = item.ebay_title
            new_product.amazon_title = item.amazon_title
            new_product.amazon_link = item.amazon_link
            new_product.ebay_url = item.ebay_url
            new_product.lifetime_sales = item.lifetime_sales
            new_product.recent_sales = item.recent_sales
            query.products.append(new_product)
            i += 1
    try:
        session.commit()
        logger.info("Query committed successfully to database")
    except Exception as e:
        logger.error("Internal Error")
        logger.info(e)
    else:
        session.commit()
    user = session.query(User).filter_by(id=query.runner_id).first()
    if user.email_notifications:
        logger.info("Sent email notification to user")
        send_query_ended(query.runner_id)
    return
