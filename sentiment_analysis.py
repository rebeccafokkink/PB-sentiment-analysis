# Install some libraries
from PyPDF2 import PdfReader
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

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

# IPBES reports analysis
IPBES_2016 = analysis_function('IPBES_2016.pdf', 2, 22, ANEW)
IPBES_2019 = analysis_function('IPBES_2019.pdf', 3, 38, ANEW)
IPBES_2022 = analysis_function('IPBES_2022.pdf', 2, 37, ANEW)

# IPCC reports analysis
IPCC_2001 = analysis_function('IPCC_2001.pdf', 2, 34, ANEW)
IPCC_2007 = analysis_function('IPCC_2007.pdf', 2, 22, ANEW)
IPCC_2014 = analysis_function('IPCC_2014.pdf', 2, 32, ANEW)
IPCC_2023 = analysis_function('IPCC_2023.pdf', 4, 36, ANEW)

# ozone reports analysis
ozone_1985 = analysis_function('ozone_1985.pdf', 2, 26, ANEW)
#ozone_1994 = analysis_function('ozone_1994.pdf', 13, 24, ANEW) (creates an error)
ozone_2006 = analysis_function('ozone_2006.pdf', 19, 37, ANEW)
ozone_2014 = analysis_function('ozone_2014.pdf', 17, 43, ANEW)
ozone_2022 = analysis_function('ozone_2022.pdf', 10, 48, ANEW)

# create DataFrame for IPBES reports
IPBES_data = pd.DataFrame({'x': [2016, 2019, 2022],
                   'y1': [IPBES_2016[0], IPBES_2019[0], IPBES_2022[0]],
                   'y2': [IPBES_2016[1], IPBES_2019[1], IPBES_2022[1]],
                   'z': [IPBES_2016[2], IPBES_2019[2], IPBES_2022[2]]})

years_datetime_IPBES = pd.to_datetime(IPBES_data['x'], format='%Y') # converting list into datetime format

plt.scatter(IPBES_data.x, IPBES_data.y1, s=100, c=IPBES_data.z, cmap='viridis', marker='d')
plt.scatter(IPBES_data.x, IPBES_data.y2, s=100, c=IPBES_data.z, cmap='viridis')

plt.title("Sentiment & Arousal Analysis of IPBES reports (2016-2022)")
plt.legend(["Positive Sentiment", "Negative Sentiment"])
plt.xlabel("Year")
plt.ylabel("Sentiment Scores")

plt.colorbar(label = 'Arousal Score')

plt.savefig('IPBES_analysis.png')