# Dictionary-based Sentiment Analysis

> [Description](#description) | [Methods](#methods) | [Repository Structure](#repository-structure) | [Usage](#usage) | [Results and Disucssion](#results-and-discussion) |

## Description
> This project relates to Assignment 3: Sentiment Analysis of the course Language Analytics.

Sentiment analysis aims to investigate the sentiment, meaning emotionality or polarity and its temporal development in text. One way sentiment can be analysed is through dictionary based approaches, meaning single words are assigned sentiment values which are defined in a dictionary **spaCyTextBlob** and **VADER** are dictionaries, which can be used for sentiment analysis. 
This repository provides a script to conduct dictionary-based sentiment analysis on a dataset of over a million headlines of the Australian news source ABC from 2003-2020. The script can extract sentiment scores using either **spaCyTextBlob** and **VADER**. Further, it will visualise the temporal development of sentiment scores over time using 1-week and 1-month rolling averages. Running the script with both dictionary also allowed comparing the two methods and how similar/different their results are.


## Methods

### Data and Preprocessing
For this project a collection of over a million headlines of the Australia news source ABC (Start Date: 2003-02-19 ; End Date: 2020-12-31) was used. The data is available on [Kaggle](https://www.kaggle.com/therohk/million-headlines).

### Dictionary-Based Sentiment Anaylsis
*spaCyTextBlob* returns for any given sentence a score of polarity (positive, negative) and subjectivity (emotionality). In this project, the score of polarity is used, which ranges between -1 (negative) and 1 (positive). *VADER* returns the probability of a sentence being positive, negative or neural, and a compound score, which is an aggregated score of all values. This compound score also ranges between -1 (negative) and 1 (positive). For each headline in the data, either the polarity score using *spaCyTextBlob* or the compound score using *VADER* is extracted. Subsequently, a daily average is computed, as the data contained multiple headlines per day. These daily averages were then used to calculate rolling averages over 1-week and 1-month.


## Repository Structure
```
|-- data/
    |-- abcnews-date-text.csv
    
|-- out/ 
    |-- vader_sentiment.csv
    |-- vader_1-week_sentiment.png
    |-- vader_1-month_sentiment.png
    |-- textblob_sentiment.csv
    |-- textblob_1-week_sentiment.png
    |-- textblob_1-month_sentiment.png

|-- src/
    |-- sentiment.py
    
|-- README.md
|-- create_venv.sh
|-- requirements.txt

```

## Usage
**!** The scripts have only been tested on Linux, using Python 3.6.9. 

### 1. Cloning the Repository and Installing Dependencies
To run the script in this repository, I recommend cloning this repository and installing necessary dependencies in a virtual environment. The bash script `create_venv.sh` can be used to create a virtual environment called `venv_sentiment` with all necessary dependencies, listed in the `requirements.txt` file. The following commands can be used:

```bash
# cloning the repository
git clone https://github.com/nicole-dwenger/cdslanguage-sentiment.git

# move into directory
cd cdslanguage-sentiment/

# install virtual environment
bash create_venv.sh

# activate virtual environment 
source venv_sentiment/bin/activate
```

### 2. Data
The data, which was downloaded from [kaggle](https://www.kaggle.com/therohk/million-headlines) and described above, is already stored in the `data/` directory, meaning that when cloning the entire repository it is not necessary to retrieve any data before running the script (instructions for cloning the repository below). 


### 3. Running the Script 
The script `sentiment.py` extracts sentiment scores for each headline in the date, generates daily means and plot 1-week and 1-month rolling averages over time. The script should be called from the `src/` directory: 

```bash
# move into src 
cd src/

# run script with default parameters
python3 sentiment.py

# run script with specified parameters
python3 sentiment.py -l vader -s 2008-01-01

```

__Parameters:__

- `-d, --data`: *str, optional, default:* `../data/abcnews-date-text.csv`\
    File path to data. The script is targeted towards the abc-news data.
    
- `-l, --library`: *str, optional, default:* `textblob`\
   Sentiment library to use for sentiment analysis. Should be either: `textblob` or `vader`. 

- `-s, --start_date`: *str, optional, default:* `2003-02-19`\
  Start date to subset headlines. Earliest is `2003-02-19`.
  
- `-e, --end_date`: *str, optional, default:* `2020-12-31`\ 
  End date to subset headlines. Latest is `2020-12-31`.


__Output__ saved in `out`: 

- `{library}_sentimet.csv`\
  CSV file with columns of publish date, headline and sentiment 
  
- `{library}_1-week_sentiment.png`\
  Plot of the 1-week rolling average sentiment over the specified time and end date. 
  
- `{library}_1-month_sentiment.png`\
  Plot of the 1-month rolling average sentiment over the specified time and end date.
  

## Results and Discussion

The output csv files and images can be found in the `out/` directory. Below are the 1 week average and 1 month rolling sentiment scores using spaCyTextBlob and VADER. It should be noted, that the scale of the y-axis is different in the plots, so the values should be interpreted with caution. 

__1-week-average sentiment scores__

spaCyTextBlob             |  VADER
:-------------------------:|:-------------------------:
![](https://github.com/nicole-dwenger/cdslanguage-sentiment/blob/master/out/textblob_1-week_sentiment.png)  |  ![](https://github.com/nicole-dwenger/cdslanguage-sentiment/blob/master/out/vader_1-week_sentiment.png)


__1-month-average sentiment scores__

spaCyTextBlob             |  VADER
:-------------------------:|:-------------------------:
![](https://github.com/nicole-dwenger/cdslanguage-sentiment/blob/master/out/textblob_1-month_sentiment.png)  |  ![](https://github.com/nicole-dwenger/cdslanguage-sentiment/blob/master/out/vader_1-month_sentiment.png)


Generally, the 1-month rolling average plots seem to reduce some of the noise in the data, and the values vary in a smaller range than they do in the 1-week-rolling average-
Further, the development or trajectory of the sentiment seems to be fairly similar for both TextBlob and VADER. In both cases, and the sentiment seems to decrease between 2004 and 2010, increase between 2010 and 2016, decrease between 2016 and 2020, and increase again in 2020. 

However, it is interesting, that while for TextBlob values were mostly slightly above 0, for VADER they are slightly below 0. VADERs documentation suggests that values between -0.05 and 0.05 are neutral, however it seems that both in the weekly and monthly averages, values are also below -0.05, which would be interpreted as being negative. This might be related to the way the two lexica were constructed. While VADER’s lexicon was built with the help of Amazon Mechanical Turks and is mainly targeted towards social media. TextBlob has both hand-coded and inferred polarity scores, and mainly focuses on adjectives. Thus, it might be that VADER takes into account some nouns which were coded to be positive or negative, which TextBlob does not take into account. This can be considered to be good, as the polarity of those nouns may be biased by those who coded the values, or it can be considered to be bad, that TextBlob is not taking into account those judgements. 

Either way, all of these results should be taken with caution, as these sentiment based analysis have many disadvantages, such as that they only can take into account those words which are part of the lexicon and cannot take into account the context in which the words occur
