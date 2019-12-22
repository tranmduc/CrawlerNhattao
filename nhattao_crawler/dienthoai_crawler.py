# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 09:50:46 2019

@author: Minh Duc
"""

import sys
from selenium import webdriver
from parsel import Selector
from time import sleep
import csv
import time
from selenium.webdriver.chrome.options import Options

def validate_field(field):
    if field:
        field.strip()
    else:
        field = ""
    return field

def removeURLMonth(url):
    url_parts = url.split("&")
    return url_parts[2]



class Crawl():
    def __init__(self):
        self.temp_url = "& &"

        chrome_options = Options()
        chrome_options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=chrome_options, executable_path='D:\Software\chromedriver')
        #self.driver = webdriver.Chrome('D:\Software\chromedriver')

        if (len(sys.argv) == 1):
            self.runAll()

        elif (len(sys.argv) == 2):
            self.switch(sys.argv[1])

        else:
            print("Wrong numbers of argument!")

    def runAll(self):
        tabs = ["dienthoai", "maytinhbang", "maytinh", "camera", "dienmay", "xe", "sim", "dongho", "matkinh"]

        for tab in tabs:
            self.switch(tab)

    def switch(self, tab):
        if (tab == "dienthoai"):
            self.dienThoai()

        elif (tab == "maytinhbang"):
            self.mayTinhBang()

        elif (tab == "maytinh"):
            self.mayTinh()

        elif (tab == "camera"):
            self.camera()

        elif (tab == "dienmay"):
            self.dienMay()

        elif (tab == "xe"):
            self.xe()

        elif (tab == "sim"):
            self.sim()

        elif (tab == "dongho"):
            self.dongHo()

        elif (tab == "matkinh"):
            self.matKinh()

        else:
            print ("Wrong argument!")

    def dienThoai(self):
        self.driver.get("https://nhattao.com/f/dien-thoai.543/")
        sleep(1)

        self.sub_brand_page()

    def mayTinhBang(self):
        self.driver.get("https://nhattao.com/f/may-tinh-bang.548/")
        sleep(1)

        self.sub_brand_page()

    def mayTinh(self):
        self.driver.get("https://nhattao.com/f/may-tinh.553/")
        sleep(1)

        self.sub_brand_page()

    def camera(self):
        self.driver.get("https://nhattao.com/f/camera.556/")
        sleep(1)

        self.sub_brand_page()

    def dienMay(self):
        self.driver.get("https://nhattao.com/f/dien-may.602/")
        sleep(1)

        self.sub_page()

    def xe(self):
        self.driver.get("https://nhattao.com/f/xe.532/")
        sleep(1)

        self.sub_page()

    def sim(self):
        self.driver.get("https://nhattao.com/f/sim-dien-thoai.533/")
        sleep(1)

        self.sub_brand_page()

    def dongHo(self):
        self.driver.get("https://nhattao.com/f/dong-ho-thong-minh.585/")
        sleep(1)

        self.brand_page()

    def matKinh(self):
        self.driver.get("https://nhattao.com/f/mat-kinh.749/")
        sleep(1)

        self.sub_brand_page()

    def sub_page(self):
        brands = self.driver.find_elements_by_xpath('//*[@class="nodeTitle"]/a')
        brands = [brand.get_attribute('href') for brand in brands]
        for brand in brands:
            self.driver.get(brand)
            sleep(1)
            self.sub_brand_page()

    def sub_brand_page(self):
        brands = self.driver.find_elements_by_xpath('//*[@class="nodeTitle"]/a')
        brands = [brand.get_attribute('href') for brand in brands]
        brands = brands[1:]
        for brand in brands:
            self.driver.get(brand)
            sleep(1)
            self.brand_page()

    def brand_page(self):
        try:
            self.driver.find_element_by_xpath('//a[text()="34"]').click()
            sleep(1)

            years = self.driver.find_elements_by_xpath('//h3[text()="Archived by Years"]/following-sibling::ol/li/a')
            year_urls = [year.get_attribute('href') for year in years]
            #year_urls = year_urls[1:]
            for year_url in year_urls:
                self.driver.get(year_url)
                sleep(1)
                self.year_page()

        except:
            self.week_page()

    def year_page(self):
        months = self.driver.find_elements_by_xpath('//h3[text()="Archived by Months"]/following-sibling::ol/li/a')
        month_urls = [month.get_attribute('href') for month in months]
        for month_url in month_urls:
            self.driver.get(month_url)
            sleep(1)
            self.month_page()

    def month_page(self):
        weeks = self.driver.find_elements_by_xpath('//h3[text()="Archived by Weeks"]/following-sibling::ol/li/a')
        week_urls = [week.get_attribute('href') for week in weeks]
        for week_url in week_urls:
            if(removeURLMonth(week_url) != removeURLMonth(self.temp_url)):
                self.driver.get(week_url)
                sleep(1)
                self.temp_url = week_url
                self.week_page()

    def week_page(self):
        try:
            items = self.driver.find_elements_by_xpath('//a[@class="Nhattao-CardItem--image"]')
            item_urls = [item.get_attribute('href') for item in items]
            for item_url in item_urls:
                self.item_page(item_url)
        except:
            pass

        try:
            next_page = self.driver.find_element_by_xpath('//a[text()="Sau >"]')
            next_page.click()
            sleep(1)
            self.week_page()
        except:
            pass

    def item_page(self, item_url):
        self.driver.get(item_url)
        sleep(1)

        sel = Selector(text=self.driver.page_source)

        phoneNumbers = sel.xpath('//*[@class="threadview-header--contactPhone"]/text()').extract()
        if (phoneNumbers == []):
            phoneNumber = ""
        else:
            phoneNumber = phoneNumbers[1]
            phoneNumber = phoneNumber.strip('\n\t\t\t\t\t\t\t\t\t')

        price = sel.xpath('//*[@class="threadview-header--classifiedPrice"]/text()').extract_first()
        if price:
            price = price.strip('\n\t\t\t\t\t\t\n\t\t\t\t\t\t')
        else:
            price = ""

        status = sel.xpath('//*[@class="threadview-header--classifiedStatus"]/text()').extract_first()
        status = validate_field(status)

        location = sel.xpath('//*[@class="threadview-header--classifiedLoc"]/span/text()').extract_first()
        location = validate_field(location)

        address = sel.xpath('//*[@class="address"]/text()').extract_first()
        address = validate_field(address)

        views = sel.xpath('//*[@class="threadview-header--viewCount"]/b/text()').extract_first()
        views = validate_field(views)

        date_time = sel.xpath('//*[@class="threadview-header--postDate"]/abbr/text()').extract_first()
        #date_time = sel.xpath('//*[@class="threadview-header--postDate"]/abbr/@data-datestring').extract_first() + " " + sel.xpath('//*[@class="threadview-header--postDate"]/abbr/@data-timestring').extract_first()

        if date_time:
            pass
        else:
            date_time = sel.xpath('//*[@class="threadview-header--postDate"]/span/@title').extract_first()
            #date_time = date_time.replace(" at ", " ")

        date_time = validate_field(date_time)

        seller = sel.xpath('//*[@class="username seller-name"]/span/text()').extract_first()
        seller = validate_field(seller)

        seller_date_start = sel.xpath('//dt[text()="Ngày tham gia:"]/following-sibling::dd/span/@title').extract_first()
        seller_date_start = validate_field(seller_date_start)
        #seller_date_start = seller_date_start.replace(" at ", " ")


        seller_product_count = sel.xpath('//dt[text()="Sản phẩm:"]/following-sibling::dd/text()').extract_first()
        seller_product_count = validate_field(seller_product_count)

        seller_likes = sel.xpath('//dt[text()="Thích đã nhận:"]/following-sibling::dd/text()').extract_first()
        seller_likes = validate_field(seller_likes)

        item_url = self.driver.current_url
        item_url = validate_field(item_url)

        t = time.localtime()
        t = time.strftime('%m %d %Y %H:%M:%S', t)

        item_classes = sel.xpath('//span[@itemprop="title"]/text()').extract()
        if (item_classes == []):
            item_1st_class = ""
            item_2nd_class = ""
            item_3rd_class = ""
        elif (len(item_classes) == 3):
            item_1st_class = item_classes[1]
            item_2nd_class = item_classes[2]
            item_3rd_class = ""
        elif (len(item_classes) == 4):
            item_1st_class = item_classes[1]
            item_2nd_class = item_classes[2]
            item_3rd_class = item_classes[3]


        data = {
                'Phone Number': phoneNumber,
                'Price': price,
                'Status': status,
                'Location': location,
                'Address': address,
                'Views': views,
                'Date - Time': date_time,
                'First class': item_1st_class,
                'Second class': item_2nd_class,
                'Third class': item_3rd_class,
                'Seller': seller,
                'Seller starting date': seller_date_start,
                'Seller products count': seller_product_count,
                'Seller likes': seller_likes,
                'Item URL': item_url,
                'Crawled time': t
                }

        print(data)

        self.save_data(data)

        self.driver.back()
        sleep(1)

    def save_data(self, data):
        dict_data = []
        dict_data.append(data)

        csv_columns = ['Phone Number',
                       'Price',
                       'Status',
                       'Location',
                       'Address',
                       'Views',
                       'Date - Time',
                       'First class',
                       'Second class',
                       'Third class',
                       'Seller',
                       'Seller starting date',
                       'Seller products count',
                       'Seller likes',
                       'Item URL',
                       'Crawled time']

        csv_file = "nhattao.csv"

        try:
            with open(csv_file, 'a', encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, delimiter='╡', lineterminator='\n', fieldnames=csv_columns)
                for data in dict_data:
                    writer.writerow(data)
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)

if __name__ == '__main__':
    run = Crawl()
    run.__init__
