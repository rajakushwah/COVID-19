from tkinter import filedialog
from datetime import date
import requests
import bs4
#import pandas as pd
import csv
import re
#from pandas_profiling import ProfileReport

url='https://www.mygov.in/covid-19/'
html_data=requests.get(url)
bs=bs4.BeautifulSoup(html_data.text,'html.parser')

#No. of cases in INDIA

info_div=bs.find('div',class_='information_row')
info_title=info_div.find('div',class_='info_title')
print(info_title.text+"\n")
print("IndiaFightsCorona COVID-19\n")
all_data=info_div.findAll('div',class_='iblock')
for block in all_data:
    count=block.find('span',class_='icount').get_text()
    text=block.find('div',class_='info_label').get_text()
    print(text+':'+count+'\n')


#testing status in INDIA
print("Testing Status------!!!\n")
info_testing=bs.find('div',class_='testing_block')
#sample
test_sample = info_testing.find('div', class_='testing_sample')
text_sample=test_sample.find('span').get_text()
count_sample=test_sample.find('strong').get_text()
print(text_sample+" is " + count_sample)

#result
box = info_testing.find('div', class_='test_box')
result = info_testing.find('div', class_='testing_result')
text=result.find('span').get_text()
count=result.find('strong').get_text()
print(text+" is " + count+"\n")

#state wise filter

#header
header=['Name of state','Confirmed cases','Active cases','Total Recovered','Death']
header_list=[header]
states_info=header_list
info_div=bs.find('div',class_='information_block')
all_states=info_div.find('div',class_='marquee_data view-content')
#basic info
for block in all_states.findAll('div', class_='views-row'):
   single_state=[]
   for st_name in block.findAll(class_='st_name'):
        st_name=st_name.text
        single_state.append(st_name)
#all_info
   for confirmed in block.findAll(class_='tick-confirmed'):
        confirmed=re.sub("\D", "", confirmed.text)
        single_state.append(confirmed)
   for active in block.findAll(class_='tick-active'):
        active=re.sub("\D", "", active.text)
        single_state.append(active)
   for discharge in block.findAll(class_='tick-discharged'):
        discharge=re.sub("\D", "", discharge.text)
        single_state.append(discharge)
   for death in block.findAll(class_='tick-death'):
        death=re.sub("\D", "", death.text)
        single_state.append(death)
   states_info.append(single_state)
#print(states_info)

print("Please choose the path to download state wise COVID-19 CSV data --")
FolderName = filedialog.askdirectory()
today = date.today()
with open(FolderName+'\\COVID-19 State wise report - '+str(today)+'.csv', 'w',newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(states_info)
    print("Successfully generated the CSV File ---")

#TO Generate Analytics Using pandas_profiling

# df=pd.read_csv(FolderName+'corona_report.csv')
# profile=ProfileReport(df)
# profile.to_file(output_file='Analysis.html')