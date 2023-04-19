# Install some libraries
from PyPDF2 import PdfReader
import pandas as pd
from collections import Counter

# Load ANEW lexicon
ANEW = pd.read_csv('ANEW.TXT', sep='\t', header=None, names=['word', 'wordnr', 'ValMN', 'ValSD', 'AroMN', 'AroSD', 'DomMN', 'DomSD', 'Frequency'])

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
    pos_words = df_report_sent[df_report_sent['ValMN'] >= 5]['word'].tolist()
    neg_words = df_report_sent[df_report_sent['ValMN'] < 5]['word'].tolist()

    # Count the total number of positive and negative words:
    pos_count = sum(words_report[words_report['word'].isin(pos_words)]['freq'])
    neg_count = sum(words_report[words_report['word'].isin(neg_words)]['freq'])
    
    return pos_count, neg_count

#IPBES reports analysis
IPBES_2016 = analysis_function('IPBES_2016.pdf', 2, 22, ANEW)
IPBES_2019 = analysis_function('IPBES_2019.pdf', 3, 38, ANEW)
IPBES_2022 = analysis_function('IPBES_2022.pdf', 2, 37, ANEW)

print(IPBES_2016)
print(IPBES_2019)
print(IPBES_2022)

# IPCC reports analysis
IPCC_2001 = analysis_function('IPCC_2001.pdf', 2, 34, ANEW)
IPCC_2007 = analysis_function('IPCC_2007.pdf', 2, 22, ANEW)
IPCC_2014 = analysis_function('IPCC_2014.pdf', 2, 32, ANEW)
IPCC_2023 = analysis_function('IPCC_2023.pdf', 4, 36, ANEW)

print(IPCC_2001)
print(IPCC_2007)
print(IPCC_2014)
print(IPCC_2023)

# ozone reports analysis
ozone_1985 = analysis_function('ozone_1985.pdf', 2, 26, ANEW)
ozone_1998 = analysis_function('ozone_1998.pdf', 7, 19, ANEW)
ozone_2006 = analysis_function('ozone_2006.pdf', 19, 37, ANEW)
ozone_2014 = analysis_function('ozone_2014.pdf', 17, 43, ANEW)
ozone_2022 = analysis_function('ozone_2022.pdf', 10, 48, ANEW)

print(ozone_1985)
print(ozone_1998)
print(ozone_2006)
print(ozone_2014)
print(ozone_2022)