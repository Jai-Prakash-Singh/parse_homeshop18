#!/usr/bin/env python 
import phan_proxy
from bs4 import BeautifulSoup
import logging
import time 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException



logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )


def ajax_complete(driver):
    try:
        return 0 == driver.execute_script("return jQuery.active")

    except WebDriverException:
        pass



def driver_scroller(driver):
    height = 0
    loop = True

    while loop is True:
        logging.debug("scrolling...")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        heightnow = driver.execute_script("return $(document ).height();")

        if heightnow == height:
            loop = False

        else:
            height = heightnow
            loop = True

    return driver


def sub_scroller(driver):
    loop = True
    while loop is True:
        try:
            print "clicking..."
            driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div[3]/div/span/a/span").click()
            
            WebDriverWait(driver, 1000).until( ajax_complete,  "Timeout waiting for page to load")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(driver, 1000).until( ajax_complete,  "Timeout waiting for page to load")

        except WebDriverException:
            return driver 





def main(line):
    print line
    line2 = line.strip().split(",")
    
    menulink = line2[0].strip()
    menutitle = line2[1].strip()
  
    catlink = line2[2].strip()
    cattitle = line2[3].strip()

    subcatlink = line2[4].strip()
    subcatitle = line2[5].strip()

    brandlink = line2[6].strip()
    brandtite = line2[7].strip()

    driver = phan_proxy.main(brandlink)
   
    driver = driver_scroller(driver)    

    driver = sub_scroller(driver)

    page = driver.page_source
    
    soup = BeautifulSoup(page)

    tag_srchresult = soup.find("div", attrs={"id":"searchResultsDiv"})

    tag_product = tag_srchresult.find_all("p", attrs={"class":"product_title"})

    for al in tag_product:
        print "%s%s" %("http://www.homeshop18.com", str(al.a.get("href")).strip())

    
    


if __name__=="__main__":
    line = "http://www.homeshop18.com/fashion-accessories/category:15095/,Fashion Accessories,http://www.homeshop18.com/unisex/category:15521/,Unisex,http://www.homeshop18.com/caps-26-hats/category:16999/,Caps & Hats,http://www.homeshop18.com/caps-26-hats/category:16999/filter_Brand:%28%22CrossCreek%22%29/,Caps & Hats - CrossCreek"

    main(line)

