"""
    Version: 1.0
    Author: Ecoplay 김유빈
    Create Date: 2021.02.26
    Last Update Date: 2021.02.26
"""

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib import parse
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import os.path


def crawling(keyword: str = '환경교육', page_number: int = 5, types: str = 'txt'):
    if keyword is None or keyword.strip() == '':
        keyword = '환경교육'
    if types is None or types.strip() == '':
        types = 'txt'

    data_list = []
    current_time = datetime.datetime.now()
    url = 'https://www.google.com/search?hl=ko&tbm=nws&q='
    query = parse.quote(keyword)
    urls = ''
    for i in range(0, page_number * 10, 10):
        req = Request(url + query + '&start=' + str(i), headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req)
        source = html.read()
        html.close()
        soup = BeautifulSoup(source, 'html.parser')
        main_div = soup.find(id="main")
        start_div = main_div.select_one("div").find_next_sibling("div")
        for_div = start_div
        main_divs = []
        while True:
            for_div = for_div.find_next_sibling("div")
            if for_div is None:
                break
            else:
                main_divs.append(for_div)

        for main_div_ in main_divs:
            # URL Parsingx
            a_tag = main_div_.find('a')
            a_tag_url = a_tag.attrs['href']
            url_start = 'url?q='
            url_start_index = a_tag_url.find(url_start)
            url_end = '&sa=U'
            url_end_index = a_tag_url.find(url_end)
            if url_end_index < 0:
                url_end = '&sa=u'
                url_end_index = a_tag_url.find(url_end)
            __url_parsed = a_tag_url[url_start_index + len(url_start):url_end_index]
            __url_parsed = parse.unquote(__url_parsed)
            urls.join(__url_parsed)

            a_tag_divs = a_tag.find_all('div')
            # Title Parsing
            __a_tag_title = a_tag_divs[0].get_text()

            # Company Parsing
            __a_tag_company = a_tag_divs[1].get_text()

            # Content & Day Parsing
            divs_text = main_div_.find('div').find('div').find_next_siblings('div')
            div_text = ''
            for divs_ in divs_text:
                div_text = divs_.get_text()
                if div_text != '':
                    break
            __div_date = div_text[0:div_text.find('·')].rstrip()
            __div_content = div_text[div_text.find('·') + 1:].lstrip()

            if __div_date.find('분') > 0:
                __div_date = current_time - datetime.timedelta(minutes=int(__div_date[:__div_date.find('분')]))
            elif __div_date.find('시간') > 0:
                __div_date = current_time - datetime.timedelta(hours=int(__div_date[:__div_date.find('시간')]))
            elif __div_date.find('일') > 0:
                __div_date = current_time - datetime.timedelta(days=int(__div_date[:__div_date.find('일')]))
            elif __div_date.find('주') > 0:
                __div_date = current_time - datetime.timedelta(weeks=int(__div_date[:__div_date.find('주')]))
            elif __div_date.find('개월') > 0:
                __div_date = current_time - relativedelta(months=int(__div_date[:__div_date.find('개월')]))
            elif __div_date.find('년') > 0:
                __div_date = current_time - relativedelta(years=int(__div_date[:__div_date.find('년')]))
            else:
                __div_date = current_time
            data_list.append(
                [__div_date.strftime('%Y년%m월%d일 %H시%M분'), __a_tag_title, __div_content, __url_parsed, __a_tag_company])

    directory = 'crawling'
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_name = './' + directory + '/' + current_time.strftime('%Y-%m-%d %H-%M') + ' ' + keyword
    if types == 'txt':
        # To txt
        file_name = file_name + '.txt'
        f = open(file_name, 'w', encoding='utf-8')
        for lists in data_list:
            for index, data in enumerate(lists):
                if index == 0:
                    f.write('날짜 : ')
                elif index == 1:
                    f.write('제목 : ')
                elif index == 2:
                    f.write('내용 : ')
                elif index == 3:
                    f.write('URL : ')
                elif index == 4:
                    f.write('회사 : ')
                f.write(data + '\n')
            f.write('\n--------------------------------------------------\n\n')
        f.close()
    else:
        # To Excel
        df = pd.DataFrame(data_list, columns=['날짜', '제목', '내용', 'URL', '회사'])

        file_name = file_name + '.xlsx'
        df.to_excel(excel_writer=file_name, sheet_name=keyword)
