#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 15:10:21 2021

@author:  team5 BIA660
"""

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
import csv
import re
LIMIT_DATASET = 10  # this should be 5000


def run(url, jobTitle, limit_dataset=LIMIT_DATASET):
    driver = webdriver.Chrome('./chromedriver')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-popup-blocking")
    file_output = f'./data/{jobTitle}_output.csv'
    # fw=open('software_engineer_test.txt','a',encoding='utf8') #output file for software_engineer
    # output file for software_engineer
    fw = open(file_output, 'a', encoding='utf8')
    # fw=open('data_scientist_test.txt','a',encoding='utf8') #append mode for output file
    # create a csv writer for this file
    writer = csv.writer(fw, lineterminator='\n')
    num = limit_dataset  # 5000 datasets
    """
    if the program stops, need to modify i and page to the numbers after the ones program failed last time
    so that program can append data
    """
    i = 0  # number of dataset
    page = 0  # pagenum

    """
    need to set sleepTime to a larger number(such as 80 ) for big data set 
    to deal with captcha manually when program breaks
    """
    sleepTime = 5
    interval = 0  # set interval to sleep for longer time after 5 round to intimate as an human
    while i < num:
        newUrl = url+'&start='+str(page * 10)
        driver.get(newUrl)

        interval = interval+1
        if interval == 4:
            sleepTime = 150
            interval = 0

        time.sleep(sleepTime)
        sleepTime = 10
        print("this is page:---------------------------- ", page)
        page = page+1

        # if there is a popup window, close it
        try:
            btn = driver.find_element_by_css_selector(
                'button.popover-x-button-close.icl-CloseButton')
            print('popup close btn found---------------')
            btn.click()
        except:
            print('no popup')

        # find the jobcards div
        try:
            jobcards = driver.find_element_by_id('mosaic-provider-jobcards')
            jobsDiv = jobcards.find_elements_by_css_selector(
                "a[class^='tapItem fs-unmask result']")
            # print(len(jobsDiv))

            for job in jobsDiv:
                description, title = 'NA', jobTitle

                try:
                    job.click()
                    time.sleep(3)
                    # switch the to right size frame
                    driver.switch_to_frame('vjs-container-iframe')
                    descriptionDiv = driver.find_element_by_class_name(
                        'jobsearch-jobDescriptionText')
                    description = descriptionDiv.text.replace('\n', " ")
                    # print(description)
                except:
                    print('finding description failed')
                    continue

                # #find title
                # try:
                #     jobTitle = driver.find_element_by_css_selector('h1.jobsearch-JobInfoHeader-title')
                #     title = jobTitle.text
                #     print(title)
                # except:
                #     print('finding title failed')
                #     title = 'Software Engineer' #if job tile is not found, just fill with 'software engineer

                if description != 'NA':
                    writer.writerow([description, title])
                    i = i+1
                    if i == limit_dataset:
                        break
                    # print out the most recent successfull data index and page num
                    print('-----------------------------------i  page ', i, page)
                 # switch back to main frame
                driver.switch_to_default_content()

        except:
            # if find job cards failed, maybe bcs of capatcha issue, sleep longer, sometime need to do capatcha test manually
            print('jobsDiv not found')
            time.sleep(300)
            driver.refresh()

        # get to next page by edit url
        page = page+1

    fw.close()
    driver.quit()


"""
url is for Software Engineer
jobTitle is for Software Engineer
url2 is for data scientist
jobTitle2 is for Data Scientist
"""
url = "https://www.indeed.com/jobs?q=Software%20Engineer"
jobTitle = 'Software Engineer'
jobTitle2 = 'Data Scientist'
url2 = "https://www.indeed.com/jobs?q=data%20scientist"

if __name__ == "__main__":
    run(url, jobTitle)
    # run(url2,jobTitle2)
