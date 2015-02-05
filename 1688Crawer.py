#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import io
import sys
import re
import time
import requests
from random import randint
from lxml.html import fromstring
from lxml.etree import tostring
from lxml.html.clean import Cleaner
from itertools import chain
from bs4 import BeautifulSoup
from django.utils.html import remove_tags
from suds.client import Client
from copy import deepcopy


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

locreg = re.compile("实际经营地址:(.*?)\"")


def stringify_children(node):
    parts = ([node.text] +
             list(chain(*([c.text, tostring(c).decode('utf-8'), c.tail] for c in node.getchildren()))) +
             [node.tail])
    # filter removes possible Nones in texts and tails
    return ''.join(filter(None, parts))


def stripy(node):
    cleaner(node)
    return remove_tags(tostring(node, encoding='utf-8').decode('utf-8'), 'div')

cleaner = Cleaner(safe_attrs_only=True, safe_attrs="", allow_tags=['p', 'br', 'table', 'tbody', 'tr', 'td'], remove_unknown_tags=False)


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
                            "zyhy": "餐饮美食",
                            "lxr": "",
                            "xb": "",
                            "zw": "",
                            "lxdh": "0000",
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
                               "fl": "小吃车",
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
                               "khid": -1}}

    baseurl = url
    # url4 = url + "index_4.shtml"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching page:", url, e)
        return None

    response.encoding = 'gbk'
    # print(content)
    parser = BeautifulSoup(response.text)
    tree = fromstring(response.text)
    # for ele in parser.find(class_='conter1 f14px').find_all('p'):
    #     ProjInfo += "\r\n"
    #     ProjInfo += ele.text
    try:
        # ProjName = parser.find(class_='menberIfo bg-A p10-5').find('h1').text.strip()
        CompanyName = parser.find(class_='company-title').text.split()[0]
    except (IndexError, AttributeError) as e:
        print("Error for:", url, e)
        return None

    try:
        result = parser.find((lambda tag: tag.has_attr('map-mod-config')))['map-mod-config']
        Location = locreg.search(result).groups(1)[0]
    except (IndexError, AttributeError) as e:
        print("Get ProjInfo Error:", url, e)
        return None

    try:
        Industry = parser.find('td', text='主营行业').find_next().text.strip()
    except (IndexError, AttributeError) as e:
        print("Get industry error:", url, e)
        Industry = ""

    try:
        ContactPerson = tree.xpath("/html/body/div[1]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[2]/div[1]/div[1]/div[2]/dl/dd[1]/text()")[0].split()[0]
    except IndexError as e:
        print("Get ContactPerson Error:", url, e)
        ContactPerson = ""

    try:
        Phone = tree.xpath("/html/body/div[1]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[2]/div[1]/div[1]/div[2]/dl/dd[2]/text()")[0].split()[0]
    except IndexError as e:
        print("Get Phone Number Error:", url, e)
        Phone = ""

    try:
        Brand = parser.find('td', text='品牌名称').find_next().text.split()[0]
    except (IndexError, AttributeError) as e:
        print("Find Brand Error:", url, e)
        Brand = ""

    try:
        StaffNumber = parser.find('td', text='员工人数').find_next().text.strip()
    except (IndexError, AttributeError) as e:
        print("IndexError:", url, e)
        StaffNumber = ""

    try:
        CompanyIntro = parser.find(id='company-more').text.strip()
    except (IndexError, AttributeError) as e:
        print("Error for:", url, e)
        return None
        
    # print(CompanyIntro)

    Project['custinfo']['khmc'] = CompanyName
    Project['custinfo']['gsjj'] = CompanyIntro
    Project['custinfo']['sourceurl'] = baseurl
    Project['custinfo']['gsgm'] = StaffNumber
    Project['projectinfo']['khmc'] = CompanyName
    Project['projectinfo']['ppmc'] = Brand
    Project['projectinfo']['sjhm'] = Phone
    Project['projectinfo']['jyms'] = Industry
    # Project['projectinfo']['xmjs'] = ProjInfo
    Project['custinfo']['lxr'] = ContactPerson
    Project['projectinfo']['lxr'] = ContactPerson
    Project['custinfo']['lxdh'] = Phone
    Project['custinfo']['jyfw'] = Industry
    Project['projectinfo']['szqy'] = Location
    Project['custinfo']['szqy'] = Location
    return Project
    # print("Name is:", Name)
    # print("Type is:", Type)
    # print("Address is:", Address)
    # print("Contact is:", Contact)
    # print("Introduction is:", Intro)

nameRegx = re.compile("[(.*)]")


CategoryList = [
    "墙艺", "装饰装修", "采暖", "门窗", "地板", "建筑贴膜",
    "油漆", "水晶建材", "五金配件", "楼梯", "瓷砖", "吊顶"]

