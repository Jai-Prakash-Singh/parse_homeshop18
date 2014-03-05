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




def main2(ml_mt_sub, filename):
  
    f = open(filename, "a+")

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

                print >>f, ','.join([menulink, menutitle, catolink, catotitle, sub_catolink, sub_catotext])
                
	else:
	   print >>f, ','.join([menulink, menutitle, catolink, catotitle, catolink, catotitle])

    f.close()




def mainthreading2(i, q):
    for ml_mt_sub , filename in iter(q.get, None):
        try:
            main2(ml_mt_sub, filename)

        except:
            f2 = open("page1_first_error.txt", "a+")
            print >>f2, ml_mt_sub
            f2.close()

        time.sleep(2)
        q.task_done()

    q.task_done()
        


	
def mainthreading(ml_mt):

    f = open("to_extract.txt", "a+")
    directory = f.read().strip()
    f.close()

    filename = "%s/%s" %(directory, "f_ml_mt_ctt_ctl_sl_st.txt")
    
    procs = []
  
    for i in range(num_fetch_threads):
        procs.append(multiprocessing.Process(target=mainthreading2, args=(i, enclosure_queue,)))
        #worker.setDaemon(True)
        procs[-1].start()

    for  ml_mt_sub in ml_mt:
        enclosure_queue.put((ml_mt_sub, filename))

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

    print "closing file...."
    



def main():

    directory = "dir%s" %(time.strftime("%d%m%Y"))

    try:
        os.makedirs(directory)

    except:
        pass

    f = open("to_extract.txt", "w+")
    print >>f, directory
    f.close()

    f = open("extracted.txt", "a+")
    print >>f, directory
    f.close()

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
