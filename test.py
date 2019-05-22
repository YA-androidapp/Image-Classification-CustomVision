#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2019 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.

from glob import glob
import configparser
import datetime
import json
import os
import requests


scrpath = os.path.abspath(os.path.dirname(__file__))
os.chdir(scrpath)

# このスクリプトと同じディレクトリにtestフォルダを作成、
# そのサブディレクトリに訓練データと検証データからなるデータセットを格納
root_test_dirname = 'test'

# テスト結果を出力するテキストファイル名
nowstr = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
result_filename = 'result-test-'+nowstr+'.txt'

# 正答率評価のための変数
count_items_all = 0
count_items_correct = 0

# 設定ファイル読み込み
inifile = configparser.ConfigParser()
inifile.read('./.key', 'UTF-8')
url = inifile.get('customvision', 'url')
predictionkey = inifile.get('customvision', 'predictionkey')

# url='https://southcentralus.api.cognitive.microsoft.com/customvision/v2.0/Prediction/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/image?iterationId=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
headers = {'content-type': 'application/octet-stream',
           'Prediction-Key': predictionkey}


def classify(path):
    try:
        with open(path, 'rb') as images_file:
            response = requests.post(
                url, data=open(path, 'rb'), headers=headers)
            response.raise_for_status()
            analysis = response.json()
            name, pred = analysis['predictions'][0]['tagName'], analysis['predictions'][0]['probability']
            print(name, pred)
            return name
    except Exception as e:
        print('[Err] {0}'.format(e))
    return ''


def main():
    global count_items_all
    global count_items_correct

    # テスト用画像取得
    subdirs = glob(os.path.join(
        scrpath, root_test_dirname, '**'))
    for subdir in subdirs:
        if os.path.isdir(subdir):
            print('sub directory: {}'.format(subdir), datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
            testdatas = glob(os.path.join(subdir, '*.png'))
            count_testfile = 0
            answer = os.path.basename(subdir)
            for testdata in testdatas:
                print('  {} {:.2%} {}'.format(
                    answer, (count_testfile/len(testdatas)), testdata), datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
                label = classify(testdata)

                count_testfile += 1
                count_items_all += 1
                if label == answer:
                    count_items_correct += 1

    if count_items_all > 0:
        mes = 'Complete. accuracy:{} / {} = {:.2%}'.format(
            count_items_correct, count_items_all, count_items_correct / count_items_all)
    else:
        mes = 'Complete.'
    mes += ' ' + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    print(mes)
    with open(os.path.join(scrpath, result_filename), mode='a') as f:
        f.write(mes + '\n')



if __name__ == '__main__':
    main()
