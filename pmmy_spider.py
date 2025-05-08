# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from pmmy.items import PmmyItem
# from scrapy.http import Request
from scrapy.selector import Selector
from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import glob, os
# import urlparse


class PmmySpiderSpider(scrapy.Spider):
    name = "pmmy_spider"
    allowed_domains = ["www.pmmydata.mudra.org.in"]
    start_urls = (
        'http://pmmydata.mudra.org.in/Reports/Performance#/',
    )
    def __init__(self):
        self.driver = webdriver.Chrome('C:/Python27/selenium/webdriver/chromedriver.exe')
        # self.driver = webdriver.Firefox()

    def parse(self, response):
        self.driver.get(response.url)
        username = self.driver.find_element_by_id("UserName")
        username.send_keys("ReportingUser")
        password = self.driver.find_element_by_id("Password")
        password.send_keys("ReportingUser_123")
        self.driver.find_element_by_id("login_submit").click()

        ## Bank List
        # selectBank = self.driver.find_element_by_id("BankId")
        # bankoptions = selectBank.find_elements_by_tag_name("option")
        # banklist=[]
        #
        # ## State List
        # selectState = self.driver.find_element_by_id("StateId")
        # stateoptions = selectState.find_elements_by_tag_name("option")
        # statelist=[]

        ## Data until date - issue persists
        datelist = [ "05/04/2015","05/05/2015","05/06/2015","05/07/2015","05/08/2015","05/09/2015","05/10/2015","05/11/2015",
                    "05/12/2015", "05/01/2016", "05/02/2016", "05/03/2016", "05/04/2016", "05/05/2016", "05/06/2016",
                    "05/07/2016", "05/08/2016"]

        date= self.driver.find_element_by_id("_DataTillDate")

        n = 1
        d = 'd:\varun.aggarwal\Downloads\vaish downloads tue'
        dateindex = range(2,11)
        self.driver.find_element_by_xpath('*//div[@id="FYear_chosen"]').click()
        self.driver.find_element_by_xpath('*//div[@id = "FYear_chosen"]/div/ul/li[1]').click()

        for i in dateindex:
            date.clear()
            date.send_keys(datelist[i])

        # for bankoption in bankoptions:
        #     banklist.append(bankoption.get_attribute("value"))
        #
        # for stateoption in stateoptions:
        #     statelist.append(stateoption.get_attribute("value"))
        # banklist = range(20,234)
            banklist = range(2,237)
            statelist = range(2,37)
            items = []


            for bank in banklist:
                # print("starting loop on bank %s" % bank)
                item = PmmyItem()
                try:
                    self.driver.find_element_by_xpath('*//div[@id="BankId_chosen"]').click()
                    bankxpath = '//*[@id = "BankId_chosen"]/div/ul/li['
                    bankxpath += str(bank)
                    bankxpath += ']'
                    bank = self.driver.find_element_by_xpath(bankxpath).click()
                    time.sleep(1)
                except NoSuchElementException:
                    time.sleep(20)
                    continue
                # item['Banklist'] = self.driver.xpath('*//a[@class="chosen-single"]/span//text()').extract()
                # items.append(item)
                for state in statelist:

                    try:
                        self.driver.find_element_by_xpath('*//div[@id="StateId_chosen"]').click()
                        statexpath = '//*[@id = "StateId_chosen"]/div/ul/li['
                        statexpath += str(state)
                        statexpath += ']'
                        state = self.driver.find_element_by_xpath(statexpath).click()
                        time.sleep(1)

                        self.driver.find_element_by_xpath('*//input[@value="Search"]').click()

                        time.sleep(1)
                        export = self.driver.find_element_by_xpath('*//a[@title="Export"]')

                        try:
                            norecords = self.driver.find_element_by_xpath('*//div[@class="info-icon"]')
                        except NoSuchElementException:
                            export.click()
                            time.sleep(1)
                            continue
                    except NoSuchElementException:
                        time.sleep(20)
                        continue

                for fname in os.listdir(d):
                    if fname.startswith("Perfo"):
                        fpath = os.path.join(d,fname)
                        newfname = str(n)+"_" + fname
                        os.rename(fpath, os.path.join(d, newfname))
        # if fname.startswith(badprefix):
            # rename(fname, fname.replace(badprefix, str(n), 1))
                        n+= 1

