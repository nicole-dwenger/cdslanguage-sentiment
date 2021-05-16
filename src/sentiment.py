#!/usr/bin/env python

"""
Script to calculate sentiment scores of news headlines using TextBlob or VADER, and
save sentiment scores in csv file and generate plots of rolling averages 

Steps:
  - Get sentiment score for each headline in the data using TextBlob or VADER
  - Save csv with date, headline and sentiment score 
  - Resample by getting an average sentiment for each day
  - Calculate rolling means for 1 week and 1 months
  - Visualise rolling means in plots
  
Input:
  - -d, --data_path, str, optional, default: ../data/abcnews-date-text.csv, path to datafile
  - -l, --library, str, optional, default: textblob, should be either "textblob" or "vader"
  - -s, --start_date, str, optional, default: 2003-02-19, start date to get sentiment scores for in yyyy-mm-dd
  - -e, --end_date, str, optional, default: 2020-12-3, end date to get sentiment scores for in yyyy-mm-dd

Output saved in out/:
  - {library}_sentiment.csv: csv file with publish_date, headline, sentiment score
  - {library}_1-week_sentiment.png: plot with 1 week rolling average from start-end date
  - {library}_1-month_sentiment.png: plot with 1 month rolling average from start-end date
"""

# LIBRARIES ---------------------------------------------------

# Basics
import os
import argparse
from tqdm import tqdm

# Data and visualisation
import pandas as pd
import matplotlib.pyplot as plt

# Spacy and nltk
import spacy 
from spacytextblob.spacytextblob import SpacyTextBlob
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


# MAIN FUNCTION -----------------------------------------------
 
def main():
    
    # --- ARGUMENT PARSER AND OUTPUT DIRECTORY ---
    
    # Initialise argument parser
    ap = argparse.ArgumentParser()
    
    # Add input options for file path for input data and 
    ap.add_argument("-d", "--data_path", help = "Path to input file",
                    required = False, default = "../data/abcnews-date-text.csv")
    
    ap.add_argument("-l", "--library", help = "Library: 'textblob' or 'vader'",
                    required = False, default = "textblob")
    
    ap.add_argument("-s", "--start_date", help = "Start date in yyyy-mm-dd",
                    required = False, default = "2003-02-19")
    
    ap.add_argument("-e", "--end_date", help = "End date in yyyy-mm-dd",
                    required = False, default = "2020-12-31")
    
    # Retrieve iput arguments
    args = vars(ap.parse_args())
    data_path = args["data_path"]
    library = args["library"]
    start_date = args["start_date"]
    end_date = args["end_date"]
    
    # Prepare output directory
    out_directory = os.path.join("..", "out")
    if not os.path.exists(out_directory):
        os.mkdir(out_directory)
    
    # --- SENTIMENT ANALYSIS ---
    
    # Print message
    print(f"\nInitialising sentiment analysis for {data_path} from {start_date} to {end_date} using {library}")
    
    # Load data to pandas df, with publish date as index, and parsed as date time
    df = pd.read_csv(data_path, index_col=["publish_date"], parse_dates=["publish_date"])
    # Filter out dates by start and end date
    df = df.loc[start_date:end_date]        
  
    # Get sentiment scores as list based on input
    if library == "textblob":
        sentiment_scores = get_textblob_sentiments(df, "headline_text")
    elif library == "vader":
        sentiment_scores = get_vader_sentiments(df, "headline_text")
        
    # Append the sentiment_scores to the dataframe as sentiment
    df = df.assign(sentiment = sentiment_scores)
    
    # Save dataframe with sentiment scores in output directory
    out_df = os.path.join(out_directory, f"{library}_sentiment_scores.csv")
    df.to_csv(out_df, index = True)

    # --- PLOTTING ---
    
    # Print message
    print(f"Sentiment scores are calculated, now generating plots.")
    
    # Calculate average sentiment score for each day
    df_daily_sentiment = df.resample("1d").mean()
    
    # Generate and save plots in output directory
    rolling_sentiment_plot("7d", "1-week", df_daily_sentiment, out_directory, library)
    rolling_sentiment_plot("30d", "1-month", df_daily_sentiment, out_directory, library)
    
    # Print message
    print(f"Done! CSV file and plots are in {out_directory}.\n ")

    
# HELPER FUNCTIONS --------------------------------------------

def get_textblob_sentiments(df, text_column):
    """
    Get sentiments for each row in text_column of dataframe using spaCyTextBlob
    Append all polarity scores to a list
    Input: 
      - df: dataframe with each doc in a row
      - text_column: column name in df of texts
    Returns:
      - sentiment_scores: list of polarity scores 
    """
    # Load spacy model
    spacy_nlp = spacy.load("en_core_web_sm")
    
    # Initialise TextBlob and add to pipe
    spacy_text_blob = SpacyTextBlob()
    spacy_nlp.add_pipe(spacy_text_blob)
    
    # Create empty target list to store sentiment scores
    sentiment_scores = []
    
    # Apply sentiment analysis to each headline in the data
    for doc in spacy_nlp.pipe(tqdm(df[text_column]), batch_size = 500):
        # Retrieve polarity score
        sentiment = doc._.sentiment.polarity
        # Append sentiment score to target list
        sentiment_scores.append(sentiment)
        
    return sentiment_scores


def get_vader_sentiments(df, text_column):
    """
    Get sentiments for each row in text_column of dataframe using VADER
    Append all compound scores to a list
    Input: 
      - df: dataframe with each doc in a row
      - text_column: column name in df of texts
    Returns:
      - sentiment_scores: list of compound scores 
    """
    # Load vader lexicon
    nltk.download("vader_lexicon")
    # Initialise sentiment anlayser
    vader_sentiment = SentimentIntensityAnalyzer()
    
    # Create empty target list to store sentiment scores
    sentiment_scores = []

    # Iterate over dataframe
    for index, row in tqdm(df.iterrows(), total = df.shape[0]):
        # Get polarity scores for each row in the text_column
        sentiment = vader_sentiment.polarity_scores(row[text_column])
        # Extract only the compound score
        compound = sentiment["compound"]
        # Append compound score to target list
        sentiment_scores.append(compound)
        
    return sentiment_scores
    
    
def rolling_sentiment_plot(time_window, time_label, df, out_directory, library):
    """
    Plotting the rolling sentiment scores for a given time window, 
    and saving plot in output directory
    Input:
      - time_window: time window to generate rolling means for
        in pd datetime format, e.g. 7d, 30d
      - time_label: description of time window for plot label
      - df: dataframe containing "publish_date" column and "sentiment_score"
      - out_directory: path to output directory
    Saves .png of plot in out_directory
    """
    
    # Calculate rolling mean over time window
    rolling_df = df.sort_index().rolling(time_window).mean()
    
    # Initialise plot 
    plt.figure()
    # Plot the smoothed data values
    plt.plot(rolling_df["sentiment"], label = f"{time_label} rolling average")
    # Add title, x label and y label and legend to the plot
    plt.title(f"Sentiment [{library}] over time with a {time_label} rolling average")
    plt.xlabel("Date")
    plt.xticks(rotation=45)
    plt.ylabel(f"Sentiment score")
    plt.legend(loc="upper right")
    
    # Save figure as png in output
    plt.savefig(os.path.join(out_directory, f"{library}_{time_label}_sentiment.png"), bbox_inches='tight')
    
    
if __name__=="__main__":
    main()
