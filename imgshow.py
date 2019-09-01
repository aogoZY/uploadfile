# coding: utf-8
from tornado.ioloop import IOLoop
from tornado import web
import shutil
import os
import json
import psycopg2
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    )

dataBaseName = "postgres"
userName = "postgres"
password = "aogo"
host = "localhost"
port = "5432"

def connect_db():
    try:
        conn = psycopg2.connect(database='test', user='postgres',
                                password='aogo', host='127.0.0.1', port=5432)

    except Exception as e:
        logging.error(e)
    else:
        print('connect success')
        return conn
    return None

conn = connect_db()
cursor = conn.cursor()

class User():
    def __init__(self, user_id, img_id):
        self.user_id = user_id
        self.img_id = img_id

    def check_user(self):
        sql = "select user_id from users where user_id ={userID}".format(userID=self.user_id)
        # conn = connect_db()
        # cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        print (rows)
        return rows

    def check_role(self):
        sql = "select role from users where user_id ={userID}".format(userID=self.user_id)
        # conn = connect_db()
        # cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        print (rows[0][0])
        return rows[0][0]

    def check_img(self):
        sql = "select img_id from image where img_id ={imgID}".format(imgID=self.img_id)
        # conn = connect_db()
        # cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        print (rows)
        return rows

    def add_img(self):
        sql = "insert into image values ({imgID} ,'aogo', '/file/aogoimg'} where img_id ={imgID}".format(imgID=self.img_id)
        # conn = connect_db()
        # cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

    def delete_img(self):
        print(self.img_id)
        sql = "delete from image where img_id = {imgID}".format(imgID=self.img_id)
        cursor.execute(sql)
        conn.commit()


class ImgShowHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        logging.info('---get start---')
        user_id = self.get_argument("user_id")
        img_id = self.get_argument("img_id")
        logging.info("the user_id is " + user_id + " and the image_id is " + img_id)
        # 判断user_id是否存在
        user = User(user_id, img_id)
        check_user_result = user.check_user()
        if check_user_result:
            logging.info('the user is existed')
            check_img_result = user.check_img()
            if check_img_result:

                self.write()
                # show the image
                logging.info('the image is existed')
            else:
                logging.error('the image is not correct')
        else:
            logging.error('the user is not correct')


    def post(self, *args, **kwargs):
        logging.info("---post start---")
        user_id = self.get_argument("user_id")
        img_id = self.get_argument("img_id")
        logging.info("the user_id is " + user_id + " and the image_id is " + img_id)
        user = User(user_id, img_id)
        check_user_result = user.check_user()
        if check_user_result:
            logging.info('the user is existed')
            check_role_result = user.check_role()
            if check_role_result == 'True':
                logging.info('the role is administrator')
                check_img_result = user.check_img()
                if check_img_result:
                    logging.info('the image is existed')
                    user.add_img()
                else:
                    logging.error('the image is not correct')
            else:
                logging.error('the role is visitor,u have no right')
        else:
            logging.error('the user is not correct')

    def delete(self, *args, **kwargs):
        logging.info("---delete start---")
        user_id = self.get_argument("user_id")
        img_id = self.get_argument("img_id")
        logging.info("the user_id is " + user_id + " and the image_id is " + img_id)
        user = User(user_id, img_id)
        check_user_result = user.check_user()
        if check_user_result:
            logging.info('the user is existed')
            check_role_result = user.check_role()
            if check_role_result:
                logging.info('the role is administrator')
                check_img_result = user.check_img()
                if check_img_result:
                    logging.info('the image is existed')
                    user.delete_img()
                else:
                    logging.error('the image is not correct')
            else:
                logging.error('the role is visitor，u have no right')
        else:
            logging.error('the user is not correct')



application = web.Application([
    (r'/image', ImgShowHandler),
], autoreload=True)
application.listen(8888)
IOLoop.current().start()
