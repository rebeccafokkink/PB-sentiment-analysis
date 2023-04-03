# First we install some libraries
from PyPDF2 import PdfReader
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

def analysis_function(report):
    # We load one of the pdfs for analysis, in this example IPCC, AR6:
    reader = PdfReader(report)

    # We make sure all text from the required pages is gathered in a string called 'text':
    text=''
    for i in range(16,45):
        page = reader.pages[i]
        t = page.extract_text()
        text = text + ' ' + t  

    # You can check how it looks by running this cell:
    #text

    # We remove the (){} from all words and we count how often each word occurs and save this in a dataframe called 'words_IPCC'
    text_lower = text.lower()
    per_word = text_lower.split()
    for i in range(len(per_word)):
        for characters in ['1','2','3','4','5','6','7','8','9','0','!','(',')','-','?',',','.','"',':',';','_','[',']','{','}','\n']:
            per_word[i]=per_word[i].replace(characters, '')
        words_report=pd.DataFrame.from_dict(Counter(per_word), orient='index').reset_index()
        words_report.columns=['word','freq']

    # You can check what it looks like by typing per_word or words_report:
    #print(words_report)
    # Can you already spot some mistakes? Can you think of pre-processing steps to fix those mistakes?

    # We load the file with the sentiment scores (The ANEW lexicon)
    sent=pd.read_csv('ANEW.txt',sep='\t',header=None,names=['word','wordnr','ValMN','ValSD','AroMN','AroSD','DomMN','DomSD','Frequency'])
    sent.ValMN=sent.ValMN-5

    # Check how it looks:
    #sent

    # Merge the dataframes:
    df_report_sent= pd.merge(words_report, sent, how="inner", on='word')

    # Separate into positive and negative sentiment:
    df_report_sent['valpos']=df_report_sent[df_report_sent['ValMN'] >= 0].freq*df_report_sent[df_report_sent['ValMN'] >= 0].ValMN
    df_report_sent['valneg']=df_report_sent[df_report_sent['ValMN'] < 0].freq*df_report_sent[df_report_sent['ValMN'] < 0].ValMN
    df_report_sent['arousal'] = df_report_sent['freq'] * df_report_sent['AroMN']

    # Normalize on number of words: 
    sentiment_neg = sum(df_report_sent[df_report_sent['ValMN'] < 0].valneg) / len(per_word)
    sentiment_pos = sum(df_report_sent[df_report_sent['ValMN'] >= 0].valpos) / len(per_word)
    arousal_value = sum(df_report_sent['arousal']) / len(per_word)

    sentiment = [sentiment_neg, sentiment_pos, arousal_value]

    return sentiment

AR6 = analysis_function('IPCC_AR6.pdf')
print(AR6)

#def range(s, e,i):
#   return list(range(s,e,i))

# Driver Code
#start, end, intval = -0.1, 0.1 , 0.001
#ANEW_range = range(start,end,intval)

#plt.plot(AR6, ANEW_range)
#plt.title("Sentiment scores")
#plt.xlabel("Report (year)")
#plt.ylabel("ANEW sentiment")
#plt.savefig("AR6_fig")