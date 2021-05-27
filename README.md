# Dictionary-Based Sentiment Analysis

[Description](#description) | [Methods](#methods) | [Repository Structure](#repository-structure) | [Usage](#usage) | [Results and Disucssion](#results-and-discussion) | [Contact](#contact)

## Description
> This project relates to Assignment 3: Sentiment Analysis of the course Language Analytics.

Sentiment analysis aims to investigate the sentiment, meaning emotionality or polarity and its temporal development in text. The aim of this project was to investigate sentiment in over a million headlines of the Australian news source ABC from 2003-2020. For this, a script to extract sentiment scores using either the dictionary spaCyTextBlob or VADER was developed. This allowed comparing the two methods and their results. Further, for sentiment scores of both dictionaries, their temporal development was plotted using 1-week and 1-month rolling averages. 


## Methods

### Data
For this project a collection of over a million headlines of the Australia news source ABC (Start Date: 2003-02-19; End Date: 2020-12-31) was used. The data is available on [Kaggle](https://www.kaggle.com/therohk/million-headlines).

### Dictionary-Based Sentiment Anaylsis: SpaCyTextBlob and VADER
Dictionary-based sentiment analyses rely on dictionaries, in which single words are assigned sentiment scores. Two of these dictionaries are spaCyTextBlob and VADER. SpaCyTextBlob returns for any given sentence a score of polarity (positive, negative) and subjectivity (emotionality). For this project, the score of polarity was used, which ranges between -1 (negative) and 1 (positive). VADER returns the probability of a sentence being positive, negative or neutral, and a compound score, an aggregated score of all values. Here, the compound score was used, as it also ranged between -1 (negative) and 1 (positive). For each headline in the data, either the polarity score using spaCyTextBlob or the compound score using VADER was extracted. Subsequently, a daily average was computed, as the data contained multiple headlines per day. These daily averages were then used to calculate rolling averages over one week and one month, which were plotted over time (2003-2020).


## Repository Structure
```
|-- data/                                  # Directory for data
    |-- abcnews-date-text.csv              # Input data of news headlines
    
|-- out/                                   # Directiory for (example) output
    |-- vader_sentiment.csv                # CSV file of sentiment scores for each headline using VADER
    |-- vader_1-week_sentiment.png         # Plot of 1-week rollig average sentiment scores using VADER
    |-- vader_1-month_sentiment.png        # Plot of 1-month rolling average sentiment scores usig VADER
    |-- textblob_sentiment.csv             # CSV file of sentiment scores for each headline using TextBlob
    |-- textblob_1-week_sentiment.png      # Plot of 1-week rollig average sentiment scores using TextBlob
    |-- textblob_1-month_sentiment.png     # Plot of 1-month rolling average sentiment scores usig TextBlob

|-- src/                                   # Directiory for main scripts
    |-- sentiment.py                       # Script for sentiment analysis on headlines, usig TextBlob or VADER
    
|-- README.md
|-- create_venv.sh                         # Bash script to re-create virtual environment
|-- requirements.txt                       # File with necessary dependencies
```

## Usage
**!** The scripts have only been tested on Linux, using Python 3.6.9. 

### 1. Cloning the Repository and Installing Dependencies
To run the script in this repository, I recommend cloning this repository and installing necessary dependencies in a virtual environment. The bash script `create_venv.sh` can be used to create a virtual environment called `venv_sentiment` with all necessary dependencies, listed in the `requirements.txt` file. This will also load the necessary language model from spaCy (`en_core_web_sm`). The following commands can be used:

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
The data, which was downloaded from [kaggle](https://www.kaggle.com/therohk/million-headlines) and described above, is already stored in the `data/` directory. Thus, after cloning the repository no additional data needs to be retrieved to run the script. 

### 3. Running the Script 
The script `sentiment.py` extracts sentiment scores for each headline in the data using either spaCyTextBlob or VADER, generates daily means and plots 1-week and 1-month rolling averages over time. The start and end date of headlines can be adjusted, to reduce processing time or if only a certain time frame is of interest. The script should be called from the `src/` directory: 


```bash
# move into src 
cd src/

# run script with default parameters
python3 sentiment.py

# run script with specified parameters
python3 sentiment.py -d vader -s 2008-01-01

```

__Parameters:__

- `-i, --input_file`: *str, optional, default:* `../data/abcnews-date-text.csv`\
    File path to data. The script is targeted towards the ABC-news data.
    
- `-d, --dictionary`: *str, optional, default:* `textblob`\
   Dictionary to use for sentiment analysis. Should be either: `textblob` or `vader`. 

- `-s, --start_date`: *str, optional, default:* `2003-02-19`\
  Start date to subset headlines in yyyy-mm-dd format. Earliest is `2003-02-19`.
  
- `-e, --end_date`: *str, optional, default:* `2020-12-31`\
  End date to subset headlines in yyyy-mm-dd format. Latest is `2020-12-31`.


__Output__ saved in `out/`: 

- `{dictionary}_sentiment.csv`\
  CSV file with columns of publish date, headline and sentiment.
  
- `{dictionary}_1-week_sentiment.png`\
  Plot of the 1-week rolling average sentiment over the specified time and end date. 
  
- `{dictionary}_1-month_sentiment.png`\
  Plot of the 1-month rolling average sentiment over the specified time and end date.
  

## Results and Discussion
All output can be found in the `out` directory of this repository. Below, the 1-week and 1-month rolling average sentiment scores using spaCyTextBlob or VADER are displayed. It should be noted, that the scale of the y-axis is different in the plots, so the values should be interpreted with caution. 

__1-week-rolling average sentiment scores__

spaCyTextBlob             |  VADER
:-------------------------:|:-------------------------:
![](https://github.com/nicole-dwenger/cdslanguage-sentiment/blob/master/out/textblob_1-week_sentiment.png)  |  ![](https://github.com/nicole-dwenger/cdslanguage-sentiment/blob/master/out/vader_1-week_sentiment.png)


__1-month-rolling average sentiment scores__

spaCyTextBlob             |  VADER
:-------------------------:|:-------------------------:
![](https://github.com/nicole-dwenger/cdslanguage-sentiment/blob/master/out/textblob_1-month_sentiment.png)  |  ![](https://github.com/nicole-dwenger/cdslanguage-sentiment/blob/master/out/vader_1-month_sentiment.png)


Firstly, comparing the 1-week and 1-month rolling averages, the 1-month rolling averages seem to reduce some of the noise (and extreme values) in the data, as the sentiment scores vary within a smaller range of values. Thus, small changes become more apparent, as it’s possible to zoom in on the development. However, across all plots, the development or trajectory of the sentiment seems to be fairly similar. The sentiment scores seem to decrease between 2004 and 2010, increase between 2010 and 2016, decrease between 2016 and 2020, and increase again in 2020. 

Second, looking closer at the actual scores and comparing TextBlob and VADER, it is interesting that values extracted with TextBlob were mostly slightly above 0, while values from VADER were slightly below 0. VADER’s documentation suggests that values between -0.05 and 0.05 are neutral. However, it seems that in both 1-week and 1-month rolling averages, some values are below this threshold, and would thus be considered to indicate negative sentiment. These differences might be related to the way the dictionaries were developed. While VADER’s lexicon was built with the help of Amazon Mechanical Turks and is mainly targeted towards Social Media, TextBlob has both hand-coded and inferred polarity scores, and mainly focuses on adjectives. Thus, VADER might take into account some nouns which were coded to be positive or negative (based on subjective judgement), that TextBlob does not take into account. Thus, it is possible that values of VADER are biased due to personal judgement, or that TextBlob is lacking sentiment for some important words in the dictionary. 

Either way, all of these results should be taken with caution, as these dictionary-based sentiment analyses have many disadvantages, such as that they only can take into account those words which are part of the dictionary and cannot take into account the context in which the words occur (e.g. negation, sarcasm, irony).


## Contact 
If you have any questions, feel free to contact me at 201805351@post.au.dk.
