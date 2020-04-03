import multiprocessing

import requests
from bs4 import BeautifulSoup
import xlwt
import time


# Python程序的执行顺序, 首先执行main()之前出现的非函数定义和非类定义的没有缩进的代码
url = 'https://movie.douban.com/top250?start=%s&filter='
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
n=1

book=xlwt.Workbook(encoding='utf-8',style_compression=0)
sheet=book.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True)
sheet.write(0,0,'名称')
sheet.write(0,1,'图片')
sheet.write(0,2,'排名')
sheet.write(0,3,'评分')
sheet.write(0,4,'作者')
sheet.write(0,5,'简介')

def request_douban(url):
    try:
        # status_code=418 别反爬虫拦截，添加请求头

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None

def save_to_excel(soup):
    list = soup.find(class_='grid_view').find_all('li')

    for item in list:
        item_name = item.find(class_='title').string
        item_img = item.find('a').find('img').get('src')
        item_index = item.find(class_='').string
        item_score = item.find(class_='rating_num').string
        item_author = item.find('p').text.lstrip()
        if(item.find(class_='inq')!=None):
            item_intr = item.find(class_='inq').string

        # print('爬取电影：' + item_index + ' | ' + item_name +' | ' + item_img +' | ' + item_score +' | ' + item_author +' | ' + item_intr )
        print('爬取电影：' + item_index + ' | ' + item_name  +' | ' + item_score  +' | ' + item_intr )

        # UnboundLocalError： local variable 'n' referenced before assignment
        # 在函数外部已经定义了变量n，在函数内部对该变量进行运算，运行时会遇到了这样的错误, 主要是因为没有让解释器清楚变量是全局变量还是局部变量。
        # 因为在函数内部对变量赋值进行修改后，该变量就会被Python解释器认为是局部变量而非全局变量
        # 使用global关键字，在函数内部先声明n这个变量是全局变量

        global n

        sheet.write(n, 0, item_name)
        sheet.write(n, 1, item_img)
        sheet.write(n, 2, item_index)
        sheet.write(n, 3, item_score)
        sheet.write(n, 4, item_author)
        sheet.write(n, 5, item_intr)

        n = n + 1

def main(page):
    html = request_douban(url % (str(page*25)))
    soup = BeautifulSoup(html, 'lxml')
    save_to_excel(soup)


if __name__ == '__main__':
    start = time.time()
    urls = []
    # pool = multiprocessing.Pool(multiprocessing.cpu_count())
    #
    # for page in range(0, 10):
    #     urls.append(url % (str(page * 25)))
    #
    # pool.map(main, urls)
    # pool.close()
    # pool.join()

    for page in range(0, 10):
        main(page)

book.save(u'douban.xlsx')
