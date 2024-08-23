# -*- coding: utf-8 -*-
from indeed import run as run_indeed
from classification import load_data, run, load_data_test
import pandas as pd
"""
Team Member:
- Maurizio Bella
- Justin Bernstein
- Ying Liu

Task Division:
- Web scraping: Justin & Ying
- Models and Predictions: Maurizio Bella

Created on Aug 1st 2021

@author: group5 BIA660
"""
url_software = "https://www.indeed.com/jobs?q=Software%20Engineer"
jobTitle_software = 'software_engineer'
filename_software = './data/software_engineer_output.csv'
url_data = "https://www.indeed.com/jobs?q=data%20scientist"
jobTitle_data = 'data_scientist'
filename_data = './data/data_scientist_output.csv'
filedataset = "./data/temp.csv"
LIMIT_DATASET = 100

if __name__ == "__main__":
    print(
        f'collect {LIMIT_DATASET} Job Ads for Software Engineer from Indeed.com.')
    run_indeed(url_software, jobTitle_software, LIMIT_DATASET)
    print(
        f'collect {LIMIT_DATASET} Job Ads for Data Scientists from Indeed.com.')
    run_indeed(url_data, jobTitle_data, LIMIT_DATASET)
    print('generated dataset')
    file = open("./data/temp.csv", "w")
    file1 = open(filename_software, "r")
    file2 = open(filename_data, "r")

    for line in file1:
        file.write(line)

    for line in file2:
        file.write(line)

    file.close()
    file1.close()
    file2.close()
    print('Opening the dataset and make prediction')
    X_train, X_test, y_train, y_test = load_data(filedataset)
    classifier, vect = run(X_train, X_test, y_train, y_test)
    print('--------------------------------')
    filename = input(
        "Please enter the file name with 1 job description per line (example ./data/data_test.csv ):\n")
    print(f'You entered {filename}')
    # filename = './data/data_test.csv'
    load_data_test(filename, classifier, vect)
    print('Exit!')
