#!/usr/bin/env python2

from __future__ import unicode_literals
import numpy as np
import cv2
import io
import sys
import urllib2
from StringIO import StringIO
import gzip
import re
import chardet.chardetect
from lxml import etree


def CheckBorder(image):
    if np.array_equal(image[0,0:-1], image[-1,0:-1]) and np.array_equal(image[0:-1,0], image[0:-1, -1]):
        pass;
    else:
        return False
    # print image.shape
    mask = np.zeros(image.shape, np.uint8)
    mask[:,:] = image[0,0]
    inverted = cv2.subtract(mask, image)
    # gray = cv2.cvtColor(inverted, cv2.COLOR_BGR2GRAY)
    points = np.transpose(np.nonzero(inverted))
    # rect = cv2.minAreaRect(points)
    rect = cv2.boundingRect(points)
    x, y, w, h = rect
    if (w/image.shape[0] < 0.7) and (h/image.shape[1] < 0.7):
        return True
    else:
        return False

defaultUrl = "http://www.3158.cn/static/img/xiangmu/0.1/logo_default_120x90.png"

f = open("borderUrl.txt", 'w')

def checkPage(url):
    try:
        response = urllib2.urlopen(url)
        # buf = io.BytesIO(response.read())
        # f = gzip.GzipFile(fileobj=buf, mode='rb')
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO( response.read())
            zip = gzip.GzipFile(fileobj=buf)
            content = zip.read()
        else :
            content = response.read()
    except urllib2.HTTPError as e:
        print("Error fetching page:", url, e.reason)
        return False
        # exit(1)
    tree = etree.HTML(content)
    # print content
    imgList = tree.xpath("/html/body/div[3]/div[1]/ul/li/dl/dt/a")
    # print imgList
    for element in imgList:
        ProjUrl = element.attrib['href']
        imageurl = element[0].attrib['src']
        if imageurl == defaultUrl:
            print ProjUrl
            print >> f, ProjUrl
            return True
            # print imageurl
        try:
            response = urllib2.urlopen(imageurl)
            imgcont = response.read() #.decode('utf-8')
        except urllib2.HTTPError as e:
            print("Error fetching image:", imageurl, e.reason)
            continue;
            # exit(1)
        # print response.getcode()
        picture = cv2.imdecode(np.asarray(bytearray(imgcont), np.uint8), 0)
        if picture is None:
            print ProjUrl
            print >> f, ProjUrl
            return True
        if CheckBorder(picture):
            print ProjUrl
            print >> f, ProjUrl
            return True
    return False

