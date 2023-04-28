# Install some libraries
from PyPDF2 import PdfReader
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

ANEW = pd.read_csv('ANEW.TXT', sep='\t', header=None, names=['word', 'wordnr', 'ValMN', 'ValSD', 'AroMN', 'AroSD', 'DomMN', 'DomSD', 'Frequency'])

# Function to do analysis for one report
def analyze_report(report_path, page_start, page_end, ANEW):
    # Load PDF and extract text from pages
    reader = PdfReader(report_path)
    text = ''
    for i in range(page_start, page_end):
        page = reader.pages[i]
        t = page.extract_text()
        text = text + ' ' + t  
    
    # Process text and calculate sentiment scores
    text_lower = text.lower()
    per_word = text_lower.split()
    for i in range(len(per_word)):
        for characters in ['1','2','3','4','5','6','7','8','9','0','!','(',')','-','?',',','.','"',':',';','_','[',']','{','}','\n']:
            per_word[i]=per_word[i].replace(characters, '')
    words_report=pd.DataFrame.from_dict(Counter(per_word), orient='index').reset_index()
    words_report.columns=['word','freq']
    df_report_sent= pd.merge(words_report, ANEW, how="inner", on='word')
    df_report_sent['sentiment'] = df_report_sent['ValMN'].apply(lambda x: 1 if x >= 5 else 0)
    
    return df_report_sent


# Function to plot subplots for one environmental report
def plot_subplots(report_filenames, page_ranges, ANEW, name):
    num_reports = len(report_filenames)
    fig, axs = plt.subplots(num_reports, figsize=(4, 4*num_reports))
    
    for i in range(num_reports):
        # Extract report name from file name
        report_name = report_filenames[i].split('_')[0]

        fig.suptitle(f"Sentiment Scores Distribution for {report_name} Reports")

        # Extract year from file name
        year = report_filenames[i].split('_')[1]
        year = year[:4]  # Take only the first 4 characters as the year

        df_report_sent = analyze_report(report_filenames[i], *page_ranges[i], ANEW)
        pos_scores = df_report_sent[df_report_sent['sentiment'] == 1]['ValMN']
        neg_scores = df_report_sent[df_report_sent['sentiment'] == 0]['ValMN']
        axs[i].set_ylim(1, 9)
        violin_parts = axs[i].violinplot([pos_scores, neg_scores], showmeans=True, widths = 0.8)
        odd = 0
        for vp in violin_parts['bodies']:
            if odd:
                vp.set_facecolor('Red')
            else:
                vp.set_facecolor('Green')
            odd += 1

        axs[i].set_title(year)
        axs[i].set_ylabel('Sentiment Score')
        axs[i].set_xticks([1, 2])
        axs[i].set_xticklabels(['Positive', 'Negative'])
        #axs[i].set_aspect(1)

    # Adjust the spacing between the subplots
    fig.subplots_adjust(hspace=0.3)
    plt.savefig(name)
    plt.show()

IPBES_violin_subplots = ['IPBES_2016.pdf', 'IPBES_2019.pdf', 'IPBES_2022.pdf']
page_ranges = [(2, 22), (3, 38), (3, 37)]
plot_subplots(IPBES_violin_subplots, page_ranges, ANEW, 'IPBES_violin.png')

IPCC_violin_subplots = ['IPCC_2001.pdf', 'IPCC_2007.pdf', 'IPCC_2014.pdf', 'IPCC_2023.pdf']
page_ranges = [(2, 34), (2, 22), (2, 32), (4, 36)]
plot_subplots(IPCC_violin_subplots, page_ranges, ANEW, 'IPCC_violin.png')

ozone_violin_subplots = ['ozone_1985.pdf', 'ozone_1998.pdf', 'ozone_2006.pdf', 'ozone_2014.pdf', 'ozone_2022.pdf']
page_ranges = [(2, 26), (7, 19), (19, 37), (17, 43), (10, 48)]
plot_subplots(ozone_violin_subplots, page_ranges, ANEW, 'ozone_violin.png')