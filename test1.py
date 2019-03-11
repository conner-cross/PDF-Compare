import re
import PyPDF2
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import csv

printable = set(string.printable)
stop_list = set(stopwords.words('english'))
book = "LBW"


def stripNonAlphaNumASCII(text):
    return str(re.compile(r'\W+', re.ASCII).split(text))

def onlyascii(char_in):
    if 48 < ord(char_in) < 127 or ord(char_in) == 46 or ord(char_in) == 32:
        return char_in
    else:
        return ''

def removejunk(text_in):
    text_clean = ''
    for char in text_in:
        check = onlyascii(char)
        text_clean += check
    return text_clean

def getFiles(file_list):
    sent_out = []
    for file in file_list:
        pdffo = open(file, 'rb')
        pdfr = PyPDF2.PdfFileReader(pdffo)

        # discerning the number of pages will allow us to parse through all pages
        num_pages = pdfr.numPages
        count = 0
        text = ""

        # The while loop will read each page
        while count < num_pages:
            pageObj = pdfr.getPage(count)
            count += 1
            text += pageObj.extractText()

        text = text.lower()
        text = removejunk(text)

        # The word_tokenize() function will break our text phrases into individual words
        tokens = word_tokenize(text)

        # we'll create a new list which contains punctuation we wish to clean
        punctuations = ['(', ')', ';', ':', '[', ']', ',', '-', '.', '``', '_', '/', '<', ' ', '?']
        punctuations2 = ['(', ')', ';', ':', '[', ']', ',', '-', '``', '_', '/', '<', ' ']
        # sent_out = text
        # We create a list comprehension which only returns a list of words #that are NOT IN stop_words and NOT IN
        # punctuations.
        keywords = [[word] for word in tokens if not word in stop_list and not word in punctuations]
        sent_out = [[word] for word in tokens if not word in punctuations2]

        # for word in tokens:
        #     sent_out.append([word])
    return keywords, sent_out


if book == "LBW":
    myFiles = ["Last-Bus-to-Wisdom-20.pdf", "Last-Bus-to-Wisdom-21.pdf", "Last-Bus-to-Wisdom-22.pdf",
               "Last-Bus-to-Wisdom-23.pdf", "Last-Bus-to-Wisdom-24.pdf", "Last-Bus-to-Wisdom-25.pdf",
               "Last-Bus-to-Wisdom-26.pdf", "Last-Bus-to-Wisdom-27.pdf", "Last-Bus-to-Wisdom-28.pdf",
               "Last-Bus-to-Wisdom-29.pdf", "Last-Bus-to-Wisdom-30.pdf"]
    textfile = "keywordsLBW.csv"
    sentfile = "sentencesLBW.csv"
elif book == "THS":
    myFiles = ["This-House-of-Sky-1.pdf", "This-House-of-Sky-2.pdf", "This-House-of-Sky-3.pdf"]
    textfile = "keywordsTHS.csv"
    sentfile = "sentencesTHS.csv"
else:
    print("wrong book")


text_out, sentences = getFiles(myFiles)

with open(textfile, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(text_out)
csvFile.close()

with open(sentfile, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(sentences)
    writer.writerows(["."])
csvFile.close()