TheDict = {
    "http://www.3158.cn/xiangmu/zhongcan/": 1395,
    "http://www.3158.cn/xiangmu/xiaochi/": 2021,
    "http://www.3158.cn/xiangmu/kuaican/": 684,
    "http://www.3158.cn/xiangmu/shaokao/": 669,
    "http://www.3158.cn/xiangmu/huoguo/": 1220,
    "http://www.3158.cn/xiangmu/bingqilin/": 123,
    "http://www.3158.cn/xiangmu/xican/": 385,
    "http://www.3158.cn/xiangmu/tianpin/": 873,
    "http://www.3158.cn/xiangmu/mianshi/": 880,
    "http://www.3158.cn/xiangmu/xiuxianyinpin/": 1580,
    "http://www.3158.cn/xiangmu/xiuxianshipin/": 9423,
    "http://www.3158.cn/xiangmu/shushi/": 723,
    "http://www.3158.cn/xiangmu/xiaochiche/": 43,
    "http://www.3158.cn/xiangmu/ganguo/": 58,
    "http://www.3158.cn/xiangmu/xiangguo/": 189,
    "http://www.3158.cn/xiangmu/chaye/": 1472,
    "http://www.3158.cn/xiangmu/tiaoweipin/": 5407,
    "http://www.3158.cn/xiangmu/jinkoushipin/": 372,
    "http://www.3158.cn/xiangmu/shaguo/": 11,
    "http://www.3158.cn/xiangmu/qitameishi/": 2098,
    "http://www.3158.cn/xiangmu/dengshi/": 379,
    "http://www.3158.cn/xiangmu/jiayongdianqi/": 753,
    "http://www.3158.cn/xiangmu/quanjinghua/": 20,
    "http://www.3158.cn/xiangmu/shenghuoguan/": 59,
    "http://www.3158.cn/xiangmu/zhuangshi/": 232,
    "http://www.3158.cn/xiangmu/weiyu/": 529,
    "http://www.3158.cn/xiangmu/chugui/": 670,
    "http://www.3158.cn/xiangmu/pinpaijiaju/": 1872,
    "http://www.3158.cn/xiangmu/chuangshangyongpin/": 126,
    "http://www.3158.cn/xiangmu/jiafangbuyi/": 845,
    "http://www.3158.cn/xiangmu/riyong/": 1644,
    "http://www.3158.cn/xiangmu/canju/": 171,
    "http://www.3158.cn/xiangmu/qitajiaju/": 313,
    "http://www.3158.cn/xiangmu/nvzhuang/": 13027,
    "http://www.3158.cn/xiangmu/tongzhuang/": 2670,
    "http://www.3158.cn/xiangmu/neiyi/": 3563,
    "http://www.3158.cn/xiangmu/nanzhuang/": 3755,
    "http://www.3158.cn/xiangmu/yundong/": 951,
    "http://www.3158.cn/xiangmu/pinpaixie/": 1324,
    "http://www.3158.cn/xiangmu/tongxie/": 273,
    "http://www.3158.cn/xiangmu/xiangbao/": 774,
    "http://www.3158.cn/xiangmu/yunfuzhuang/": 245,
    "http://www.3158.cn/xiangmu/peishi/": 485,
    "http://www.3158.cn/xiangmu/niuzai/": 383,
    "http://www.3158.cn/xiangmu/jiajufushi/": 460,
    "http://www.3158.cn/xiangmu/qitafuzhuang/": 832,
    "http://www.3158.cn/xiangmu/jixieshebei/": 41102,
    "http://www.3158.cn/xiangmu/taiyangneng/": 137,
    "http://www.3158.cn/xiangmu/shipinjixie/": 3334,
    "http://www.3158.cn/xiangmu/jienengshebei/": 6408,
    "http://www.3158.cn/xiangmu/diancixiufu/": 22,
    "http://www.3158.cn/xiangmu/shuijinghua/": 1358,
    "http://www.3158.cn/xiangmu/kongqijinghua/": 852,
    "http://www.3158.cn/xiangmu/huanbaocailiao/": 4524,
    "http://www.3158.cn/xiangmu/huanbaobaozhuang/": 3789,
    "http://www.3158.cn/xiangmu/yuanshuichuli/": 437,
    "http://www.3158.cn/xiangmu/huanweiyongpin/": 441,
    "http://www.3158.cn/xiangmu/qitajixie/": 1061,
    "http://www.3158.cn/xiangmu/huazhuangpin/": 8866,
    "http://www.3158.cn/xiangmu/shibaojian/": 52,
    "http://www.3158.cn/xiangmu/meiti/": 188,
    "http://www.3158.cn/xiangmu/yanjingdian/": 33,
    "http://www.3158.cn/xiangmu/yangshengbaojianpin/": 2912,
    "http://www.3158.cn/xiangmu/meijia/": 232,
    "http://www.3158.cn/xiangmu/zuyu/": 41,
    "http://www.3158.cn/xiangmu/jianshenqicai/": 34,
    "http://www.3158.cn/xiangmu/yangshengguan/": 192,
    "http://www.3158.cn/xiangmu/chanhouhuifu/": 33,
    "http://www.3158.cn/xiangmu/hanzhengfang/": 27,
    "http://www.3158.cn/xiangmu/meirongmeifa/": 520,
    "http://www.3158.cn/xiangmu/zhongcaoyao/": 262,
    "http://www.3158.cn/xiangmu/yiliaoshebei/": 2473,
    "http://www.3158.cn/xiangmu/yiliaofuwu/": 39,
    "http://www.3158.cn/xiangmu/qita156/": 172,
    "http://www.3158.cn/xiangmu/chuangyilipin/": 201,
    "http://www.3158.cn/xiangmu/gexingshipin/": 289,
    "http://www.3158.cn/xiangmu/feicuiyushi/": 53,
    "http://www.3158.cn/xiangmu/xiaoshipindian/": 31,
    "http://www.3158.cn/xiangmu/yinshi/": 64,
    "http://www.3158.cn/xiangmu/gongyipin/": 590,
    "http://www.3158.cn/xiangmu/zhuanshizhubao/": 6,
    "http://www.3158.cn/xiangmu/xiaoshipin/": 452,
    "http://www.3158.cn/xiangmu/jieqinglipin/": 178,
    "http://www.3158.cn/xiangmu/zhonbiao/": 96,
    "http://www.3158.cn/xiangmu/shuijinghupo/": 42,
    "http://www.3158.cn/xiangmu/qitashipin/": 162,
    "http://www.3158.cn/xiangmu/xueshengyongpin/": 387,
    "http://www.3158.cn/xiangmu/yunyingjiaoyu/": 45,
    "http://www.3158.cn/xiangmu/shaoerjiaoyu/": 207,
    "http://www.3158.cn/xiangmu/wangluochuangye/": 12,
    "http://www.3158.cn/xiangmu/yuanchengjiaoyu/": 36,
    "http://www.3158.cn/xiangmu/waiyupeixun/": 28,
    "http://www.3158.cn/xiangmu/shumachanpin/": 3824,
    "http://www.3158.cn/xiangmu/xuexifudao/": 32,
    "http://www.3158.cn/xiangmu/renzhengkaoshi/": 14,
    "http://www.3158.cn/xiangmu/qita18/": 119,
    "http://www.3158.cn/xiangmu/ertongleyuan/": 66,
    "http://www.3158.cn/xiangmu/yingeryouyongguan/": 23,
    "http://www.3158.cn/xiangmu/ertongwanju/": 2368,
    "http://www.3158.cn/xiangmu/yingtongjiaju/": 136,
    "http://www.3158.cn/xiangmu/yingeryongpin/": 1064,
    "http://www.3158.cn/xiangmu/mamayongpin/": 80,
    "http://www.3158.cn/xiangmu/naifen/": 784,
    "http://www.3158.cn/xiangmu/yingyangpin/": 747,
    "http://www.3158.cn/xiangmu/yingerzhijin/": 99,
    "http://www.3158.cn/xiangmu/qita114/": 169,
    "http://www.3158.cn/xiangmu/ganxi/": 74,
    "http://www.3158.cn/xiangmu/yingxiang/": 132,
    "http://www.3158.cn/xiangmu/hunqing/": 41,
    "http://www.3158.cn/xiangmu/yuleji/": 285,
    "http://www.3158.cn/xiangmu/chaoshi/": 51,
    "http://www.3158.cn/xiangmu/jiazheng/": 39,
    "http://www.3158.cn/xiangmu/jiudian/": 147,
    "http://www.3158.cn/xiangmu/yulechangsuo/": 103,
    "http://www.3158.cn/xiangmu/dichan/": 11,
    "http://www.3158.cn/xiangmu/wuliu/": 97,
    "http://www.3158.cn/xiangmu/tongxun/": 56,
    "http://www.3158.cn/xiangmu/lingshou/": 2041,
    "http://www.3158.cn/xiangmu/qita112/": 1368,
    "http://www.3158.cn/xiangmu/xiche/": 42,
    "http://www.3158.cn/xiangmu/qicheyongpin/": 1681,
    "http://www.3158.cn/xiangmu/qichemeirong/": 126,
    "http://www.3158.cn/xiangmu/cheshi/": 53,
    "http://www.3158.cn/xiangmu/qixiu/": 190,
    "http://www.3158.cn/xiangmu/daohang/": 51,
    "http://www.3158.cn/xiangmu/diandongche/": 66,
    "http://www.3158.cn/xiangmu/pinghengche/": 50,
    "http://www.3158.cn/xiangmu/qita120/": 346,
    "http://www.3158.cn/xiangmu/qiangyi/": 906,
    "http://www.3158.cn/xiangmu/zhuangshizhuangxiu/": 1040,
    "http://www.3158.cn/xiangmu/cainuan/": 114,
    "http://www.3158.cn/xiangmu/menchuang/": 1438,
    "http://www.3158.cn/xiangmu/diban/": 689,
    "http://www.3158.cn/xiangmu/jianzhutiemo/": 58,
    "http://www.3158.cn/xiangmu/youqi/": 765,
    "http://www.3158.cn/xiangmu/shuijingjiancai/": 709,
    "http://www.3158.cn/xiangmu/wujinpeijian/": 2743,
    "http://www.3158.cn/xiangmu/louti/": 121,
    "http://www.3158.cn/xiangmu/cizhuan/": 127,
    "http://www.3158.cn/xiangmu/diaodin/": 270,
    "http://www.3158.cn/xiangmu/qitajiancai/": 1542,
    "http://www.3158.cn/xiangmu/baijiu/": 7965,
    "http://www.3158.cn/xiangmu/putaojiu/": 3134,
    "http://www.3158.cn/xiangmu/yangjiu/": 551,
    "http://www.3158.cn/xiangmu/pijiu/": 612,
    "http://www.3158.cn/xiangmu/huangjiu/": 169,
    "http://www.3158.cn/xiangmu/baojianjiu/": 679,
    "http://www.3158.cn/xiangmu/yinliao/": 1996,
    "http://www.3158.cn/xiangmu/chunjingshui/": 236,
    "http://www.3158.cn/xiangmu/qita110/": 238
}

def main():
    for (key, value) in TheDict.items() :
        pageNums = value//20;
        for i in range(0, pageNums):
            queryUrl = key + "?page=" + str(i+1)
            checkPage(queryUrl)

# if __name__ == '__main__':
# main()

