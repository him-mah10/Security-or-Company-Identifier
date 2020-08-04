# Author - Himanshu Maheshwari

## Objective:
Given a set of news data and the objective is to perform NER on the data to derive a particular security for which the article is. These news articles may refer to one or more companies. The goal is to find out the primary company which the article is referring to. 

### Rules to identify primary company:
 1. If an article title contain company name or security name that takes precedence over others
 2. If an article contains one security or company’s name multiple times, the company or security mentioned the most would win.
 3. If an article contains several securities, the company which was mentioned first should win.

## Solution Outline:
 - For NER I am using spaCy - which is very fast, scalable and provides state-of-the art results.
 - First we take the given headline and perform NER on it.
 - Then get all the Named Entity of the type organization.
 - The first occurring company/security name is taken as the primary security(As per Rule 1). For example in the headline: "Amazon and Facebook records losses.", the primary security would be Amazon(AMZN) and all the securities will include: Amazon and Facebook.
 - Next we use web scraping techniques to get the company's ticker symbol. I am using web scraping because the data that was given was very sparse and unlabelled and thus was not suitable to train any kind of model. Due to time limitation, I could not make my own dataset.
 - Next, if the news article is given, we take it and perform NER on it similar to the way described above.
 - If there is no primary security, then we use Rule 2 and Rule 3.
 - First we take all the securities and count their frequencies. The company that is most frequent is chosen to be as Primary Security as per Rule 2. If all of them have the same frequency then the company that was mentioned first is chosen as Primary Security as per Rule3.
 - I have implemented two modes of script as described below.

### Different Modes
 - Mode 1 - In this mode we provide a file as command line input to the script and the script produces a new file called output.csv, which has two additional column called security and securities. The security and securities information are added here. The input file should have same structure as 'uci-news-aggregator.csv'.
 - Mode 2 - In this mode we provide Title and/or Article Text as command line input to the script and the script outputs security and securities.

## How to run?

 - The script is written in python3 and I have attached requirements.txt file. First install all the requirements.
 - If you want to run Mode 1 i.e. you want to give input csv file and get an output csv file, open run.sh file and make changes like this - 
  `mode=1`  
  `filename="uci-news-aggregator.csv" #Insert File name here if mode==0`
  `python code.py $mode "$filename"`
  It will produce a file **output.csv** in same directory with structure similar to filename but with additional column for security and securities.
 - If you want to run Mode 2 i.e. you want to give input title and/or article text, open run.sh file and make changes like this 
 `mode=2`
 `title="Insert the news title here"` 
`article="Insert the article text here.`
`python code.py $mode "$filename" "$article" `
It will output security and securities.
- After that open terminal and use command `bash run.sh`
## Sample Output
### run.sh: 
  `mode=1`  

  `filename="uci-news-aggregator.csv" #Insert File name here if mode==0`

  `python code.py $mode "$filename"`
### output
`output.csv` file.


### run.sh:
`mode=1`

`title="Apple Inc and Google started working on COVID-19 tracing application. AAPL stock went up by 1%." `

`python code.py $mode "$title"`
### output:
`security: AAPL`

`securities: ['GOOG', 'AAPL']`

### run.sh:
`mode=1`

`title="Apple, Amazon and Microsoft are reporting earnings after market close on April 30th." `

`python code.py $mode "$title"`
### output:
`security: AAPL`

`securities: ['AAPL', 'MSFT', 'AMZN']`



### run.sh:
`mode=1` 

`title="Zacks Investment Ideas feature highlights: Google, Facebook, Apple, Microsoft and Amazon" `

`article="Chicago, IL – May 4, 2020 – Today, Zacks Investment Ideas feature highlights Features: Google GOOGL, Facebook FB, Apple AAPL, Microsoft MSFT and Amazon AMZN.
Market Rally Exhausted After Big Tech Earnings
The stimulus-driven equity markets may be exhausted after big tech released its March quarter earnings this week. The market had rallied over 30% from its lows in late March to the end of April. Now investors are pulling profits off the table with uncertainty still exceptionally high.
Big Tech Turnout 
Tech earnings were mixed. Google and Facebook both surged off the engagement tailwind that each demonstrated in their reports, boosted by the global stay at home initiative. Apple shares are seeing modest gains this morning after beating both top and bottom-line estimates, with services driving a progressively more substantial portion of its income.
Microsoft’s essential enterprise cloud services have allowed the company’s operations to get by virtually unscathed by the pandemic. The firm illustrated robust double-digit top and bottom line expansions year-over-year in its March quarter results. MSFT remains up over 10% for the year, and I suspect these shares will reach a new all-time high in the next 6-months.
Amazon shares had been trading at all-time highs going into earnings last night, and the miss on EPS estimates was enough for investors to start pulling profits. AMZN is still up 22% in 2020 thus far. This pandemic is the perfect storm for Amazon, conditioning the world to rely on its first-class e-commerce platform for their shopping needs, and further illuminating the necessity of its cloud computing services. AMZN is still too expensive for me to consider purchasing, but the long-term investment outlook is compelling.
Profit pulling from these big tech names is not the only reason that the markets have broken down the last couple of trading days. We are living in a digital world where technology drives more than just consumption patterns. Computers are now literally running the equity markets."`

`python code.py $mode "$title" "$article" `

### output: 
`security: GOOG`
`securities: ['FB', 'AMZN', 'MSFT', 'AAPL', 'GOOG', 'UBS']`

