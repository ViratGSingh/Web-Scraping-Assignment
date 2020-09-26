# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from shutil import which
from scrapy.selector import Selector
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


class InternSpider(scrapy.Spider):
    name = 'intern'
    allowed_domains = ['internshala.com']
    start_urls = ['https://internshala.com/internships']

    def __init__(self):
        firefox_options= Options()
        firefox_options.add_argument("--headless") 
        firefox_path=which("geckodriver.exe")

        driver= webdriver.Firefox(executable_path=firefox_path,options=firefox_options)
        driver.set_window_size(1920,1080)
        driver.get("https://internshala.com/internships/page-0")
        timeout=5
        WebDriverWait(driver,timeout)
        button=driver.find_element_by_xpath("/html/body/div[1]/div[17]/div/div[2]/div[3]/div[2]")
        button.click()

        self.html=driver.page_source
        driver.close()

    def parse(self, response):
        #make string into a selector
        resp=Selector(text=self.html)

        #extracting the listing container
        listings=resp.xpath("/html/body/div[1]/div[19]/div[2]/div/div[3]/div[2]/div[2]/div/div")
        
        #extracting contents of the listing container
        for listing in listings:
             
            profile=listing.xpath(".//div[1]/div[1]/div[1]/div[1]/a/text()").get(),
            company=listing.xpath(".//div[1]/div[1]/div[1]/div[2]/a/text()").get()
            logo_url=listing.xpath(".//div[1]/div[1]/div[2]/img/@src").get() 
            start_date=listing.xpath(".//div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/span[2]/text()").get()
            apply_by=listing.xpath(".//div[1]/div[2]/div[2]/div[2]/div[2]/div[2]/text()").get()
            job_type=listing.xpath(".//div[2]/div/div[@class='label_container label_container_desktop']/text()").get() 
            duration=listing.xpath(".//div[1]/div[2]/div[2]/div[1]/div[2]/div[2]/text()").get()
            stipend=listing.xpath(".//div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/span/text()").get()
            location=listing.xpath(".//div[1]/div[2]/div[1]/span/a/text()").get()
            
            profile=" ".join(profile)
            company=" ".join(company.split())
            
            #filling columns with relevant info if empty

            try:
                logo_url=" ".join(logo_url.split())
                logo_url="{}logo_url".format("https://internshala.com")
            except:
                logo_url="no logo"
            try:
                start_date=" ".join(start_date.split())
            except:
                start_date="not mentioned"
            try:    
                apply_by=" ".join(apply_by.split())
            except:
                apply_by="not mentioned"
            try:    
                job_type=" ".join(job_type.split())
            except:
                job_type="not mentioned"
            try:    
                duration=" ".join(duration.split())
            except:
                duration="not mentioned" 
            try:
                location=" ".join(location.split())
            except:
                location="not mentioned"
                
            #dictionary of listing's contents
            
            yield{
                   "profile": profile,
                   "company": company,
                   "logo_url":logo_url,
                   "start_date":start_date,
                   "apply_by":apply_by,
                   "job_type":job_type,
                   "duration":duration,
                   "stipend":stipend,
                   "location":location
                 }
        #dealing with pagination
        
        ###number of pages can be changed according to user's requirements
        pages=3
        for page in range(0,pages):
            yield scrapy.Request( 
                  url="https://internshala.com/internships/page-{}".format(page),
                  
                  callback=self.parse
                  )                    
            
         