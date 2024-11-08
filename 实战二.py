from selenium.webdriver import Edge
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv
import pymysql
web = Edge()
web.get('https://search.cnki.com.cn/Search/Result')
time.sleep(2)
inputs = web.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[2]/div[1]/input")
inputs.send_keys('机器学习', Keys.ENTER)
time.sleep(2)
# def save_sql(title, detail, author, public,date, keywords):
#     mydb = pymysql.connect(
#         host="localhost",
#         user="root",
#         password="cmqgjy520.",
#         database="zhiwang")
#     cursor = mydb.cursor()
#     create_table_query = """
#     CREATE TABLE IF NOT EXISTS papers(
#                 title varchar(50) ,
#                 detail text ,
#                 author varchar(50) ,
#                 public varchar(50) ,
#                 date INT ,
#                 keywords varchar(50) )
#     """
#     cursor.execute(create_table_query)
#     sql = """INSERT INTO papers ( title, detail, author, public,date, keywords)
#                            VALUES (%s, %s, %s, %s, %s, %s)"""
#     values = title, detail, author, public, date, keywords
#     cursor.execute(sql, values)
#     mydb.commit()
#
#     mydb.close()
f = open('知网.csv', mode='w', encoding='utf-8', newline='')
title_1 = ['题目', '简介', '作者', '出版社', '日期', '关键字']
csv_writer = csv.writer(f)
csv_writer.writerow(title_1)
for page in range(10):
    list_item = web.find_elements(By.XPATH, '/html/body/div[2]/div/div[1]/div[11]/div[4]/div/div')
    for item in list_item:
        title = item.find_element(By.XPATH, './p[1]/a | ./p[1]/a[1]').text
        # print(title)
        detail = item.find_element(By.XPATH, './p[2]').text
        #print(detail)
        author = item.find_element(By.XPATH, './p[3]/span[1]').text
        #print(key.text)
        public = item.find_element(By.XPATH, './p[3]/a[1]/span | ./p[3]/span[2]').text
        #print(public.text)
        date = item.find_element(By.XPATH, './p[3]/a[2]/span | ./p[3]/span[3]').text
        keywords = item.find_element(By.XPATH, './div').text
        #print(keywords.text)
        csv_writer.writerow([title, detail, author, public, date, keywords])
        #save_sql(title, detail, author, public, date, keywords)
    try:
        next_page = web.find_element(By.XPATH, '//*[@id="PageContent"]/div/div[1]/div[13]/a[11]').click()
        time.sleep(2)
    except:
        break


