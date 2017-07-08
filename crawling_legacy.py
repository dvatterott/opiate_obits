import requests
import re

header_data = {
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)'
        ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 '
        'Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9'
        ',image/webp,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive'
    }

search_term = 'opiate'

legacy_page = '''http://www.legacy.com/obituaries/legacy/obituary-search.aspx?
daterange=99999&keyword={}&countryid=0&stateid=all
&affiliateid=all'''.format(search_term)

response = requests.get(legacy_page, headers=header_data)

dt_query = '<a href=".+?">.+? \((\d{4})-(\d{4})\)</a>'
age_list = re.compile(dt_query, re.DOTALL).findall(response.text)
