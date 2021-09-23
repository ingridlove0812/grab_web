import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd

class grab():
    def __init__(self, srt_date, end_date):
        self.url = 'https://cn.investing.com/instruments/HistoricalDataAjax'
        self.request_headers = {
            'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47',
            'content-type':'application/x-www-form-urlencoded',
            'X-Requested-With':'XMLHttpRequest'
        }
        self.parameters = {
            'curr_id':6408,
            'smlID':1159963,
            'header':'AAPL历史数据',
            'st_date':srt_date,
            'end_date':end_date,
            'interval_sec':'Daily',
            'sort_col':'date',
            'sort_ord':'DESC',
            'action':'historical_data',
        }

    def run(self):
        r = requests.post(self.url, headers = self.request_headers, data = self.parameters)
        soup = BeautifulSoup(r.text, "html.parser")
        col = [c for c in re.sub(' ','\n',soup.find(['thead','th']).text).split('\n') if c != '']
        dict1 = {key: [] for key in range(1,8)}
        dict2 = {}
        i = 1; l = 1
        for listing in soup.find_all('tr'):
            if l == len(soup.find_all('tr')):
                for values in listing.find_all('td'):
                    dict2[values.text.split(':')[0]] = values.text.split(':')[1]
            else:
                for values in listing.find_all('td'):
                    dict1[i].append(values.text)
                    i += 1
                    if i % 7 == 1:
                        i = 1
            l += 1
        table1 = pd.DataFrame.from_dict(dict1)
        table1.columns = col
        dict_final = {key: {} for key in ['table1','table2']}
        dict_final['table1'] = table1.to_dict(orient='split')
        dict_final['table2'] = dict2
        return dict_final

# result = grab('2021/09/13','2021/09/14').run()
