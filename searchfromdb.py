# -*- coding: utf-8 -*-
# @File  : searchfromdb.py
# @Author: FanLu
# @Date  : 2021/8/21

# 利用数据库中的文件查询《国语辞典》中的汉字
# 台湾正体和大陆简体通用

import pymysql.cursors
import opencc
import pyperclip3 as pc

def query_by_word(word):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='lf123456',
                                 database='dictsdb',
                                 cursorclass=pymysql.cursors.DictCursor)
    # 大陆简体转台湾正体
    converter = opencc.OpenCC('s2twp.json')
    word = converter.convert(word)
    # 台湾正体转大陆简体
    converter = opencc.OpenCC('tw2sp.json')

    with connection:
        with connection.cursor() as cursor:
            # read records
            sql = "SELECT * FROM `dict_tb_all_backup` WHERE `name` = %s"
            cursor.execute(sql, (word,))
            # result = cursor.fetchone()
            results = cursor.fetchall()
            tw_str = ''
            results = sorted(results, key = lambda e : e['pinyin'])
            for result in results:
                han_pinyin = '漢語拼音 ' + result['pinyin'] if result['pinyin'] != None else '漢語拼音 '
                meaning = '釋義\n' + result['meaning']
                if len(results) == 1:
                    tw_str = han_pinyin + '\n\n' + meaning + '\n\n'
                    break
                tw_str = tw_str + han_pinyin + '\n\n' + meaning + '\n\n'
            sp_str = converter.convert(tw_str)
            total_str = tw_str + '---\n\n' + sp_str
            return total_str[:-2]

if __name__ == '__main__':
    # 此处输入查询汉字
    word = '齐'
    total_str = query_by_word(word)

    print(total_str)
    pc.copy(total_str)
