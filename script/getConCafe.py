#!/usr/local/bin/python3
from selenium import webdriver
#from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
import datetime
import requests
import re
import smtplib
import sys
from email.mime.text import MIMEText
import configparser
import traceback

def getConCafeData(browser: webdriver, url):
    try:
        # URLにアクセス
        browser.get(url)
        sleep(3)

        # エリアのリンク一覧を配列で取得
        AreaList = browser.find_elements_by_class_name("f-found_link")[0]

        for Area in AreaList:
            Area[0].click()
            sleep(3)
            for Shop in browser.find_elements_by_class_name("free_shop"):
                print(shop.find_elements_by_class_name("shop_name ellipsis"))
                sleep(3)


        # データの取得
        articleElements = browser.find_elements_by_class_name("data")
        contactAddress = articleElements[3].text
        updateDate = articleElements[2].text

        return [contactAddress, updateDate]
    
    except Exception as e:
        return e

def getConfig(filepath, production):
    try:
        config = configparser.ConfigParser()
        config.read(filepath)
        rtn = config.items(production)
        return dict(rtn)
    except Exception as e:
        return e
    

def getArg():
    args = sys.argv
    if len(args) == 2:
        return args[1]
    elif len(args) == 1:
        return "product"
    else:
        return 1



############### メイン処理 ###############
# 【処理概要】設定ファイルで指定したポータルのURLの本文から連絡先一覧を取得し、
#            設定ファイルで指定したwikiのURLをapiで更新する。
#            処理実行日が各月の1日~7日だった場合は、取得した連絡先一覧をメール送信する。
#　 【引数１】設定ファイルのセクション名（string）
#########################################
if __name__ == '__main__':
    try:
        config_file_path = "getConCafe.ini"

        ############### HEADLESSブラウザに接続 ###############
        browser = webdriver.Remote(
            command_executor='http://selenium-hub:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)

        ############### 引数取得 ###############
        config_production = getArg()
        if config_production == 1:
            print("引数の数が不正です。")
            sys.exit(1)
        
        ############### 設定ファイル取得 ###############
        configs = getConfig(config_file_path, config_production)
        if isinstance(configs, Exception):
            print("設定ファイルを取得できませんでした。")
            print(configs.args)
            sys.exit(1)
            
        ############### ecbeingポータルで情報取得 ###############
        ConCafeData = getConCafeData(browser, configs["url"])
        if isinstance(ConCafeData, Exception):
            print("指定されたURLから情報を取得できませんでした。")
            print(contactData.args)
            sys.exit(1)
    
    except Exception as e:
        print("予期せぬエラーが発生しました。")
        print(e.args)

    finally:
        ############### 終了 ###############
        browser.close()
        browser.quit()
        print("処理が終了しました。")
