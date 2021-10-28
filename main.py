import re
import requests
from lxml.html import etree
import pandas as pd
import time
from rich.progress import track



id_pattern = re.compile('data-article-id="(.*?)">')
title_pattern = re.compile('<title>(.*?) - PubMed</title>')
page_max = int(input('需要爬多少页'))
find_title = input('检索关键词')
find_abstract = input('摘要关键词，多个词组之间用英文逗号分隔').split(',')
#print(find_abstract)
L = []


for page in track(range(1, page_max + 1)):
    time.sleep(1)
    #print('第{}页'.format(page))
    url = str('https://pubmed.ncbi.nlm.nih.gov/?term=' + str(find_title) + '&page=' + str(page))
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'ncbi_sid=8A1A740617608901_0381SID; pmc.article.report=; _ga=GA1.2.248246895.1635125439; pm-csrf=83wP0rXYWVchXoGnutEiFymbwahssaUcb5ZxHSIUcu7ZNw9KmUAGZQheG6pXSMiG; pm-sessionid=fv6lze8oh454vg28dfiib9h05ws6x8cq; _gid=GA1.2.115086200.1635333676; _gat_ncbiSg=1; _gat_dap=1; pm-iosp=; pm-sfs=; ncbi_pinger=N4IgDgTgpgbg+mAFgSwCYgFwgAwCEDsAHNiQIwCiAYlQCKEDMArCSQEyUBs5p2AggCwVslAHSkRAWzisQAGhABXAHYAbAPYBDVEqgAPAC6ZQMrGAUAjCVHTz6mcBas2Q/ewGcoGiAGNE0NwoqhvKM9nIgpKT2UfKs2PZ4RCwU1JR0TCzY7Fw8AkKi4lIysVGmjtYYZpYVHl6+/oH6GAByAPLN5OGsJg7VqCJK3ubIAyoSA8iIIgDmajBdAJz2cfyE4fTxWJGMxSD0pSAra7Y9kaS79HZYAGYaKh7rrlj6EApQ62tY60tYrAuEjFC8n4mz22A4jGOLiuOBE+zE4X4T0Uqk02j0wRcoSw8RCMPOpCBIEYyIWJPCjA4CQp+Gp8g4B0BRI4VKwtR8iBAAF8uUA==',
    'referer': url,
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
    }
    #print (url)
    t = 1
    while t :
        try :
            r = requests.get(url,headers = headers)
        except:
            pass
        else :
            t = 0
    
    data = id_pattern.findall(r.text)
    if not data:
        break
    for i in data:
        url_article = 'https://pubmed.ncbi.nlm.nih.gov/{}/'.format(i)
        t = 1
        while t :
            try:
                r_article = requests.get(url_article)
            except:
                pass
            else:
                t = 0
        html = etree.HTML(r_article.text)
        title = (title_pattern.findall(r_article.text))[0]
        abs_xpaths = html.xpath('//*[@id="abstract"]/div/*')
        Abs = ''
        for abs_xpath in abs_xpaths:
            text = abs_xpath.xpath('./text()')
            text = text[-1].replace('\n', '').strip()

            TEXT = abs_xpath.xpath('./*/text()')
            TEXT = TEXT[-1].replace('\n', '').strip() if TEXT else ''

            Abs += TEXT + text + '\n'
        for a in find_abstract:
            if a in Abs:
                L.append([title, Abs, url_article])
                break

pd.DataFrame(L).to_excel('1.xlsx')
print("All finish")
