from os import listdir
from os.path import isfile, join
import json
import pickle
from tqdm import tqdm
from pdf_parser import *
from datetime import datetime

pdf_path = './articoli_conferenza/'



files = [f for f in listdir(pdf_path) if isfile(join(pdf_path, f))]


all_data = []
i = 0

#files = [files[1]] #it was for getting one file, only

print(len(files))
for file in tqdm(files):  
    temp_dic = {'filename':file}
    try:
        file_parser = PDFParser(pdf_path + file)
        try:
            temp_dic['title'] = file_parser.extractTitle()
        except: 
            temp_dic['title'] = "UNABLE TO EXTRACT TITLE"
        temp_dic['abstract'] = file_parser.extractAbstract()
    except: 
        temp_dic['title'] = "Unable to open the pdf"
        temp_dic['abstract'] = "Unable to open the pdf"

    all_data.append(temp_dic) 
    
    i+=1

time_coordinates = str(datetime.now())[0:19].replace(":", "-")

with open(f"jsons/articles_data_{time_coordinates}.json", "w") as out_file:
    json.dump(all_data, out_file)

a = []
t = []
for item in all_data:
    a.append(item['abstract'])
    t.append(item['title'])

out_file = open(f'titoli_pkls/titoli_list_{time_coordinates}.pickle', 'wb')
pickle.dump(t, out_file)
out_file.close()

out_file = open(f'abstract_pkls/abstracts_list_{time_coordinates}.pickle', 'wb')
pickle.dump(a, out_file)
out_file.close()

print(a)