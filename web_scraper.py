#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 14:13:12 2022

@author: marlanithin
"""

from selenium import webdriver
import time
import pandas as pd



def glassdoor_scraper(num_jobs, url):
    driver = webdriver.Chrome(executable_path='/Users/marlanithin/chromedriver')
    driver.get(url)
    jobs_retrieved = 0
    time.sleep(10)
    driver.find_element_by_class_name('react-job-listing').click() #clicking on an element to trigger the sign up window
    time.sleep(10)
    #creating empty lists to store the scraped data
    company = []
    rating = []
    role = []
    salary_est = []
    location = []
    company_type = []
    company_size = []
    company_revenue = []
    sector = []
    try:
        driver.find_element_by_xpath(".//span[@class='SVGInline modal_closeIcon']").click() #closing the sign up prompt window
    except NoSuchElementException():
        pass
    
    while jobs_retrieved < num_jobs:
        
        jobs = driver.find_elements_by_class_name('react-job-listing') #listing all the job card elements on the page
          
        
        for job in jobs:
            job.click()
            time.sleep(4)
            
            try:
                company.append(driver.find_element_by_xpath("//div[@class='css-87uc0g e1tk4kwz1']").text[:-5])
                rating.append(driver.find_element_by_xpath("//div[@class='css-87uc0g e1tk4kwz1']").text[-3:])
            except:
                company.append('na')
                rating.append('na')
                pass
            
            try:
                role.append(driver.find_element_by_xpath("//div[@class='css-1vg6q84 e1tk4kwz4']").text)
            except:
                role.append('na')
                pass
            
            try:
                salary_est.append(driver.find_element_by_xpath("//*[@id='JDCol']//span[@class='css-1xe2xww e1wijj242']").text)
            except:
                salary_est.append('na')
                pass
            
            try:
                location.append(driver.find_element_by_xpath("//div[@class='css-56kyx5 e1tk4kwz5']").text)
            except:
                location.append('na')
                pass
            
            try:
                company_size.append(driver.find_element_by_xpath("//span[@class='css-i9gxme e1pvx6aw2']").text)
            except:
                company_size.append('na')
                pass
            
            try:
                company_type.append(driver.find_element_by_xpath("//div[@class='d-flex flex-wrap']/div[3]/span[@class='css-i9gxme e1pvx6aw2']").text)
            except:
                company_type.append('na')
                pass
            
            try:
                company_revenue.append(driver.find_element_by_xpath("//div[@class='d-flex flex-wrap']/div[6]/span[@class='css-i9gxme e1pvx6aw2']").text)
            except:
                company_revenue.append('na')
                pass
              
            try:
                sector.append(driver.find_element_by_xpath("//div[@class='d-flex flex-wrap']/div[5]/span[@class='css-i9gxme e1pvx6aw2']").text)
            except:
                sector.append('na')
                pass
            
            jobs_retrieved+=1
            print(f'Retrieved {jobs_retrieved}/{num_jobs}')
            if jobs_retrieved==num_jobs:
                break
            
        if jobs_retrieved < num_jobs:
            try:
                driver.find_element_by_xpath("//*[@id='MainCol']/div[2]/div/div[1]/button[7]").click() #clicking on next page after exausting all the jobs in current page
                time.sleep(10)
            except:
                print(f'Terminating scraper before reaching target as only {jobs_retrieved} records were available') #if there is no next page return all the jobs that are available
                return pd.DataFrame(list(zip(company, role, salary_est, location, rating, company_type, sector, company_size, company_revenue)),
                columns =['Company', 'Role', 'Salary Estimate', 'Location', 'Glassdoor Rating', 'Company type', 'Sector', 'Company size', 'Company revenue'])
        else:
            print(f'scraping complete and succesfully retrieved {jobs_retrieved} jobs')
            
            return pd.DataFrame(list(zip(company, role, salary_est, location, rating, company_type, sector, company_size, company_revenue)),
            columns =['Company', 'Role', 'Salary Estimate', 'Location', 'Glassdoor Rating', 'Company type', 'Sector', 'Company size', 'Company revenue'])

