'''Collect data from legacy.com using selenium.'''
import pickle
import re
from time import sleep
from selenium import webDRIVER

WINDOW = True

if WINDOW:
    DRIVER = webDRIVER.Firefox()
else:
    DRIVER = webDRIVER.PhantomJS()
    # Phantomjs binary available at
    # /usr/local/lib/node_modules/phantomjs-prebuilt/lib/phantom/bin/phantomjs


SEARCH_TERM = 'heroin'
LEGACY_PAGE = ('http://www.legacy.com/obituaries/legacy/obituary-search.aspx?'
               'daterange=99999&keyword={}&countryid=0&stateid=all'
               '&affiliateid=all'.format(SEARCH_TERM))


DRIVER.get(LEGACY_PAGE)

result_id = ('ctl00_ctl00_ContentPlaceHolder1_'
             'ContentPlaceHolder1_uxSearchLinks_Message')
results_count = DRIVER.find_elements_by_id(result_id)
results_count = results_count[0].text.split(' ')[0]
if results_count == '1000+':
    num_results = 1000
    open_results_id = ('ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1'
                       '_uxSearchLinks_ViewAllLink')
    DRIVER.find_elements_by_id(open_results_id)[0].click()
else:
    num_results = int(results_count)

obit_dict = {}
# load obit_dict if exists and use it.
# with open(search_term + '.pkl', 'wb') as f:
#     pickle.dump(obit_dict, f, pickle.HIGHEST_PROTOCOL)
obit_dict['birth'] = []
obit_dict['death'] = []
name_dict = {}
obit_dict['obit_text'] = []

read_more_list = ["ReadMore", "readMoreLink"]
obit_text_class = ["ObitTextContent", "full", "ObitTextHtml", "donatic_div"]
bad_word_list = ['heroine', 'Dr.', 'director', 'Director',
                 'Chairman', 'PhD', 'heroines']


def find_content(DRIVER, class_list):
    count = 0
    output = DRIVER.find_elements_by_class_name(class_list[count])
    while len(output) < 1:
        count += 1
        if count >= len(class_list):
            return []
        output = DRIVER.find_elements_by_class_name(class_list[count])
    return output[0]


def test_repeat_name(name, name_dict):
    name = name.lower()
    if name in name_dict:
        return 0, name_dict
    else:
        name_dict[name] = None
        return 1, name_dict


for i in range(num_results):
    name_list = DRIVER.find_elements_by_class_name("obitName")

    # scroll to bottom
    while len(name_list) <= i:
        DRIVER.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        temp = DRIVER.find_elements_by_class_name("obitName")
        if len(temp) == len(name_list):
            sleep(0.5)
        else:
            name_list = temp

    text_list = DRIVER.find_elements_by_class_name("ObitHtml")
    button_links = DRIVER.find_elements_by_class_name("ViewButtonLink")

    name = name_list[i]
    text = text_list[i]
    button = button_links[i]

    # query = '(.+?) \((\d{4}) - (\d{4})\)'
    query = '(.+?) \((\d{4}) - (\d{4})\)'
    found = re.compile(query, re.DOTALL).findall(name.text)
    if len(found) > 0:
        name = found[0][0]
        birth = int(found[0][1])
        death = int(found[0][2])
    else:
        name = name.text
        birth = None
        death = None

    repeat, name_dict = test_repeat_name(name, name_dict)
    if repeat:
        obit_dict['birth'].append(birth)
        obit_dict['death'].append(death)

        try:
            button.click()
        except:
            pass

        read_more = find_content(DRIVER, read_more_list)
        try:
            read_more.click()
        except:
            pass

        obit_text = find_content(DRIVER, obit_text_class)
        if obit_text:
            for bad_words in bad_word_list:
                if obit_text.text.find(bad_words) > -1:
                    print('passed on %s' % name)
                    continue
            obit_dict['obit_text'].append(obit_text.text)
            print('grabbed %s' % name)
        else:
            print('no text for %s' % name)

        while DRIVER.current_url != legacy_page:
            DRIVER.execute_script("window.history.go(-1)")
            # DRIVER.back()

    with open(search_term + '.pkl', 'wb') as f:
        pickle.dump(obit_dict, f, pickle.HIGHEST_PROTOCOL)

DRIVER.close()
