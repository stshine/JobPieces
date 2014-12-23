#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import io
import sys
import urllib2
import requests
from lxml import etree
from bs4 import BeautifulSoup

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def getInfo(url):
    Project = {"Key": "",
               "DLL": "",
               "custinfo": {"id": -1,
                            "khmc": "",
                            "szqy": "",
                            "khlx": "",
                            "jyms": "",
                            "jyfw": "",
                            "zczb": "",
                            "fr": "",
                            "khwz": "",
                            "dz": "",
                            "clrq": "",
                            "zblx": "",
                            "gsgm": "",
                            "ywy": "",
                            "zyhy": "",
                            "lxr": "",
                            "xb": "",
                            "zw": "",
                            "lxdh": "",
                            "sj": "",
                            "dzyx": "",
                            "gsjj": "",
                            "sourceurl": "",
                            "cssstring": "",
                            "cssimage": "",
                            "Remark": "",
                            "Tag": ""},
               "projectinfo": {"items": [],
                               "id": -1,
                               "khmc": "",
                               "xmmc": "",
                               "fl": "",
                               "ppmc": "",
                               "szqy": "",
                               "jhxm": "",
                               "ywy": "",
                               "tzje": "",
                               "mdsl": -1,
                               "clrq": "",
                               "jyms": "",
                               "zsdx": "",
                               "zsqy": "",
                               "xmjs": "",
                               "scfx": "",
                               "jmfs": "",
                               "xmlogo": "",
                               "sjhm": "",
                               "gddh": "",
                               "cz": "",
                               "dzyx": "",
                               "lxr": "",
                               "khid": -1}
           }
    Item = {"id": -1,
            "xmmc": "",
            "xmid": -1,
            "cpmc": "",
            "cpfl": "",
            "cpxxxx": "",
            "cptp": ""}
    # url1 = url + "index_1.html"
    url2 = url + "index_2.html"
    url3 = url + "index_3.html"
    url4 = url + "index_4.html"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print("HTTP Error:", response.status_code)
            return
    except urllib2.error.HTTPError as e:
        print("Error fetching page:", url, e.reason)
        return
    response.encoding = 'utf-8'
    # print(content)
    parser = BeautifulSoup(response.text)
    ProjInfo = parser.find(class_='art1_con').text
    ItemList = parser.find(id='a-img').find_all('li')
    Category = parser.find(class_='abf0').b.text
    CompanyName = parser.find(class_='a336 bold').a.text
    VestAmout = parser.find(class_="right list9").contents[3].contents[1]
    ProjName = parser.find(id="container4").find_all('a')[2]['title']

    try:
        response = requests.get(url2)
        if response.status_code != 200:
            print("HTTP Error:", response.status_code)
            return
    except urllib2.HTTPError as e:
        print("Error fetching page:", url, e.reason)
        return
    response.encoding = 'utf-8'
    parser = BeautifulSoup(response.text)
    CompanyIntro = parser.find(class_="art1_con").text

    try:
        response = requests.get(url3)
        if response.status_code != 200:
            print("HTTP Error:", response.status_code)
            return
    except urllib2.HTTPError as e:
        print("Error fetching page:", url, e.reason)
        return
    response.encoding = 'utf-8'
    parser = BeautifulSoup(response.text)
    JoinIntro = parser.find(class_="art1_con").text

    try:
        response = requests.get(url4)
        if response.status_code != 200:
            print("HTTP Error:", response.status_code)
            return
    except urllib2.HTTPError as e:
        print("Error fetching page:", url, e.reason)
        return
    response.encoding = 'utf-8'
    parser = BeautifulSoup(response.text)
    ProfitAnal = parser.find(class_="art1_con").text
    Project['custinfo']['khmc'] = CompanyName
    Project['custinfo']['gsjj'] = CompanyIntro
    Project['custinfo']['zyhy'] = Category
    Project['projectinfo']['xmmc'] = ProjName
    Project['projectinfo']['khmc'] = CompanyName
    Project['projectinfo']['tzje'] = VestAmout
    Project['projectinfo']['fl'] = Category
    Project['projectinfo']['xmjs'] = ProjInfo
    Project['projectinfo']['scfs'] = ProfitAnal
    Project['projectinfo']['jmfs'] = JoinIntro
    for i in ItemList:
        imgLink = i.img['src']
        Item['xmmc'] = ProjName
        Item['cpmc'] = ProjName
        Item['cptp'] = imgLink
        Project['projectinfo']['items'].append(Item)
    return Project
    # print("Name is:", Name)
    # print("Type is:", Type)
    # print("Address is:", Address)
    # print("Contact is:", Contact)
    # print("Introduction is:", Intro)


def main():
    baseUrl = "http://www.shang360.com/search/"
    for i in range(1, 853):
        payload = {"search": "输入关键词进行搜索", "page": str(i)}
        r = requests.get(baseUrl, params=payload)
        r.encoding = 'utf-8'
        tree = etree.HTML(r.text)
        elements = tree.xpath("/html/body/div[6]/div[1]/ul[1]/li/span[1]/font/a")
        
        for node in elements:
            ProjUrl = node.attrib['href']
            logoLink = node[0].attrib['src']
            result = getInfo(ProjUrl)
            result['xmlogo'] = logoLink

# print json.dumps(getInfo("http://www.shang360.com/item/51768/"))
