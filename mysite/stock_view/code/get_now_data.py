import requests
import bs4
import re
def get_1a0001():
    """
    获取上证指数
    :return:
    """
    url1='http://d.10jqka.com.cn/v6/time/hs_1A0001/last.js'
    header={'Referer': 'http://q.10jqka.com.cn/',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'}
    request=requests.get(url1,headers=header)
    regex = re.compile('".+?"', re.MULTILINE)
    js_text = re.findall(regex,request.text)
    regex = re.compile('.+?;', re.MULTILINE)
    js_text = re.findall(regex, js_text[16])
    time_list=list(map(lambda x:x.split(',')[0],js_text))
    shangzhen_list = list(map(lambda x: x.split(',')[1], js_text))
    return time_list,shangzhen_list

def get_399001():
    """
    获取深证指数
    :return:
    """
    url1='http://d.10jqka.com.cn/v6/time/hs_399001/last.js'
    header={'Referer': 'http://q.10jqka.com.cn/',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'}
    request=requests.get(url1,headers=header)
    regex = re.compile('".+?"', re.MULTILINE)
    js_text = re.findall(regex,request.text)
    regex = re.compile('.+?;', re.MULTILINE)
    js_text = re.findall(regex, js_text[16])
    time_list=list(map(lambda x:x.split(',')[0],js_text))
    shenzhen_list = list(map(lambda x: x.split(',')[1], js_text))
    return time_list,shenzhen_list

def get_399006():
    """
    获取创业板指
    :return:
    """
    url1='http://d.10jqka.com.cn/v6/time/hs_399006/last.js'
    header={'Referer': 'http://q.10jqka.com.cn/',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'}
    request=requests.get(url1,headers=header)
    regex = re.compile('".+?"', re.MULTILINE)
    js_text = re.findall(regex,request.text)
    regex = re.compile('.+?;', re.MULTILINE)
    js_text = re.findall(regex, js_text[16])
    time_list=list(map(lambda x:x.split(',')[0],js_text))
    chuangye_list = list(map(lambda x: x.split(',')[1], js_text))
    return time_list,chuangye_list

def get_upAndDown():
    """获取涨跌分布,涨跌停,昨日涨停今日收益"""
    url1 = 'http://q.10jqka.com.cn/api.php?t=indexflash&'
    header = {'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Host': 'q.10jqka.com.cn',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

    session=requests.Session()
    session.get('http://q.10jqka.com.cn/',headers=header)
    request = session.get(url1, headers=header)
    print(request.text)

print(get_upAndDown())
