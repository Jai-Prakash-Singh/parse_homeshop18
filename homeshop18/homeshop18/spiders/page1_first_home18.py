#!/usr/bin/env python 

import phan_proxy
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
import re
import logging
import time
import os
import req_proxy
import multiprocessing
import logging

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

num_fetch_threads = 10
enclosure_queue = multiprocessing.JoinableQueue()




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




def main2(ml_mt_sub):
    menulink = ml_mt_sub[0]
    menutitle = ml_mt_sub[1]
    
    page = req_proxy.main(menulink)

    soup = BeautifulSoup(page)

    tag_box = soup.find_all("div", attrs={"class":"head clearfix"})
    
    for al in tag_box:
        cato = al.find("div")

        catolink = "%s%s" %("http://www.homeshop18.com", str(cato.a.get("href")).strip())
        catotitle = cato.a.get_text()

        sub_cato = al.find_next_sibling("div")
        
	if sub_cato:
            sub_cato2 = sub_cato.find_all("a")

	    for al in sub_cato2:
	        sub_catolink = "%s%s" %("http://www.homeshop18.com", str(al.get("href")).strip())
                sub_catotext = al.get("title")

                print menulink, menutitle, catolink, catotitle, sub_catolink, sub_catotext
                
	else:
	   print menulink, menutitle, catolink, catotitle, catolink, catotitle




def mainthreading2(i, q):
    for ml_mt_sub in iter(q.get, None):
        #print ml_mt_sub
        try:
            main2(ml_mt_sub)

        except:
            f = open("page1_first_error.txt", "a+")
            print >>f, ml_mt_sub
            f.close()


        time.sleep(2)
        q.task_done()

    q.task_done()
        


	
def mainthreading(ml_mt):
    procs = []
  
    for i in range(num_fetch_threads):
        procs.append(multiprocessing.Process(target=mainthreading2, args=(i, enclosure_queue,)))
        #worker.setDaemon(True)
        procs[-1].start()

    for  ml_mt_sub in ml_mt:
        enclosure_queue.put(ml_mt_sub)

    print '*** Main thread waiting'
    enclosure_queue.join()
    print '*** Done'

    for p in procs:
        enclosure_queue.put(None)

    enclosure_queue.join()

    for p in procs:
        p.join()

    print "Finished everything...."
    print "num active children:", multiprocessing.active_children()

    


def main():
    link = "http://www.homeshop18.com/all-stores.html"

    driver = phan_proxy.main(link)

    try:
        WebDriverWait(driver, 1000).until( ajax_complete,  "Timeout waiting for page to load")
    except WebDriverException:
        pass

    try:
        driver.find_element_by_xpath("/html/body/div[7]/div/a").click()
    except:
        pass

    try:
        WebDriverWait(driver, 1000).until( ajax_complete,  "Timeout waiting for page to load")
    except WebDriverException:
        pass

    driver = driver_scroller(driver)

    page = driver.page_source    
    
    soup = BeautifulSoup(page)

    tag_menuflyer = soup.find("div", attrs={"class":"bcMenuFlyer"})

    tag_menu_lt = tag_menuflyer.find_all("a")

    ml_mt = []

    for lt in tag_menu_lt:
         lt.get_text()
	 menulink = "%s%s" %("http://www.homeshop18.com", str(lt.get("href")).strip())
         menutitle = str(lt.get_text()).strip()
         ml_mt.append([menulink , menutitle])
      
    mainthreading(ml_mt)
         



if __name__=="__main__":
    main()
    #ml_mt_sub = ['http://www.homeshop18.com/jewellery/category:3376/', 'jewellery']
    #main2(ml_mt_sub)
