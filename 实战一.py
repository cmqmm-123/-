from concurrent.futures import ThreadPoolExecutor

import pymysql
import requests
from bs4 import BeautifulSoup
import csv


f = open('movie.csv', mode='w', encoding='utf-8', newline='')
title = ['名次', '电影名称', '导演', '编剧', '主演', '剧情', '地区', '评分']
csv_writer = csv.writer(f)
csv_writer.writerow(title)

#111.6.43.154:3128

# mydb = pymysql.connect(
#     host="localhost",
#     user="root",
#     password="cmqgjy520.",
#     database="douban250"
#     )
#
# cursor = mydb.cursor()
# create_table_query = """
#             CREATE TABLE IF NOT EXISTS movies(
#                         top varchar(20) ,
#                         title1 varchar(50) ,
#                         director varchar(50) ,
#                         bianju varchar(50)  ,
#                         actor varchar(50) ,
#                         a_type  varchar(50) ,
#                         area varchar(50) ,
#                         grade  varchar(50) )
#
#             """
#
# cursor.execute(create_table_query)
# mydb.commit()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 SLBrowser/9.0.5.8121 SLBChan/111 SLBVPV/64-bit'}


def main_html(url):
    resp = requests.get(url, headers=headers)
    c_text = resp.text
    soup = BeautifulSoup(c_text, 'html.parser')
    main = soup.find_all('div', class_='pic')
    for i1 in main:
        a = (i1.find('a'))
        c_url = a.get('href')
        c_resp = requests.get(c_url, headers=headers)
        c_soup = BeautifulSoup(c_resp.text, 'html.parser')
        content = c_soup.find_all('div', id="info")
        top = c_soup.find('span', class_='top250-no').text
        title1 = c_soup.find('h1').text
        data = c_soup.find_all('span', class_='attrs')
        director = data[0].text
        bianju = data[1].text
        actor = data[2].text
        type = c_soup.find_all('span', property="v:genre")
        a_type = [z.text for z in type]
        area = c_soup.find('span', class_="pl", string='制片国家/地区:').next_sibling.strip()
        grade = c_soup.find('strong', class_="ll rating_num").text
        csv_writer.writerow([top, title, director, bianju, actor, a_type, area, grade])
        # insert_query = """INSERT INTO movies ('top','title1','director','bianju','actor','a_type','area','grade')
        #                                         VALUES (%s, %s, %s, %s, %s, %s,%s, %s,%s)"""
        # values = (top, title1, director, bianju, actor, a_type, area, grade)
        # cursor.execute(insert_query, values)
        # mydb.commit()


if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 SLBrowser/9.0.5.8121 SLBChan/111 SLBVPV/64-bit'}

    with ThreadPoolExecutor(50) as t:
        for i in range(0, 250, 25):
            t.submit(main_html, f'https://movie.douban.com/top250?start={i}&filter=')

    print('ok')
# mydb.close()
