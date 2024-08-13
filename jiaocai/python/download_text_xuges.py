import requests
import time
from bs4 import BeautifulSoup


def download_and_dump(url: str):
    output_file = url.split('/')[-1]  #'test.txt'
    output_file = output_file.split('.')[0]
    output_file += '.txt'

    r = requests.get(url)
    #print(r.encoding)
    text = r.content[3:].decode('gb2312', errors='strict') #'gbk')
    soup = BeautifulSoup(text, features="html.parser")
    dump = soup.get_text()

    with open(output_file, 'w', encoding='utf8') as file:
        file.write(dump)  #.encode(encoding='utf-8', errors='ignore')) # errors='strict'))


urls = []

for page in range(8, 25):  # 81
    url = f'https://www.xuges.com/xdmj/laoshe/ltxz/{page:02}.htm'
    try:
        download_and_dump(url)
    except UnicodeError as e:
        print(e)
    time.sleep(1)





#urllib.request.urlretrieve(url, output_file)