regionDict = {"东北": ["黑龙江省", "吉林省", "辽宁省"],
              "华北": ["北京市", "天津市", "河北省", "山西省", "内蒙古自治区"],
              "华中": ["河南省", "湖南省", "湖北省"],
              "华东": ["上海市", "江苏省", "浙江省", "福建省", "山东省", "江西省","安徽省", "台湾"],
              "西南": ["四川省", "云南省", "重庆市", "贵州省", "西藏自治区"],
              "西北": ["新疆自治区", "陕西省", "甘肃省", "宁夏自治区", "青海省"],
              "华南": ["广东省", "广西省", "海南省"]}

regionList = ["黑龙江省", "吉林省", "辽宁省",
              "北京市", "天津市", "河北省", "山西省", "内蒙古自治区",
              "河南省", "湖南省", "湖北省",
              "上海市", "江苏省", "浙江省", "福建省", "山东省", "江西省", "安徽省",
              "台湾", "四川省", "云南省", "重庆市", "贵州省", "西藏自治区",
              "新疆自治区", "陕西省", "甘肃省", "宁夏自治区", "青海省",
              "广东省", "广西省", "海南省"]


def main():
    Item = {"id": -1,
            "xmmc": "",
            "xmid": -1,
            "cpmc": "",
            "cpfl": "",
            "cpxxxx": "",
            "cptp": ""}


    baseUrl = "http://s.1688.com/company/company_search.htm"
    client = Client("http://tongji.1958.cc:8105/CommonWebService.asmx?WSDL")
    thekey = client.factory.create('SecurityToken')
    thekey.Key = "5pu56YeR6Imz77ya4oCc6ZSA5Yag4oCd55qE5oiQ6ZW/5Y+y"
    client.set_options(soapheaders=thekey)
    with open("1688.json", 'w', encoding='utf-8') as f:
        for i in range(1, 50):
            print(i, flush=True)
            payload = {"beginPage": str(i), "keywords": "小吃车".encode('gbk')}
            r = requests.get(baseUrl, params=payload)
            r.encoding = 'gbk'
            tree = fromstring(r.text)
            # elements = tree.xpath("/html/body/div[1]/div[2]/div[1]/div[2]/div/ul/li[1]")
            elements = tree.find_class("company-list-item")
            for node in elements:
                time.sleep(randint(0, 4))
                try:
                    ProjUrl = node.xpath("div[1]/div[2]/div[3]/div[1]/div[4]/a[3]")[0].attrib['href']
                except:
                    continue
                # print(ProjUrl)
                # if ProjUrl.split("/")[-1] == "zshb.html":
                #     continue
                # logoLink = node[0][0].attrib['src']
                # infoNode = node.getnext()
                # try:
                #     Category = infoNode[1][0][0].text
                #     for kind in CategoryList:
                #         if kind in Category:
                #             Category = kind
                #         else:
                #             Category = "其他"
                # except IndexError:
                #     print("Get category error")
                #     Category = "其他"
                # try:
                #     Area = infoNode[1][0][1][0].text
                #     if Area == "全国":
                #         pass
                #     else:
                #         for (key, vals) in regionDict.items():
                #             if Area in vals:
                #                 break
                #             else:
                #                 Area = "全国"
                # except IndexError:
                #     Area = "全国"
                # try:
                #     Location = infoNode[1][1][1].text.split("：")[1]
                #     for place in regionList:
                #         if Location.startswith(place):
                #             Location = place
                #             break
                # except IndexError:
                #     Location = ""
                result = getInfo(ProjUrl)
                if not result:
                    continue
                for node in node.xpath("div[2]/div/div[2]/ul/li/a"):
                    ItemUrl = node.attrib['href']
                    try:
                        response = requests.get(ItemUrl)
                        response.raise_for_status()
                    except requests.exceptions.RequestException as e:
                        print("Error fetching page:", ItemUrl, e)
                        return None
                    response.encoding = 'gbk'
                    parser = BeautifulSoup(response.text)
                    tree = fromstring(response.text)
                    itemName = ""
                    imgLink = ""
                    itemInfo = ""
                    try:
                        itemName = parser.find('h1').text
                        imgLink = tree.xpath("/html/body/div[1]/div[2]/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[3]/div/div[1]/div/div/div/div/div[1]/div/a/img")[0].attrib['src']
                        itemInfo = stripy(tree.xpath("/html/body/div[1]/div[2]/div/div[3]/div/div[1]/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/table")[0])
                    except (IndexError, AttributeError) as e:
                        print("Error getting item info:", ItemUrl, e)
                    Item['cpmc'] = itemName
                    Item['cptp'] = imgLink
                    Item['cpxxxx'] = itemInfo
                    result['projectinfo']['items'].append(deepcopy(Item))
    
                result['projectinfo']['xmlogo'] = result['projectinfo']['items'][0]['cptp']
                # print(json.dumps(result, ensure_ascii=False), flush=True)
                try:
                    client.service.Router(json.dumps(result))
                except Exception as e:
                    print("Router Error:", ProjUrl, e)
                json.dump(result, f, ensure_ascii=False)
                print("\n", file=f)

if __name__ == '__main__':
    main()


# print json.dumps(getInfo("http://www.shang360.com/item/51768/"))
