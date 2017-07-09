from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
from math import ceil
from time import sleep

window = True

if window:
    driver = webdriver.Firefox()
else:
    driver = webdriver.PhantomJS()

search_term = 'opiate'
legacy_page = '''http://www.legacy.com/obituaries/legacy/obituary-search.aspx?
daterange=99999&keyword={}&countryid=0&stateid=all
&affiliateid=all'''.format(search_term)

driver.get(legacy_page)

result_id = ('ctl00_ctl00_ContentPlaceHolder1_'
             'ContentPlaceHolder1_uxSearchLinks_Message')
results_count = driver.find_elements_by_id(result_id)
num_results = int(results_count[0].text.split(' ')[0])

# scroll to bottom
name_list = [0]
while len(name_list) < num_results:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    temp = driver.find_elements_by_class_name("obitName")
    if len(temp) == len(name_list):
        sleep(0.5)
    else:
        name_list = temp

obit_dict = {}
obit_dict['birth'] = []
obit_dict['death'] = []
obit_dict['obit_text'] = []

name_list = driver.find_elements_by_class_name("obitName")
text_list = driver.find_elements_by_class_name("ObitHtml")
print(len(name_list))

# for name, text in zip(name_list, text_list):
#     # query = '(.+?) \((\d{4}) - (\d{4})\)'
#     query = '\((\d{4}) - (\d{4})\)'
#     found = re.compile(query, re.DOTALL).findall(name.text)
#     obit_dict['birth'].append(int(found[0][0]))
#     obit_dict['death'].append(int(found[[0][1]]))
#     obit_dict['obit_text'].append(text.text)

# driver.close()
