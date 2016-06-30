#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      alex.yatsenko
#
# Created:     21/11/2013
# Copyright:   (c) alex.yatsenko 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import sys
import random
import httplib
import logging
from datetime import datetime
import string
import urllib
import urllib2
import re
import unittest
import rotwurst
from xml.dom.minidom import parseString
import base64
import hashlib
import datetime
from time import sleep


class TestHeartbeat(unittest.TestCase):

    logger = logging.getLogger()
    hdlr = logging.FileHandler(r'c:\tmp\hb.log')
    formatter = logging.Formatter('%(asctime)s -- %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)


    def setUp(self):
        pass
    def host(self):
	return "10.9.8.96"

    def port(self):
        return "80"

    def gen_ip(self):
        ip=str(random.randint(1,255)) + '.' + str(random.randint(1,255)) + '.' + str(random.randint(1,255)) + '.' + str(random.randint(1,255))
        return ip

    def headers(self):
        return {"Content-Type" : "text/xml; charset=UTF-8"}

    def ascii_data(self):
        charset = "ABCDEFGHIJKLMNOPQRSTUVWYXZabcdefghijklmnopqrstuvwxyz0123456789 !\"#$%&'()*+,-./:;<=>?@_"
        data=(''.join(random.choice(charset) for x in range(12)))
        return data

    def byte_range(self, first, last):
        return list(range(first, last+1))

    def utf_fqdn(self):

        fqdn_lower=''.join(unichr((self.utf_char())) for x in range(random.randint(1,70))).encode('utf-8')
        fqdn_chinese=u""

        for x in range(random.randint(1,70)):
            fqdn_chinese+=self.chinese_char()

        fqdn_list=[fqdn_chinese.encode('utf-8'), fqdn_lower]
        return random.choice(fqdn_list)

    def utf_char(self):

        while 1:
            c = random.choice(xrange(0, 65536, 1))
            """

            first_values = self.byte_range(0x00, 0x7F) + self.byte_range(0xC2, 0xF4)
            trailing_values = self.byte_range(0x80, 0xBF)
            first = random.choice(first_values)

            if first <= 0x7F:
                c = random.choice([first])
            elif first <= 0xDF:
                c = random.choice(([first, random.choice(trailing_values)]))
            elif first == 0xE0:
                c = random.choice(([first, random.choice(self.byte_range(0xA0, 0xBF)), random.choice(trailing_values)]))
            elif first == 0xED:
                c = random.choice(([first, random.choice(self.byte_range(0x80, 0x9F)), random.choice(trailing_values)]))
            elif first <= 0xEF:
                c = random.choice(([first, random.choice(trailing_values), random.choice(trailing_values)]))
            elif first == 0xF0:
                c = random.choice(([first, random.choice(self.byte_range(0x90, 0xBF)), random.choice(trailing_values), random.choice(trailing_values)]))
            elif first <= 0xF3:
                c = random.choice(([first, random.choice(trailing_values), random.choice(trailing_values), random.choice(trailing_values)]))
            elif first == 0xF4:
                c = random.choice(([first, random.choice(self.byte_range(0x80, 0x8F)), random.choice(trailing_values), random.choice(trailing_values)]))
            """
            if not self.is_invalid_char_ref(c):
                return c

    def is_invalid_char_ref(self, c):
        int_c = c
        if (int_c >= 0 and int_c<9) or (int_c>10 and int_c<13) or (int_c>13 and int_c<31) or (int_c==127) or (int_c>=128 and int_c<159) or (int_c>=55296 and int_c<=57343) or (int_c==65534 or int_c==65535):
            return True
        return False

    def chinese_char(self):

        ch = u"阿啊哎愛安八把爸吧白百班搬半拌辦幫棒保抱報杯北貝被備本鼻比筆必閉幣邊便表別病伯不步部猜才菜參餐廁差茶查長常場唱超吵車襯稱城程吃出初除廚楚穿床春詞次聰從醋存寸錯大打帶單擔但當刀導到道的得登燈等地弟第典點店電調定訂冬東懂動都豆肚對頓多E餓而兒耳二發罰法煩飯方房風放非飛啡費封服腐父付附傅復該趕剛鋼港高糕告戈哥歌各個給跟更工弓公功共狗夠瓜颳掛拐關館慣廣貴國果過孩還海寒韓漢航好號喝合和河黑很紅後候護花華滑話劃壞歡換黃回會活火或貨幾磯機及急級極己季計記寄際濟加家傢架價假間簡件見檢減健將教腳較餃叫覺接節姐介借斤今金緊近進京經睛精景靜九久酒就舊局俱劇咖卡開看康考可渴刻客課空哭苦褲快塊口啦辣來藍籃老樂了累淚冷離李里理裡禮力連臉練涼兩倆亮林另聊留流六樓路錄律旅綠倫洛嗎媽麻馬碼買賣滿慢忙毛麼沒門們悶每美米面民敏名明末母姆木目拿哪那奶男南難腦呢內能你年唸您牛紐女暖拍盤旁胖跑朋皮啤片篇便票漂平瓶婆七期其起汽氣戚千簽前錢且親琴慶清請秋球去然讓熱人認日容肉如賽三掃色沙山杉衫傷上燒少紹社舍誰身什生盛剩師十拾食時實識始示市式事是室視飾試適收手首受售瘦書舒輸暑屬樹帥雙水睡順說司糸思死四送束素速宿訴酸算雖隨歲孫所它他她台太彈探湯糖躺套特疼踢提題體天田甜條調跳貼鐵聽廳停同頭途圖土腿托外灣完玩晚碗王往網忘望危囗為位味喂文問我臥五午舞物務夕西希習洗喜係下夏先鮮險現線香鄉箱想象像小校笑些鞋寫謝心辛新信星行醒姓興須許續學雪押呀壓淹言顏眼演驗養癢樣要藥爺也夜葉業一衣醫宜姨已以椅易意因音銀印英迎營贏影應泳用郵游遊友有又右魚雨語預寓元員園圓遠願月約越樂運再在糟早澡怎站張長漲找照折者著這真針鎮整正政證支汁芝知直職只指紙中鐘種重州轉週助住祝專隹準桌子字自嘴最走租足昨左作坐座做"
        return random.choice(ch)


    def utf8_data(self):
        #user=random.choice(["Яценко", "幸福的無知", "Administratör", "βλακασ", 104*'𨳍', ''])
        user=104*'𨳍' + 'a'
        #user=104*'𨳍'
        data=self.ascii_data()
        fqdn=self.utf_fqdn()
        #fqdn_array=[34, 77, 62, 195, 144, 41, 68, 46, 79, 195, 162, 195, 149, 43, 111, 31, 40, 101, 195, 155, 54, 194, 180, 195, 148, 50, 102, 64, 59, 10, 40]
        #fqdn = ''.join(unichr(x) for x in fqdn_array).encode('utf-8')
        fqdn_e = fqdn.decode('utf-8').encode('ascii', 'xmlcharrefreplace')

        hd=self.rot_e(data) + "." + self.rot_e(data) + "." + self.rot_e(data) + "." + self.rot_e(fqdn_e)

        logging.info("FQDN: %s" %fqdn)
        logging.info("FQDN_e: %s" %fqdn_e)
        logging.info("FQDN_a: %s" % `[ord(c) for c in fqdn.decode('utf-8')]`)
        #logging.info("FQDN_a: %s" % fqdn_array)
        return hd, user

    def rot_e(self, data):
        return rotwurst.rotwurst_encode(data)


    def do_hb(self, xml, api_path='/api/heartbeat'):
        host=self.host()
        port=self.port()
        conn=httplib.HTTPConnection(host, port)
        conn.request("POST", api_path, xml, self.headers())
        response = conn.getresponse()
        data = response.read()
        #print(str(response.status) + response.reason + data)
        print(str(response.status) + response.reason)
        logging.info("XML: %s; data: %s" %(xml, data))
        conn.close()
        return response, data

    def do_url_hb(self, xml, api_path='/api/heartbeat'):
        url=r"https://10.9.8.92:80/api/heartbeat/"
        request=urllib2.Request(url, xml, self.headers())
        response="Empty"
        data="Empty"
        try:
            response=urllib2.urlopen(request)
            data=response.read
            print html
        except urllib2.URLError, e:
            print e.reason
        return response, data

    def form_install(self, hb_type, product, ip, hd, user, group, action, result_text, code):
        userline=''
        if user!='':
            userline = " user=\"%s\"" % user
        xml=(
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" +
        " <%s fmt=\"xml\"" % hb_type +
        " product=\"%s\"" % product +
        " ip=\"%s\"" % ip +
        " hd=\"%s\"" % hd +
        userline +
        " group_name=\"%s\"" % group +
        " action=\"%s\"" % action +
        " result_text=\"%s\"" % result_text +
        " code=\"%s\">" % code +
        " </%s>" % hb_type
        )
        #print "XML: %s" % xml
        return xml

    def form_heartbeat(self, hb_type, product, ip, hd, user, group, files={}):
        opt=''
        if hb_type!='fetch_config':
            opt=" active=\"%s\">" % "true"
        else:
            opt=" >"

        userline=''
        if user!='':
            userline = " user=\"%s\"" % user

        if not files:
            xml=(
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" +
            " <%s fmt=\"xml\"" % hb_type +
            " product=\"%s\"" % product +
            " ip=\"%s\"" % ip +
            " hd=\"%s\"" % hd +
            userline +
            " group_name=\"%s\"" % group +
            opt +
            " </%s>" % hb_type
            )
        else:
            file_string=''
            for file_name, md5 in files.iteritems():
                file_string+=" <file name=\"%s\"" % file_name + " md5=\"%s\">" % md5 + " </file>"
            xml=(
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" +
            " <%s fmt=\"xml\"" % hb_type +
            " product=\"%s\"" % product +
            " ip=\"%s\"" % ip +
            " hd=\"%s\"" % hd +
            userline +
            " group_name=\"%s\"" % group +
            opt +
            file_string +
            " </%s>" % hb_type
            )
        #print "XML: %s" % xml
        return xml

    def form_audit(self, hd, user, ip, events):
        userline=''
        if user!='':
            userline = " user=\"%s\"" % user

        xml=(
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" +
        " <audit fmt=\"xml\" hd=\"%s\"" % hd +
        userline +
        " ip=\"%s\"> " % ip +
        events +
        " </audit>"
        )
        #print "XML: %s" % xml
        return xml

    def form_events(self):
        event_string=''

        event_length=random.randrange(1, 10)
        for event in range(event_length):
            event_type=random.choice(['trusted_site', 'trusted_site_remove'])
            time_now=datetime.datetime.now().isoformat()
            url=random.choice(['http://www.david.com/foo/l', 'https://mentis.com/bar', 'http://экслер.рф', 'https://幸福的無知幸福的無知'])
            #url=self.utf_fqdn()
            opt=''
            if event_type=='trusted_site':
                permanent=random.choice(['true', 'false'])
                reason=random.choice(['Да почему-то фиг его знает', 'Do not know why I did this', '幸福的無知幸福'])
                opt=(
                ' permanent=\"%s\"' % permanent +
                ' reason=\"%s\"' % reason
                )
            event_string+=(
            ' <event type=\"%s\"' % event_type +
            ' time=\"%s\"' % time_now +
            ' url=\"%s\"' % url +
            opt + ' />'
            )
        return event_string


    def verify(self, xml, hb_path):

        response, response_data=self.do_hb(xml, hb_path)
        print "Response: %s" % response
        print "Data: %s" % response_data

        self.assertEqual(str(response.status), '200')

        if 'audit' not in hb_path:
            dom = parseString(response_data)
            status_code = dom.getElementsByTagName('status')[0].getAttribute('code')
            self.assertEqual(status_code, '0')

    
    def test_install(self):
         "Install/upgrade/uninstall heartbeats"
         print "============ test_install ================"

         hd, user=self.utf8_data()
         hb_path='/api/install_status'

         actions=["install_start", "install_end", "upgrade_start", "upgrade_end", "uninstall_start", "uninstall_end"]
         ip=self.gen_ip()
         for action in actions:
             xml=self.form_install("install_status", "Enterprise:3.1.0-install", ip, hd, user, "Default", action, "result text", "0")
             sleep(1)
             self.verify(xml, hb_path)

   
    def test_regular(self):
        "Regular heartbeat"
        print "============= test_regular ==============="

        hd, user=self.utf8_data()
        hb_path='/api/heartbeat'
        file_set=self.file_set()
        files=random.choice(file_set)
        ip=self.gen_ip()
        xml=self.form_heartbeat("heartbeat", "Enterprise:3.1.0-regular", ip, hd, user,"Default", files)
        self.verify(xml, hb_path)





    def test_fetch(self):
        "Fetch config"
        print "=============== test_fetch ==============="

        hd, user=self.utf8_data()

        #host has to exist first, so install first
        hb_path='/api/install_status'
        actions=["install_start", "install_end"]
        ip=self.gen_ip()
        for action in actions:
            xml=self.form_install("install_status", "Enterprise:3.1.0-fetch", ip, hd, user, "Default", action, "result text", "0")
            sleep(1)
            self.verify(xml, hb_path)

        #then we do a hearbeat
        hb_path='/api/heartbeat'
        file_set=self.file_set()
        files=random.choice(file_set)
        xml=self.form_heartbeat("heartbeat", "Enterprise:3.1.0-fetch", ip, hd, user,"Default", files)
        self.verify(xml, hb_path)

        #now an actual fetch
        hb_path='/api/fetch_config'
        xml=self.form_heartbeat("fetch_config", "Enterprise:3.1.0-fetch", ip, hd, user,"Default", files)
        self.verify(xml, hb_path)

  

    def file_set(self):
        m=hashlib.md5()
        m.update('12345')
        m = m.hexdigest()
        file_set=(
            {},
            {"preferences.xml": m},
            {"preferences.xml": m, "custom_apps.xml": m},
            {"preferences.xml": m, "custom_apps.xml": m, "trustedsites.txt": m}
        )
        return file_set

    def test_audit(self):
        "Escape hatch auditing"
        print "===============test_audit==============="

        hd, user=self.utf8_data()

        #host has to exist first, so install first
        hb_path='/api/install_status'
        actions=["install_start", "install_end"]
        ip=self.gen_ip()
        for action in actions:
            xml=self.form_install("install_status", "Enterprise:3.1.0-audit", ip, hd, user, "Default", action, "result text", "0")
            sleep(1)
            self.verify(xml, hb_path)

        #then we do a hearbeat
        hb_path='/api/heartbeat'
        file_set=self.file_set()
        files=random.choice(file_set)
        xml=self.form_heartbeat("heartbeat", "Enterprise:3.1.0-audit", ip, hd, user,"Default", files)
        self.verify(xml, hb_path)

        #and only then the audit
        hb_path='/api/audit'
        events=self.form_events()
        xml=self.form_audit(hd, user, ip, events)
        self.verify(xml, hb_path)


if __name__ == '__main__':
    unittest.main()
