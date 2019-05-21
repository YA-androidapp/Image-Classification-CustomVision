#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import requests
import json

# 設定ファイル読み込み
inifile = configparser.ConfigParser()
inifile.read('./.key', 'UTF-8')
url = inifile.get('customvision', 'url')
predictionkey = inifile.get('customvision', 'predictionkey')

# url="https://southcentralus.api.cognitive.microsoft.com/customvision/v2.0/Prediction/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/image?iterationId=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
headers={'content-type':'application/octet-stream','Prediction-Key':predictionkey}


def classify(path):
    try:
        with open(path, 'rb') as images_file:
            response =requests.post(url,data=open("image01.jpg","rb"),headers=headers)
            response.raise_for_status()
            analysis = response.json()
            name, pred = analysis["predictions"][0]["tagName"], analysis["predictions"][0]["probability"]
            print(name, pred)
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def main():
    pass

if __name__ == "__main__":
    main()