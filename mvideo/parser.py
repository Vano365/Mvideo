import requests
import json
import time
import sqlite3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class MvideoParser():

    def __init__(self):
        self.cookies = ''

    def get_cookies(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36")
        options.add_argument("--disable-blink-features=AutomationControlled")
        browser = webdriver.Chrome(options=options)
        browser.set_window_size(1920,1080)
        browser.get("https://www.mvideo.ru/")
        cookies = browser.get_cookies()
        for cookie in cookies:
            try:
                self.cookies += cookie['name'] + '=' + cookie['value'] + ';'
            except KeyError:
                continue
        browser.quit()

    def add_table_product(self, product, conn):
        cursor = conn.cursor()
        rating = product['rating']
        if rating['star'] == None and rating['count'] == None:
            rating['star'] = 0
            rating['count'] = 0
        cursor.execute(f"SELECT * FROM reviews_product")
        rows = cursor.fetchall()
        ids = []
        for row in rows:
            ids.append(row[2])
        id = product['productId']
        url = f"https://www.mvideo.ru/products/{str(id)}"
        if id not in ids:
            cursor.execute(f"INSERT INTO reviews_product(name, sku_id, rating, reviews_amount, url) VALUES('{product['name']}', '{product['productId']}', {rating['star']}, {rating['count']}, '{url}')")
        conn.commit()

    def add_table_review(self, review, conn, sku_id):
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM reviews_review")
        rows = cursor.fetchall()
        ids = []
        for row in rows:
            ids.append(row[10])
        if review['reviewId'] not in ids:
            cursor.execute(f"SELECT * FROM reviews_product WHERE sku_id='{sku_id}'")
            product_id = cursor.fetchall()[0][0]

            cursor.execute(f"INSERT INTO reviews_review(name, date, comment, pros, cons, likes, dislikes, rating, product_id, review_id) VALUES(?, '{review['date']}', ?, ?, ?, {review['like']}, {review['dislike']}, {review['score']}, {product_id}, '{review['reviewId']}')", (review['name'], str(review['text']).strip(), review['benefits'], review['drawbacks']))
        else:
            cursor.execute(f"UPDATE reviews_review SET likes={review['like']}, dislikes={review['dislike']} WHERE review_id='{review['reviewId']}'")
        conn.commit()

    def get_list_products(self, categoryId):
        headers = {
            'accept': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': self.cookies,
        }
        limit = '24'
        params = (
            ('categoryId', str(categoryId)),
            ('offset', '0'),
            ('limit', limit),
        )

        response = requests.get('https://www.mvideo.ru/bff/products/listing', headers=headers, params=params)
        try:
            soup = json.loads(response.text)['body']
        except KeyError:
            return response.text

        total = soup['total']
        max_iter = total // 24 + 1
        print("Всего страниц: " + str(max_iter))

        result = []
        conn = sqlite3.connect('mvideo/db.sqlite3')
        for iter in range(max_iter + 1):
            print("Страница - " + str(iter))
            time.sleep(1)
            params = (
                ('categoryId', str(categoryId)),
                ('offset', str(iter * 24)),
                ('limit', limit),
            )
            try:
                response = requests.get('https://www.mvideo.ru/bff/products/listing', headers=headers, params=params)
                products_site = json.loads(response.text)['body']['products']
                for p in products_site:
                    response = requests.get(f'https://www.mvideo.ru/bff/product-details?productId={str(p)}', headers=headers)
                    product = json.loads(response.text)['body']
                    self.add_table_product(product, conn)

                    response = requests.get(f'https://www.mvideo.ru/bff/reviews/product?productId={str(p)}', headers=headers)
                    soup = json.loads(response.text)['body']

                    for s in soup['reviews']:
                        try:
                            self.add_table_review(s, conn, product['productId'])
                        except Exception as e:
                            print(str(e))
                            continue
            except:
                continue
        return products

def main():
    parser = MvideoParser()
    parser.get_cookies()
    products = parser.get_list_products(205)

if __name__ == '__main__':
    main()
