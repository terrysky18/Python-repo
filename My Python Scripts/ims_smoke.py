#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:       IMS Smoke
# Purpose:
#
# Author:      Alex Yatsenko
# Author:      Serge Shichanin - slpit port and login
#
# Created:     21/11/2013
#-------------------------------------------------------------------------------

import os, sys

path = os.path.normpath(os.path.dirname(os.path.abspath(__file__))+r"\..\..\src")
sys.path = [path]+[p for p in sys.path if not p==path]
import common

from inv_helper import *

import random
import httplib
from datetime import datetime
import string
import urllib,urllib2
import re
import rotwurst
from xml.dom.minidom import parseString
import base64
import hashlib
import datetime
from time import sleep
import utilities as david
from inv_logger import log,debug,log_title,error,info

import inv_host
import inv_download
import inv_auto


AUTOMATION_SUPPORT=dict(browser=['EIE','IMS'], severity=10)

class IMSSmoke(common.InvinceaTestCase):

    def setUp(self):
        "set up before each test in this TestCase"
        log_title(self)
        common.set_trace()
        self.initTimes()
        import dbwrapper
        dbwrapper.init_conn(self.imsdbstring)
        #dbstring='host="10.9.8.96",user="root",db="invincea2"'
        #dbwrapper.init_conn(dbstring)
        pass

    def tearDown(self):
        "clean up after each test in this TestCase"
        log.info("--------------\n             tearDown: %s - %s\n------------" % (
            self.testModuleName,
            self._testMethodDoc))
        self.logIfNotLogged()

    def host(self):
        return self.imshost
        #return "10.9.8.96"

    def port(self):
        return self.imsport
        #return "80"

    def apiport(self):
        return self.imsapiport
        #return "80"

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

        fqdn_list=[fqdn_lower]
        return random.choice(fqdn_list)

    def utf_char(self):

        while 1:
            c = random.choice(xrange(0, 65536, 1))
            if not self.is_invalid_char_ref(c):
                return c

    def is_invalid_char_ref(self, c):
        int_c = c
        if (int_c >= 0 and int_c<9) or (int_c>10 and int_c<13) or (int_c>13 and int_c<31) or (int_c==127) or (int_c>=128 and int_c<159) or (int_c>=55296 and int_c<=57343) or (int_c==65534 or int_c==65535):
            return True
        return False


    def utf8_data(self):
        user=random.choice(["Яценко", "幸福的無知", "Administratör", "βλακασ", 104*'𨳍', ''])
        #user=104*'𨳍' + 'a'
        data1=self.ascii_data()
        data2=self.ascii_data()
        data3=self.ascii_data()

        fqdn=self.utf_fqdn()
        #fqdn=self.ascii_data()
        fqdn_e = fqdn.decode('utf-8').encode('ascii', 'xmlcharrefreplace')

        hd=self.rot_e(data1) + "." + self.rot_e(data2) + "." + self.rot_e(data3) + "." + self.rot_e(fqdn_e)

        log.info("FQDN: %s" %fqdn)
        log.info("FQDN_e: %s" %fqdn_e)
        log.info("FQDN_a: %s" % `[ord(c) for c in fqdn.decode('utf-8')]`)
        return hd, user

    def rot_e(self, data):
        return rotwurst.rotwurst_encode(data)


    def do_hb(self, xml, api_path='/api/heartbeat'):
        host=self.host()
        port=self.apiport()
        conn=httplib.HTTPConnection(host, port)
        conn.request("POST", api_path, xml, self.headers())
        response = conn.getresponse()
        data = response.read()
        #print(str(response.status) + response.reason + data)
        log.info(str(response.status) + response.reason)
        log.info("XML: %s; data: %s" %(xml, data))
        conn.close()
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
            time_now=datetime.datetime.utcnow().isoformat()
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
        #print "Response: %s" % response.status
        #print "Data: %s" % response_data

        self.assertEqual(str(response.status), '200')

        if 'audit' not in hb_path:
            dom = parseString(response_data)
            status_code = dom.getElementsByTagName('status')[0].getAttribute('code')
            self.assertEqual(status_code, '0')


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


    def portstatus(self):
        url = "http://chameleon3:8000/qa/ims/status"
        status = urllib2.urlopen(url).read()
        info(status,url)
        return status

    def lastport(self):
        url = "http://chameleon3:8000/qa/ims/lastport"
        port = urllib2.urlopen(url).read()
        info('last port = ',port,url)
        return port


    def setapiport(self,port):
        info("set api port to ",port)
        self.imsapiport=int(port)
        args=urllib.urlencode(dict(apiport=port,key='WinstonWolf'))
        url = "http://chameleon3:8000/qa/ims/setport?%s" % args
        setport_status = urllib2.urlopen(url).read()
        if not 'OK'== setport_status:
            raise Exception,"cannot communicate to %s" % url
        sleep(5)
        count = 60
        while count:
            count -= 1
            sleep(1)
            if 'acknowledged'==self.portstatus():
                sleep(30)
                return
        raise Exception,"cannot get api port acknowledgement"

    def bothports(self,check,port1,port2):
        lp = self.lastport()
        if not int(lp)==port1:
            self.setapiport(port1)
        check()
        self.setapiport(port2)
        check()

    def test_001_regular(self):
        """001 regular;;   ...

        Regular hearbeat request to the server

        Step 1. Form a host descriptor and check for its existance
        Expected: Host descriptor doesn't exist
        Step 2. Hearbeat in that host and check
        Expected: Host now exists in the database

        """
        def check():
            hd, user=self.utf8_data()
            #Server strips out fqdn from HD
            new_hd = ".".join(hd.split('.')[:-1])
            result=david.host_desc_exists(new_hd)
            self.assertFalse(result, "The host desc, %s, was found before running heartbeat" %new_hd)
            hb_path='/api/heartbeat'
            file_set=self.file_set()
            files=random.choice(file_set)
            ip=self.gen_ip()
            xml=self.form_heartbeat("heartbeat", "Enterprise:3.1.0-new", ip, hd, user,"Default", files)
            self.verify(xml, hb_path)
            result=david.host_desc_exists(new_hd)
            self.assertTrue(result, "The host desc, %s, was not found after running heartbeat" %new_hd)
            #Redo that with a new IP
            ip=self.gen_ip()
            xml=self.form_heartbeat("heartbeat", "Enterprise:3.1.0-new", ip, hd, user,"Default", files)
            self.verify(xml, hb_path)
            result=david.host_desc_exists(new_hd)
            self.assertTrue(result, "The host desc, %s, was not found after running heartbeat" %new_hd)
            db_ip=david.get_host_attribute("ip", new_hd).strip("'")
            self.assertEqual(str(ip), str(db_ip), "The IP address %s that was generated did not match the IP %s in the database" %(ip, db_ip))
        self.bothports(check,80,8081)

    def test_002_install(self):
        """002 install;;   ...

        Install hearbeats to the server

        Step 1. Form a host descriptor and check for its existance
        Expected: Host descriptor doesn't exist
        Step 2. Hearbeat in that host with all install statuses and check
        Expected: Host now exists in the database with correct install status

        """
        def check():
            hd, user=self.utf8_data()
            new_hd = ".".join(hd.split('.')[:-1])
            hb_path='/api/install_status'
            result=david.host_desc_exists(new_hd)
            self.assertFalse(result, "The host desc, %s, was found before running heartbeat" %new_hd)
            actions={"install_start":"installing", "install_end":"just_installed", "upgrade_start":"upgrading", "upgrade_end":"installed", "uninstall_start":"uninstalling", "uninstall_end":"uninstalled"}
            ip=self.gen_ip()
            for action in actions.iterkeys():
                xml=self.form_install("install_status", "Enterprise:3.1.0-install", ip, hd, user, "Default", action, "result text", "0")
                sleep(1)
                self.verify(xml, hb_path)
                attr=david.get_host_attribute("install_status", new_hd).strip('\'')
                log.info(action)
                log.info(attr)
                self.assertEqual(attr, actions[action])

        self.bothports(check,8081,80)


    def test_003_fetch(self):
        """003 fetch;;   ...

        Fetch hearbeat request to the server

        Step 1. Form a host descriptor and check for its existance
        Expected: Host descriptor doesn't exist
        Step 2. Hearbeat in that host as installed and check
        Expected: Host now exists in the database
        Step 3. Perform a fetch hearbeat request
        Expected: The correct response comes back

        """
        def check():

            hd, user=self.utf8_data()
            new_hd = ".".join(hd.split('.')[:-1])
            result=david.host_desc_exists(new_hd)
            self.assertFalse(result, "The host desc, %s, was found before running heartbeat" %new_hd)
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

            result=david.host_desc_exists(new_hd)
            self.assertTrue(result, "The host desc, %s, was not found after running heartbeat" %new_hd)

            #now an actual fetch
            hb_path='/api/fetch_config'
            xml=self.form_heartbeat("fetch_config", "Enterprise:3.1.0-fetch", ip, hd, user,"Default", files)
            self.verify(xml, hb_path)

        self.bothports(check,80,8081)

    def test_004_audit(self):
        """004 audit;;   ...

        Host audit hearbeat request to the server

        Step 1. Form a host descriptor and check for its existance
        Expected: Host descriptor doesn't exist
        Step 2. Hearbeat in that host and check
        Expected: Host now exists in the database
        Step 3. Perform a new host audit request
        Expected: New audit now appears in the database
        """
        def check():
            hd, user=self.utf8_data()
            new_hd = ".".join(hd.split('.')[:-1])
            result=david.host_desc_exists(new_hd)
            self.assertFalse(result, "The host desc, %s, was found before running heartbeat" %new_hd)

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
            result=david.host_desc_exists(new_hd)
            self.assertTrue(result, "The host desc, %s, was not found after running heartbeat" %new_hd)

            audits=david.get_all_audit(new_hd)
            self.assertEqual(audits, None, "Audits exist for the newly created host %s" %new_hd)

            #and only then the audit
            hb_path='/api/audit'
            events=self.form_events()
            xml=self.form_audit(hd, user, ip, events)
            self.verify(xml, hb_path)

            audits=david.get_all_audit(new_hd)

            for audit in audits:
                if audit[6] not in events:
                    self.fail("The URL %s not found in the audit events for the host %s." %(audits[6], ip))
        self.bothports(check,8081,80)


    def test_005_download(self):
        """005 download;;   ...

        an attempt is made to navigate to an unsecure split download page

        Step 1. Navigate the script
        Expected: the page is not saying Not allowed

        """
        url = "http://10.9.13.32:%s/invincea/invinceaenterprise_kit_3.3.0-16942.exe"
        def downl(port):
            timer=30
            info('trying to download EXE from ',url % port)
            while timer>0:
                sleep(1)
                try:
                    f=urllib2.urlopen(url % port, timeout=5)
                    fb=f.read(2)
                    #fb = urllib2.urlopen(url % port,timeout=5).read()[:2]
                    break
                except Exception,e:
                    info(e)
                    fb = 'oops'
                info ('first two:',fb)
                timer=timer-1
            return fb


        def checks(port):
            firstbytes = downl(80)
            split = 'split' if port==8081 else 'non-split'
            self.failIf('MZ' != firstbytes, "80 is not open for downloads for %s ports" % split)
            firstbytes = downl(8081)
            if split == 'split':
                self.failIf('MZ' != firstbytes, "8081 is closed for downloads for split ports")
            else:
                self.failIf('MZ' == firstbytes, "8081 is open for downloads for  non-split ports")


        lp = self.lastport()
        info("current port = %s" % lp)
        if not int(lp)==8081:
            self.setapiport(8081)

        checks(8081)
        Sleep(10)
        self.setapiport(80)

        checks(80)

    def test_006_web_login(self):
        """006 web login;;   ...

        an attempt is made to navigate, login and check if the home page is up

        Step 1. Navigate the browser to the page
        Expected: the page is open
        Step 2. enter uername and password, hit Enter
        Expected: logged in home page

        """
        def check():
            MC = inv_auto.MouseClick
            MM = inv_auto.MouseMove

            img = lambda x: inv_download.img(self,x)
            self.ff_location = self.programFilesLocation() + r"\Mozilla Firefox\firefox.exe"
            self.smokeurl="http://" + self.imshost + ":" + self.imsport

            inv_host.runAsync(self,self.ff_location,self.smokeurl)
            Opt("WinTitleMatchMode",2)
            st = WinWaitCheck("Login","",60)
            Sleep(3000)
            WinMove("Login","",1,1,800,600)
            Sleep(1000)
            inv_auto.Opt("WinTitleMatchMode",2)
            x1,y1,x2,y2 = inv_auto.WinGetRect("Login")

            midx = (x1 + x2) / 2
            midy = (y1 + y2) / 2
            status,x1,y1,f = self.findImage(midx - 150,midy -150 ,512,512,img("IMSLogin"),level=0.8,show=True)
            debug(status,x1,y1,f)
            MM(x1,y1)
            Sleep(1000)
            MC(x1,y1)
            Send("admin")
            status,x1,y1,f = self.findImage(midx - 150,midy -150 ,512,512,img("IMSPassword"),level=0.8, show=True)
            debug(status,x1,y1,f)
            MM(x1,y1)
            Sleep(1000)
            MC(x1,y1)
            Send("asdf")
            Sleep(1000)
            Send("{ENTER}")
            Sleep(1000)
            Send("{ESC}")
            Sleep(1000)
            status,x1,y1,f = self.findImage(1,1,512,512,img("IMSLoggedIn"),level=0.8, show=True)
            self.failUnless(status, "Cannot login to IMS website")
            WinClose("Invincea")
        self.bothports(check,80,8081)

    def test_007_api_group_change(self):
        """007 api group change;;   ...

        Change the group for a host through the api.

        Step 1. Do an install_status heartbeat
        Expected: Server says ok, group is created, and host is in group
        """
        def check():

            #do the install status
            hd, user=self.utf8_data()
            new_hd = ".".join(hd.split('.')[:-1])
            result=david.host_desc_exists(new_hd)
            self.assertFalse(result, "The host desc, %s, was found before running heartbeat" %new_hd)

            new_group = 'RandomGroupName'+str(random.randint(10000,99999))

            hb_path='/api/install_status'
            actions=["install_start", "install_end"]
            ip=self.gen_ip()
            for action in actions:
                xml=self.form_install("install_status", "Enterprise:3.1.0-group", ip, hd, user, new_group, action, "result text", "0")
                sleep(1)
                self.verify(xml, hb_path)

            #check for the group on the server

            result=david.host_desc_exists(new_hd)
            self.assertTrue(result, "The host desc, %s, was not found after running heartbeat" %new_hd)
            result=david.get_host_attribute("group_name", new_hd).strip("'")
            self.assertEqual(new_group, result, "The newly created group %s was not found" %new_group)

        self.bothports(check,8081,80)

if __name__ == '__main__':
    common.runTestsFromModule(IMSSmoke,AUTOMATION_SUPPORT)
