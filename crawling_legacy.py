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

obit_dict = {}
obit_dict['birth'] = []
obit_dict['death'] = []
obit_dict['obit_text'] = []

read_more_list = ["ReadMore", "readMoreLink"]
obit_text_class = ["ObitTextContent", "full"]


def find_content(driver, class_list):
    count = 0
    output = driver.find_elements_by_class_name(class_list[count])
    while len(output) < 1:
        count += 1
        if count >= len(class_list):
            return []
        output = driver.find_elements_by_class_name(read_more_list[count])
    return output[0]


for i in range(num_results):
    name_list = driver.find_elements_by_class_name("obitName")

    # scroll to bottom
    while len(name_list) < i:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        temp = driver.find_elements_by_class_name("obitName")
        if len(temp) == len(name_list):
            sleep(0.5)
        else:
            name_list = temp

    text_list = driver.find_elements_by_class_name("ObitHtml")
    button_links = driver.find_elements_by_class_name("ViewButtonLink")

    name = name_list[i]
    text = text_list[i]
    button = button_links[i]

    # query = '(.+?) \((\d{4}) - (\d{4})\)'
    query = '\((\d{4}) - (\d{4})\)'
    found = re.compile(query, re.DOTALL).findall(name.text)
    if len(found) > 0:
        obit_dict['birth'].append(int(found[0][0]))
        obit_dict['death'].append(int(found[0][1]))
    else:
        obit_dict['birth'].append(None)
        obit_dict['death'].append(None)
    # obit_dict['obit_text'].append(text.text)
    button.click()

    read_more = find_content(driver, read_more_list)
    try:
        read_more.click()
    except:
        pass

    obit_text = find_content(driver, obit_text_class)
    obit_dict['obit_text'].append(obit_text.text)

    driver.execute_script("window.history.go(-1)")
    driver.back()

# driver.close()
