# Install some libraries
from PyPDF2 import PdfReader
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

#Function to do analysis for all reports
def analysis_function(report, x, y):
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

    # We load the file with the sentiment scores (The ANEW lexicon)
    sent=pd.read_csv('ANEW.txt',sep='\t',header=None,names=['word','wordnr','ValMN','ValSD','AroMN','AroSD','DomMN','DomSD','Frequency'])
    sent.ValMN=sent.ValMN-5

    # Merge the dataframes:
    df_report_sent= pd.merge(words_report, sent, how="inner", on='word')

    # Separate into positive and negative sentiment:
    df_report_sent['valpos']=df_report_sent[df_report_sent['ValMN'] >= 0].freq*df_report_sent[df_report_sent['ValMN'] >= 0].ValMN
    df_report_sent['valneg']=df_report_sent[df_report_sent['ValMN'] < 0].freq*df_report_sent[df_report_sent['ValMN'] < 0].ValMN

    # Arousal scores
    df_report_sent['arousal'] = df_report_sent['freq'] * df_report_sent['AroMN']

    # Normalize on number of words: 
    sentiment_neg = sum(df_report_sent[df_report_sent['ValMN'] < 0].valneg) / len(per_word)
    sentiment_pos = sum(df_report_sent[df_report_sent['ValMN'] >= 0].valpos) / len(per_word)
    arousal_value = sum(df_report_sent['arousal']) / len(per_word)

    sentiment = {'pos': sentiment_pos, 'neg': sentiment_neg, 'arousal': arousal_value}

    return sentiment

# IPBES report analysis
IPBES_2016 = analysis_function('IPBES_2016.pdf',2,22)
IPBES_2019 = analysis_function('IPBES_2019.pdf',3,38)
IPBES_2022 = analysis_function('IPBES_2022.pdf',3,37)

# IPCC report analysis
AR6 = analysis_function('IPCC_AR6.pdf',16,45)

years = [1980]

plt.scatter(
    x= years,
    y= AR6['pos'],
    c='green',
    alpha=0.5,
)

plt.scatter(
    x= years,
    y= AR6['neg'],
    c='red',
    alpha=0.5,
)

plt.title("Sentiment Analysis of IPCC AR6")
plt.legend(["Positive Sentiment", "Negative Sentiment"])
plt.xlabel("Year")
plt.ylabel("Scores")

plt.show()