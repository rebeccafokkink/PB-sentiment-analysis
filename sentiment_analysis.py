# Install some libraries
from PyPDF2 import PdfReader
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

# Load ANEW lexicon
ANEW = pd.read_csv('ANEW.TXT', sep='\t', header=None, names=['word', 'wordnr', 'ValMN', 'ValSD', 'AroMN', 'AroSD', 'DomMN', 'DomSD', 'Frequency'])
ANEW.ValMN = ANEW.ValMN - 5

#Function to do analysis for all reports
def analysis_function(report, x, y, ANEW):
    # We load one of the pdfs for analysis
    reader = PdfReader(report)

    # We make sure all text from the required pages is gathered in a string called 'text':
    text=''
    for i in range(x,y):
        page = reader.pages[i]
        t = page.extract_text()
        text = text + ' ' + t  

    # We remove the special characters from all words, make them lower case
    # and we count how often each word occurs and save this in a dataframe
    text_lower = text.lower()
    per_word = text_lower.split()
    for i in range(len(per_word)):
        for characters in ['1','2','3','4','5','6','7','8','9','0','!','(',')','-','?',',','.','"',':',';','_','[',']','{','}','\n']:
            per_word[i]=per_word[i].replace(characters, '')
        words_report=pd.DataFrame.from_dict(Counter(per_word), orient='index').reset_index()
        words_report.columns=['word','freq']

    # Merge the dataframes:
    df_report_sent= pd.merge(words_report, ANEW, how="inner", on='word')

    # Separate into positive and negative sentiment:
    df_report_sent['valpos']=df_report_sent[df_report_sent['ValMN'] >= 0].freq*df_report_sent[df_report_sent['ValMN'] >= 0].ValMN
    df_report_sent['valneg']=df_report_sent[df_report_sent['ValMN'] < 0].freq*df_report_sent[df_report_sent['ValMN'] < 0].ValMN

    # Arousal scores
    df_report_sent['arousal'] = df_report_sent['freq'] * df_report_sent['AroMN']

    # Normalize on number of words: 
    sentiment_neg = sum(df_report_sent[df_report_sent['ValMN'] < 0].valneg) / len(per_word)
    sentiment_pos = sum(df_report_sent[df_report_sent['ValMN'] >= 0].valpos) / len(per_word)
    arousal_value = sum(df_report_sent['arousal']) / len(per_word)

    analysis_scores = [sentiment_pos, sentiment_neg, arousal_value]

    return analysis_scores

# IPCC report analysis
AR6 = analysis_function('IPCC_AR6.pdf',16,45, ANEW)

# IPBES report analysis
IPBES_2016 = analysis_function('IPBES_2016.pdf', 2, 22, ANEW)
IPBES_2019 = analysis_function('IPBES_2019.pdf', 3, 38, ANEW)
IPBES_2022 = analysis_function('IPBES_2022.pdf', 2, 37, ANEW)

IPBES_reports = [IPBES_2016, IPBES_2019, IPBES_2022]  # create a list of IPBES report data

print(AR6)
print(IPBES_2016)
print(IPBES_2019)
print(IPBES_2022)

IPBES_reports = [IPBES_2016, IPBES_2019, IPBES_2022]  # create a list of IPBES report data

# Creating scatter plots 

years_IPCC = [2023, 2023]

years_IPBES = [2016, 2016, 2019, 2019, 2022, 2022]

fig, axs = plt.subplots(1, 2, figsize=(10, 5), sharey=True)

# Scatter plot for IPCC reports
axs[0].scatter(years_IPCC, AR6[0], c= None, cmap='viridis', alpha=0.5, marker="d")
axs[0].scatter(years_IPCC, AR6[1], c= None, cmap='viridis', alpha=0.5)

# Scatter plot for IPBES reports
#arousal_map = {0: (0, 1, 0), 1: (1, 1, 0), 2: (1, 0, 0)}  # dictionary for mapping arousal values to colors

for i, IPBES_report in enumerate(IPBES_reports):
    axs[1].scatter(years_IPBES, IPBES_report[0], c=IPBES_report[2], alpha=0.5, marker="d")
    axs[1].scatter(years_IPBES, IPBES_report[1], c=IPBES_report[2], alpha=0.5)

axs[0].set_title("Sentiment Analysis of IPCC AR6")
axs[1].set_title("Sentiment and Arousal Analysis of IPBES 2016-2022")
axs[0].set_xlabel("Year")
axs[1].set_xlabel("Year")
axs[0].set_ylabel("Scores")
axs[1].set_ylabel("Scores")
axs[0].legend(["Positive Sentiment", "Negative Sentiment"])
axs[1].legend(["Positive Sentiment", "Negative Sentiment"])

plt.show()