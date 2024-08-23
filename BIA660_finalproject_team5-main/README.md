# BIA660 WS Group 5 Final Project

1 - Collect at least 5,000 Job Ads for Data Scientists from Indeed.com.

2 - Collect at least 5,000 Job Ads for Software Engineers from Indeed.com.

3 - Get the html of the job description (as shown on the right side of the screen after you click on an Ad) for each Ad. 

4 - Extract the text from the html and create a csv with 1 Ad per line and 2 columns: <text>, <job title>

5- Train a classification model that can predict whether a given Ad is for a Data Scientist or Software Engineer.

### Notes:
- Your trained model will be evaluated on a separate test set that you will not have access to before the deadline.
- The deliverables include:
    - The scraping script(s)
    - The classification script
    - Instructions on how to run the 2 scripts
    - The csv from step 4
- Your classification script should be able to read a test csv that will include 1 job description per line (no labels).  It should then produce a new file that includes the predicted label for each line in the test file.


## Team Member:
- Maurizio Bella
- Justin Bernstein
- Ying Liu

## Task Division:
- Web scraping: Justin & Ying
- Models and Predictions: Maurizio Bella



## Installation
- Requirement: python3, pip3
```
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt # (pip install [package_name] -U)
```
## Execute it
```
$ source env/bin/activate
$  python .
```

## Example of output
```
generated dataset
Opening the dataset and make prediction
open file ./data/temp.csv
Accuracy:  0.8333333333333334
--------------------------------
Please enter the file name:
./data/data_test.csv
You entered ./data/data_test.csv
open file ./data/data_test.csv
generate file in ./data/indeed_prediction.csv
Exit!
```

## Dataset
- example alldata.csv [here](https://www.kaggle.com/sl6149/data-scientist-job-market-in-the-us)