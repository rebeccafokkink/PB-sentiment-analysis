# First we install some libraries
from PyPDF2 import PdfReader
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

# We load one of the pdfs for analysis, in this example IPCC, AR6:
reader = PdfReader('IPCC_AR6.pdf')

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
words_IPCC=pd.DataFrame.from_dict(Counter(per_word), orient='index').reset_index()
words_IPCC.columns=['word','freq']

# You can check what it looks like by typing per_word or words_IPCC:
#print(words_IPCC)
# Can you already spot some mistakes? Can you think of pre-processing steps to fix those mistakes?

# We load the file with the sentiment scores (The ANEW lexicon)
sent=pd.read_csv('ANEW.txt',sep='\t',header=None,names=['word','wordnr','ValMN','ValSD','AroMN','AroSD','DomMN','DomSD','Frequency'])
sent.ValMN=sent.ValMN-5

# Check how it looks:
#sent

# Merge the dataframes:
df_IPCCsent= pd.merge(words_IPCC, sent, how="inner", on='word')

# Separate into positive and negative sentiment:
df_IPCCsent['valpos']=df_IPCCsent[df_IPCCsent['ValMN'] >= 0].freq*df_IPCCsent[df_IPCCsent['ValMN'] >= 0].ValMN
df_IPCCsent['valneg']=df_IPCCsent[df_IPCCsent['ValMN'] < 0].freq*df_IPCCsent[df_IPCCsent['ValMN'] < 0].ValMN

# Normalize on number of words: 
AR6_pm_neg = sum(df_IPCCsent[df_IPCCsent['ValMN'] < 0].valneg) / len(per_word)
AR6_pm_pos = sum(df_IPCCsent[df_IPCCsent['ValMN'] >= 0].valpos) / len(per_word)

print(AR6_pm_neg, AR6_pm_pos)