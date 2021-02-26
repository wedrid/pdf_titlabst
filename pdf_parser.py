import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
import io
import pdftitle
import unicodedata
import re


class PDFParser():
    def __init__(self, filepath):
        #print(filepath)
        self.filepath = filepath
        self.pdfparser(filepath)
    
    def extractTitle(self):
        return self.removeUnwantedCharachters(pdftitle.get_title_from_file(self.filepath))
        
        #print("Here")
        #print(a)
        
    def extractAbstract(self):
        self.abstrI = self.text.find('abstract')
        #print(f"Abstract {self.abstrI}")
        self.introI = self.text.find('introduction')
        #print(f"Introduction {self.introI}")
        
        
        self.abstract = self.text[self.abstrI+9:self.introI-3]
        self.abstract = self.removeUnwantedCharachters(self.abstract)
        
        if '(cid:' in self.abstract: 
            self.abstract = "UNABLE TO DECODE ABSTRACT"
        return self.abstract

    def removeUnwantedCharachters(self, stringa):
        stringa = unicodedata.normalize("NFKD", stringa)
        
        #re.sub(u'\\\\u\d\d\d\d', self.abstract, "") #FIXME cercare modo per toglire di torno le cose tipo \u2019
        
        stringa = stringa.replace("- ", "").replace('\n', ' ').replace('.','').replace(',','').replace("'", "").replace('"', "")
        #boh l'espressione regolare non riesco a farla funzionare..
        stringa = stringa.replace(" \u2014", ' ').replace(' \u2192', '').replace('\u2022', '').replace(" \u00a9", "").replace(" \u201920", '').replace(" \u00a9", '').replace(" \u00b7", '')
        rem_list = ['\u201c', '\u201d', '\u2014', '\u0301e', '\u2019', '\u2018']
        for item in rem_list: 
            stringa = stringa.replace(item, "")
        
        return stringa

    def pdfparser(self, data, numberOfWantedPages = 1):

        fp = open(data, 'rb')
        rsrcmgr = PDFResourceManager()
        retstr = io.StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, laparams=laparams)
        # Create a PDF interpreter object.
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # Process each page contained in the document.
        i = 0
        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)
            data =  retstr.getvalue()
            i += 1
            if i >= numberOfWantedPages:
                break

        self.text = data.lower()
        #print(self.text)
