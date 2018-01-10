# -*- coding: utf-8 -*-

"""
@purpose: 
@version: 1.0
@author: Roarain
@time: 2018/1/9 9:24
@contact: welovewxy@126.com
@file: zfzx.py
@license: Apache Licence
@site: 
@software: PyCharm
"""

import logging

logging.basicConfig(filename='zfzx.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(level=logging.DEBUG)

import tornado.ioloop
import tornado.web

import MySQLdb
import MySQLdb.cursors
import json
import datetime

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, World!")


class SaleStatistic(tornado.web.RequestHandler):
    def get(self):
        ori_key = '39663e31be065892b5393e1e3547c3c0'
        today = datetime.date.today()
        # start_day = today-datetime.timedelta(days=365)
        start_day = today - datetime.timedelta(days=30)
        end_day = today - datetime.timedelta(days=0)

        str_today = str(today)
        str_start_day = str(start_day)
        str_end_day = str(end_day)
        key = self.get_argument('key', '')
        if key == ori_key:
            hall_name = self.get_argument('hall_name', '辽宁')
            # game_name = self.get_argument('game_name', 'game_lhdb')
            arg_start_day = self.get_argument('start_day', str_start_day)
            arg_end_day = self.get_argument('end_day', str_end_day)
            # sql = "select * from sales_statistics where hall_name like '%s' " % ("%" + hall_name + "%")
            sql = "select * from sales_statistics where hall_name like '%s' and date_time between '%s' and '%s' " % ("%" + hall_name + "%", str(arg_start_day), str(arg_end_day))
            try:
                conn = MySQLdb.connect(
                    user='root',
                    passwd='abcd1234',
                    host='127.0.0.1',
                    port=3306,
                    db='webapp',
                    use_unicode=True,
                    charset='utf8',
                    cursorclass=MySQLdb.cursors.DictCursor,
                )
                cursor = conn.cursor()
                cursor.execute(sql)
                datas = cursor.fetchall()
                counts = cursor.rowcount
                # 把数据类型全部设置为nvarchar(255)，就不需要decode了
                # datas = str(datas).replace('u\'','\'').decode('unicode-escape')
            except Exception as e:
                conn.rollback()
                datas = ''
                counts = ''
            finally:
                conn.close()
                response_string = {
                    'code': '0000000',
                    'message': 'Verify Success',
                    'today': str_today,
                    'start_day': arg_start_day,
                    'end_day': arg_end_day,
                    'sale_statistic': {
                        'counts': counts,
                        'datas': datas,
                    },
                }
        else:
            response_string = {
                'code': '111111',
                'message': 'Verify Failed'
            }
        json_data = json.dumps(response_string, ensure_ascii=False)
        self.write(json_data)
        self.finish()


def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/sale_statistic", SaleStatistic),
        ]
    )
if __name__ == '__main__':
    app = make_app()
    app.listen(9999)
    tornado.ioloop.IOLoop.current().start()