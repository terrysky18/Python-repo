#-------------------------------------------------------------------------------
# Name:         eAppLoop
# Purpose:      Office inline save loops
#
# Author:      Steven Kool
# Created:     07/16/2013
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import common
import os
import win32api
import shutil
from inv_logger import log, log_title, debug, error
from inv_helper import *
import win32con
import Win32Registry
import re
import time
import inv_host
from inv_host import WinWaitVisible, closeAllIEs, navigateHostIE, answerIE
from inv_attach import takeScreenShot
from Win32Registry import findInstalledProductKey
from math import sqrt

AUTOMATION_SUPPORT=dict(browser=['EIE'], severity=10)


class eAppLoop(common.InvinceaTestCase):

    def setUp(self):
       log_title(self)
       if not self.manualOrRetired(self._testMethodDoc):
            self.runMainInstaller(Enterprise=True)
            if self.installEnterprise(redirect=False):
                self.launchEnterprise()
            #self.exitEnterprise()

            self.timeout = 60

       self.initTimes()
       self.initVars()
       closeAllIEs(self)


    def initVars(self):
        self.build  = self.getINIValue("newMainInstaller").split('.exe')[0].split('-')[1]
        self.invLogfile=self.localdir + "inv.log"
        self.guestLogfile=self.localdir+"shared\\guest.log"
        self.hookLogfile=self.localdir+"shared\\inv_hook.log"

    def tearDown(self):
        self.logIfNotLogged()
        self.exitEnterprise()

    def bringUpPreferencesDialog(self):

        self.clickPreferences()
        WinWait(self.preferences, '', 10)
        WinActivateCheck(self.preferences)

    def goOpenAppTab(self):
        self.launchEnterprise()
#        Run(self.pathToInvBrowser(Enterprise=True))
#        Sleep(5000)
        self.bringUpPreferencesDialog()
        self.intro("select|tray|preferences")

        Sleep(500)
        try:
            result=self.intro("select|preferences|appsButton")
        except:
            raise Exception("ConnSonar failed to select Apps button, exception has occured")

    def gracefullyExitPreferences(self):
        if "preferences" in self.intro("list_active_dialogs"):
            self.intro("select|preferences|okButton")

    def parseApps(self):

        appsList=[]
        self.exitEnterprise()
        logfile=open(self.invLogfile, 'r')
        logfile.seek(0,2)
        self.launchEnterprise()
        loglines=logfile.readlines()
        logfile.close()

        for line in loglines:
            if "App found:" in line:
                appName=line.split('found:')
                appsList.append(appName[1].strip())

        if 'IE' in appsList:
            appsList.append('Internet Explorer')
        if 'Chrome' in appsList:
            appsList.append('Google Chrome')
        if 'Office' in appsList:
            appsList.append('Microsoft Word')
            appsList.append('Microsoft Excel')
            appsList.append('Microsoft PowerPoint')

        return appsList

    def deVersion(self,appName):
        appName=re.sub("[0-9]", "", appName)
        appName=appName.replace(".","")
        return appName.strip()




    def checkAndSetApp(self, appName="Mysterious",docType="Invalid", protectFlag=1, browser=False):

        self.goOpenAppTab()
        appsList = self.intro("get_value|preferences|appFrame.appList").split("|")
        if not appName in appsList:
            debug("%s not found in the list of apps" % appName)
            return False

        #turn off untrusted setting if on
        self.intro("select|preferences|securityButton")
        setting=self.intro("get_value|preferences|securityFrame.openUntrustedCheckBox")
        if setting=='1':
            self.intro(("select|preferences|securityFrame.openUntrustedCheckBox"))

        #check the checkbox to protect
        self.intro("select|preferences|appsButton")
        self.intro("set_value|preferences|appFrame.appList|%s" % appName)
        fileLabel=self.intro("get_value|preferences|appFrame.fileLabel")
        if docType in fileLabel:
            if browser:
                self.intro("set_value|preferences|appFrame.defaultUrlCheckBox|1")
            self.intro("set_value|preferences|appFrame.defaultDocCheckBox|%s" % protectFlag)
        else:
            raise Exception("%s does not seem to be a protected file type or %s cannot be selected in the Apps" % (docType, appName))
        self.gracefullyExitPreferences()
        self.exitEnterprise()
#        self.intro("select|tray|exit")
        return True

    def openAppOnSandbox(self, filename="Something", appClass="Mystery", fileType="Unknown"):
        Sleep(1000)
        if os.path.isfile(self.miscdir + filename):
            command="start" + " " + self.miscdir + filename
            debug("%s is executing" % command)
            os.system(command)
            self.myauto.Opt("WinTitleMatchMode", 2) # match anywhere
            if WinWaitActive(filename,"",450):
                if not WinExists("[regexpclass:Sandbox.+%s]" % appClass):
                    self.fail("The app did not open the %s on the guest" % fileType )
            else:
                raise Exception("Could not launch the %s in 450 seconds with the command %s" % (fileType, command))
        else:
            raise Exception("Test asset %s is missing from %s" % (filename, self.miscdir))

    def openAppNatively(self, filename="Something", appClass="Mystery", fileType="Unknown"):

        if os.path.isfile(self.miscdir + filename):
            command="start" + " " + self.miscdir + filename
            debug("%s is executing" % command)
            os.system(command)
            self.myauto.Opt("WinTitleMatchMode", 2) # match anywhere
            if WinWaitVisibleCheck(filename,"",120):
                if WinExists("[regexpclass:Sandbox.+%s]" % appClass):
                    self.fail("The %s opened on the guest, expected it on the host" % fileType)
                else:
                    self.answerDefault()
                    answerIE(self)
                    WinActivateCheck(filename)
                    self.myauto.Send("!{F4}")
                    Sleep(1000)
            else:
                raise Exception("Could not launch the %s in 120 seconds with the command %s" % (command, fileType))
        else:
            raise Exception("Test asset %s is missing from %s" % (filename, self.miscdir))

    def preconditionCheckAndRun(self, handlerExists, runLine, reason=""):
        if handlerExists:
            runLine()
        else:
            self.Incomplete(reason)

    def openNewFile(self, app, version='Mystery'):
        #values for app are EXCEL, POWERPNT, WINWORD
        exeName={'Excel':'Excel', 'PowerPoint':'Powerpnt', 'Word':'Winword'}
        switches={'Excel':' /e', 'PowerPoint':' /b', 'Word':' /w'}
        windowName = app

        path = 'C:\\Program Files (x86)\\Microsoft Office\\Office%s\\%s.exe' % (version, exeName[app])
        if not os.path.exists(path):
            path = 'C:\\Program Files\\Microsoft Office\\Office%s\\%s.exe' % (version, exeName[app])
        Run(path+switches[app])

        WinWaitActive(windowName)
        Sleep(10000)
        if version > 14:
            if WinWaitActive("Microsoft %s" % app, "", 5):
                Send("y")
        hotkeys=''
        if app == 'Excel':
            hotkeys += '!fnl'
            if version != 15:
                hotkeys += '{enter}'
        #elif version > 14:
        #    Sleep(250)
        #    hotkeys += '!l'
        Send(hotkeys)#hotkeys to open a blank document

    def saveAndExit(self, filename, app, version):
        windowName = app
        WinActivate(windowName)
        WinWaitActive(windowName)
        self.myauto.Send("!fa")
        if version > 14:
            self.myauto.Send('cb')
        WinWaitActive("Save As")
        self.myauto.Send(self.miscdir + filename)
        Sleep(250)
        self.myauto.Send("!s")
        if WinWaitActive("Confirm", "", 5):
            self.myauto.Send("!y")
        Opt("WinTitleMatchMode",3)
        if WinWaitActive("Microsoft Word", "", 5):#exact match to detect a dialog window
            self.myauto.Send("!r{ENTER}")
        if WinWaitActive("Microsoft PowerPoint", "", 5):#exact match to detect a dialog window
            self.myauto.Send("y")
        if WinWaitActive("Microsoft Excel", "", 5):#exact match to detect a dialog window
            self.myauto.Send("y")
        if WinWaitActive("Confirm Save As", "", 5):#exact match to detect a dialog window
            self.myauto.Send("y")
        Opt("WinTitleMatchMode",2)
        WinActivate(windowName)
        WinWaitActive(windowName)
        self.myauto.Send("!{F4}")

    def checkEditInXLSX(self, target, filename):
        #print("debug")
        shutil.copy("%s%s" % (self.miscdir, filename), "%s%s.zip" % (self.miscdir, filename))
        Run("cmd /C %s7z.exe x -so %s%s.zip xl\\worksheets\\sheet1.xml 2>nul |findstr -i \"%s\" > %sresults.xml" % (self.miscdir, self.miscdir, filename, target, self.miscdir))#unzip files
        Sleep(1000)
        resultsSize = os.path.getsize(self.miscdir+"results.xml")
        return resultsSize > 0

    def checkEditInDOCX(self, target, filename):
        #print("debug")
        shutil.copy("%s%s" % (self.miscdir, filename), "%s%s.zip" % (self.miscdir, filename))
        Run("cmd /C %s7z.exe x -so %s%s.zip word\\document.xml 2>nul |findstr -i \"%s\" > %sresults.xml" % (self.miscdir, self.miscdir, filename, target, self.miscdir))#unzip files
        Sleep(1000)
        resultsSize = os.path.getsize(self.miscdir+"results.xml")
        return resultsSize > 0

    def checkEditInPPTX(self, target, filename):
        #print("debug")
        shutil.copy("%s%s" % (self.miscdir, filename), "%s%s.zip" % (self.miscdir, filename))
        Run("cmd /C %s7z.exe x -so %s%s.zip ppt\\slides\\slide1.xml 2>nul |findstr -i \"%s\" > %sresults.xml" % (self.miscdir, self.miscdir, filename, target, self.miscdir))#unzip files
        Sleep(1000)
        resultsSize = os.path.getsize(self.miscdir+"results.xml")
        return resultsSize > 0

    def checkEditInASD(self, target, path):
        #print("debug")
        cmd = "cmd /C findstr -i \"%s\" \"%s\" > %sresults.xml" % (target, path, self.miscdir)
        Run(cmd)#unzip files
        Sleep(1000)
        resultsSize = os.path.getsize(self.miscdir+"results.xml")
        return resultsSize

    def fileCorrupted(self, filename):
        reader = open(filename, "r")
        corrupted =  "HIJACKED" in reader.readline(256)
        reader.close()
        #print(filename)
        #print(corrupted)
        return corrupted

    def getAppInfo(self, app):
        arr = Win32Registry.ListRegKeys(win32con.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Office\\")
        lastVer = 0.0
        for x in arr:
            try:
                if float(x) > lastVer:
                    lastVer = float(x)
            except:
                pass
        return int(lastVer)


    def storeLogs(self, msg, index):
        self.myauto.clipput("")
        self.myauto.send("^{PRINTSCREEN}")
        screenshot = ""
        for _ in xrange(10):
            screenshot = self.myauto.clipget()
            if screenshot != "":
                break
            self.myauto.sleep(1000)
        Sleep(1500)
        shutil.copyfile(self.invLogfile,r"c:\invinceaqa\inv.log")
        shutil.copyfile(self.guestLogfile,r"c:\invinceaqa\guest.log")
        shutil.copyfile(self.hookLogfile,r"c:\invinceaqa\inv_hook.log")
        os.system("tail -100 \\invinceaqa\\automation.log > \\invinceaqa\\qa.log")
        cmd = "%s7z.exe a -tzip \\logs\\%slogs%s_%s_%s.zip \"%s\" \"%s\" \"%s\" \"%s\" \"%s\"" % (self.miscdir,
            time.time(), self.build, msg, index,
            r"\invinceaqa\inv.log",
            r"\invinceaqa\guest.log",
            r"\invinceaqa\inv_hook.log",
            r"\invinceaqa\qa.log",
            screenshot)
        Run(cmd)
        Sleep(1500)
        self.deleteFile(screenshot)

    def clearForExit(self, app):
        Sleep(5000)
        debug("clearing")
        WinActivate("Save As")
        if WinWaitActive("Save As", "", 5):
            debug("closing save-as dialog")
            Send("{ESC}")
        self.myauto.Opt("WinTitleMatchMode", 2)
        Sleep(500)
        WinActivate(app)
        WinWaitActive(app)
        Send("!{F4}")
        self.myauto.Opt("WinTitleMatchMode", 3)
        if WinWaitActive("Microsoft %s" % app, "", 5):
            debug("closing confirm dialog")
            Send("n")
        self.myauto.Opt("WinTitleMatchMode", 2)
        debug("cleared")
        Sleep(1500)

    def genLoops(self):
        if os.path.exists("\\invinceaqa\\kill.txt"):
            os.remove("\\invinceaqa\\kill.txt")
        for incr in range(0,5):
            os.system("start cmd /C \"\\invinceaqa\\src\\loop.py\" %s" % incr)

    def test_001_xlsxLoop(self):
        """test_001_xlsxLoop; ;                               r:r001 s:Major ..."""
        msg = "ExcelInlineSave"
        xlsxfile = "ExcelLoop"
        lastVer = self.getAppInfo('Excel')
        tallyFile = "ExcelInlineFails.txt"

        self.openNewFile('Excel', lastVer)
        edit = '100000000'
        self.myauto.Send('%s' % edit)
        Sleep(250)
        self.saveAndExit(xlsxfile, 'Excel', lastVer)
        Sleep(500)

        appName='Microsoft Excel'
        self.setUserPreferences("doc_protection", "disabled", "")
        self.setUserPreferences("open_untrusted_docs_only", "enabled", "false")

        for test in range(0,1000):
            self.openAppOnSandbox(xlsxfile + '.xlsx', 'XLMAIN', 'xlsx')
            self.genLoops()
            Sleep(3000)
            self.myauto.Opt("SendKeyDelay", 15)

            for edit in range(100000001, 200000001):
                WinActivate('%s.xlsx' % xlsxfile)
                WinWaitActive('%s.xlsx' % xlsxfile)
                self.myauto.Send("{DEL}%s^s" % edit)#Make the next edit
                debug("Sending inline save")
                if WinWaitActive("Save As", "", 2):
                    debug("Save As dialog detected")
                    self.storeLogs(msg, edit)
                    break

                if not self.checkEditInXLSX(edit, '%s.xlsx' % xlsxfile):
                    Sleep(3000)
                    self.myauto.Send("^s")
                    debug("Sending inline save")
                    for doubleCheck in range(0,15):
                        WinActivate("Save As")
                        if WinWaitActive("Save As", "", 2):
                            debug("Save As dialog detected")
                            self.storeLogs(msg, edit)
                            break
                        if self.checkEditInXLSX(edit, '%s.xlsx' % xlsxfile):
                            break
                    if WinWaitActive("Save As", "", 2):
                        break
                    if not self.checkEditInXLSX(edit, '%s.xlsx' % xlsxfile):
                        debug("No edit detected on host")
                        self.storeLogs(msg, edit)
                        break
                debug("edit %s saved on the host" % edit)

            outStream = open("%s%s" %(self.miscdir, tallyFile), "a")
            outStream.write("%s\n" % (edit-100000000))
            outStream.close()
            self.clearForExit("Excel")
            self.exitEnterprise()

            killSig = open("\\invinceaqa\\kill.txt", 'w')
            killSig.close()
            for i in range(0,5):
                if not WinExists("loop.py"):
                    if not WinExists("cmd.exe"):
                        break
                Sleep(2000)
            os.remove("\\invinceaqa\\kill.txt")

    def test_002_xlsxLoopPermissions(self):
        """test_002_xlsxLoopPermissions; ;                               r:r001 s:Major ..."""
        xlsxfile = "ExcelLoop"
        lastVer = self.getAppInfo('Excel')

        appName='Microsoft Excel'
        self.setUserPreferences("doc_protection", "disabled", "")
        self.setUserPreferences("open_untrusted_docs_only", "enabled", "false")

        #Ready to begin looping
        for incr in range(0,5):
            os.system("start cmd /K \"\\invinceaqa\\src\\loop.py\" %s" % incr)
        for test in range(0,1000):
            self.openNewFile('Excel', lastVer)
            edit = '100000000'
            self.myauto.Send('%s' % edit)
            Sleep(250)
            self.saveAndExit(xlsxfile, 'Excel', lastVer)
            Sleep(500)

            self.openAppOnSandbox(xlsxfile + '.xlsx', 'XLMAIN', 'xlsx')
            self.myauto.Opt("SendKeyDelay", 15)
            WinWaitActive('%s.xlsx' % xlsxfile)
            os.system("start cmd /C \"\\invinceaqa\\src\\permissionsLoop.py\" %s.xlsx" % xlsxfile)

            for edit in range(100000001, 200000001):
                WinActivate('%s.xlsx' % xlsxfile)
                WinWaitActive('%s.xlsx' % xlsxfile)
                self.myauto.Send("{DEL}%s^s" % edit)#Make the next edit
                Sleep(5000)
                if self.fileCorrupted("%s%s.xlsx" % (self.miscdir, xlsxfile)):
                    self.storeLogs(msg, edit)
                    break
            self.exitEnterprise()

    def test_003_docxLoop(self):
        """test_003_docxLoop; ;                               r:r001 s:Major ..."""
        msg = "WordInlineSave"
        docxfile = "WordLoop"
        lastVer = self.getAppInfo('Word')
        tallyFile = "WordInlineFails.txt"

        self.openNewFile('Word', lastVer)
        edit = '100000000'
        self.myauto.Send('%s' % edit)
        Sleep(250)
        self.saveAndExit(docxfile, 'Word', lastVer)

        appName='Microsoft Word'
        self.setUserPreferences("doc_protection", "disabled", "")
        self.setUserPreferences("open_untrusted_docs_only", "enabled", "false")

        for test in range(0,1000):
            self.openAppOnSandbox(docxfile + '.docx', 'OpusApp', 'docx')
            self.genLoops()
            Sleep(3000)
            self.myauto.Opt("SendKeyDelay", 15)

            for edit in range(100000001, 200000001):
                WinActivate('%s.docx' % docxfile)
                WinWaitActive('%s.docx' % docxfile)
                self.myauto.Send("{END}+{HOME}{DEL}%s^s" % edit)#Make the next edit
                debug("Sending inline save")
                if WinWaitActive("Save As", "", 2):
                    debug("Save As dialog detected")
                    self.storeLogs(msg, edit)
                    break

                if not self.checkEditInDOCX(edit, '%s.docx' % docxfile):
                    Sleep(3000)
                    self.myauto.Send("^s")
                    debug("Sending inline save")
                    for doubleCheck in range(0,15):
                        WinActivate("Save As")
                        if WinWaitActive("Save As", "", 2):
                            debug("Save As dialog detected")
                            self.storeLogs(msg, edit)
                            break
                        if self.checkEditInDOCX(edit, '%s.docx' % docxfile):
                            break
                    if WinWaitActive("Save As", "", 2):
                        break
                    if not self.checkEditInDOCX(edit, '%s.docx' % docxfile):
                        debug("No edit detected on host")
                        self.storeLogs(msg, edit)
                        break
                debug("edit %s saved on the host" % edit)

            outStream = open("%s%s" %(self.miscdir, tallyFile), "a")
            outStream.write("%s\n" % (edit-100000000))
            outStream.close()
            self.clearForExit("Word")
            self.exitEnterprise()

            killSig = open("\\invinceaqa\\kill.txt", 'w')
            killSig.close()
            for i in range(0,5):
                if not WinExists("loop.py"):
                    if not WinExists("cmd.exe"):
                        break
                Sleep(2000)
            os.remove("\\invinceaqa\\kill.txt")



    def test_004_docxLoopPermissions(self):
        """test_004_docxLoopPermissions; ;                               r:r001 s:Major ..."""
        docxfile = "WordLoop"
        lastVer = self.getAppInfo('Word')
        tallyFile = "WordInlineFails.txt"

        appName='Microsoft Word'
        self.setUserPreferences("doc_protection", "disabled", "")
        self.setUserPreferences("open_untrusted_docs_only", "enabled", "false")
        for incr in range(0,5):
            os.system("start cmd /K \"\\invinceaqa\\src\\loop.py\" %s" % incr)

        for test in range(0,1000):
            self.openNewFile('Word', lastVer)
            edit = '100000000'
            self.myauto.Send('%s' % edit)
            Sleep(250)
            self.saveAndExit(docxfile, 'Word', lastVer)

            self.openAppOnSandbox(docxfile + '.docx', 'OpusApp', 'docx')
            self.myauto.Opt("SendKeyDelay", 15)
            WinWaitActive('%s.docx' % docxfile)
            os.system("start cmd /C \"\\invinceaqa\\src\\permissionsLoop.py\" %s.docx" % docxfile)

            for edit in range(100000001, 200000001):
                WinActivate('%s.docx' % docxfile)
                WinWaitActive('%s.docx' % docxfile)
                self.myauto.Send("{END}+{HOME}{DEL}%s^s" % edit)#Make the next edit
                Sleep(5000)
                if self.fileCorrupted("%s%s.docx" % (self.miscdir, docxfile)):
                    self.storeLogs(msg, edit)
                    break
            self.exitEnterprise()

    def test_005_pptxLoop(self):
        """test_005_pptxLoop; ;                               r:r001 s:Major ..."""
        msg = "PptInlineSave"
        pptxfile = "PptLoop"
        lastVer = self.getAppInfo('PowerPoint')
        tallyFile = "PptInlineFails.txt"

        self.openNewFile('PowerPoint', lastVer)
        edit = '100000000'
        self.myauto.Send('%s' % edit)
        Sleep(250)
        self.saveAndExit(pptxfile, 'PowerPoint', lastVer)

        appName='Microsoft PowerPoint'
        self.setUserPreferences("doc_protection", "disabled", "")
        self.setUserPreferences("open_untrusted_docs_only", "enabled", "false")

        for test in range(0,1000):
            self.openAppOnSandbox(pptxfile + '.pptx', 'PPTFrameClass', 'pptx')
            self.genLoops()
            Sleep(3000)
            self.myauto.Opt("SendKeyDelay", 15)
            WinActivate('%s.pptx' % pptxfile)
            WinWaitActive('%s.pptx' % pptxfile)
            Sleep(1000)
            self.myauto.Send("{TAB}")
            Sleep(1000)

            for edit in range(100000001, 200000001):
                WinActivate('%s.pptx' % pptxfile)
                WinWaitActive('%s.pptx' % pptxfile)
                self.myauto.Send("{END}+{HOME}{DEL}%s^s" % edit)#Make the next edit
                debug("Sending inline save")
                if WinWaitActive("Save As", "", 2):
                    debug("Save As dialog detected")
                    self.storeLogs(msg, edit)
                    break

                if not self.checkEditInPPTX(edit, '%s.pptx' % pptxfile):
                    Sleep(3000)
                    self.myauto.Send("^s")
                    debug("Sending inline save")
                    for doubleCheck in range(0,15):
                        WinActivate("Save As")
                        if WinWaitActive("Save As", "", 2):
                            debug("Save As dialog detected")
                            self.storeLogs(msg, edit)
                            break
                        if self.checkEditInPPTX(edit, '%s.pptx' % pptxfile):
                            break
                    if WinWaitActive("Save As", "", 2):
                        break
                    if not self.checkEditInPPTX(edit, '%s.pptx' % pptxfile):
                        debug("No edit detected on host")
                        self.storeLogs(msg, edit)
                        break
                debug("edit %s saved on the host" % edit)

            outStream = open("%s%s" %(self.miscdir, tallyFile), "a")
            outStream.write("%s\n" % (edit-100000000))
            outStream.close()
            self.clearForExit("PowerPoint")
            self.exitEnterprise()

            killSig = open("\\invinceaqa\\kill.txt", 'w')
            killSig.close()
            for i in range(0,5):
                if not WinExists("loop.py"):
                    if not WinExists("cmd.exe"):
                        break
                Sleep(2000)
            os.remove("\\invinceaqa\\kill.txt")

    def test_006_pptxLoopPermissions(self):
        """test_006_pptxLoopPermissions; ;                               r:r001 s:Major ..."""
        pptxfile = "PptLoop"
        lastVer = self.getAppInfo('PowerPoint')
        tallyFile = "PptInlineFails.txt"

        appName='Microsoft PowerPoint'
        self.setUserPreferences("doc_protection", "disabled", "")
        self.setUserPreferences("open_untrusted_docs_only", "enabled", "false")
        for incr in range(0,5):
            os.system("start cmd /K \"\\invinceaqa\\src\\loop.py\" %s" % incr)

        for test in range(0,1000):
            self.openNewFile('PowerPoint', lastVer)
            edit = '100000000'
            self.myauto.Send('%s' % edit)
            Sleep(250)
            self.saveAndExit(pptxfile, 'PowerPoint', lastVer)

            self.openAppOnSandbox(pptxfile + '.pptx', 'PPTFrameClass', 'pptx')
            self.myauto.Opt("SendKeyDelay", 15)
            WinWaitActive('%s.pptx' % pptxfile)
            self.myauto.Send("{TAB}")#Make the next edit
            os.system("start cmd /C \"\\invinceaqa\\src\\permissionsLoop.py\" %s.pptx" % pptxfile)

            for edit in range(100000001, 200000001):
                WinActivate('%s.pptx' % pptxfile)
                WinWaitActive('%s.pptx' % pptxfile)
                self.myauto.Send("{END}+{HOME}{DEL}%s^s" % edit)#Make the next edit
                Sleep(5000)
                if self.fileCorrupted("%s%s.pptx" % (self.miscdir, pptxfile)):
                    self.storeLogs(msg, edit)
                    break
            self.exitEnterprise()

    def test_007_docxAutoLoop(self):
        """test_007_docxAutoLoop; ;                               r:r001 s:Major ..."""
        acc = common.AssertAccumulator("test_003_DOCXAutoLoop - verify edits are saved")
        docxfile = "WordAutoLoop"
        lastVer = self.getAppInfo('Word')
        pathToASD = '%sShared\\Office\\Word\\AutoRecovery save of %s.asd' % (self.localdir, docxfile)

        self.openNewFile('Word', lastVer)
        self.myauto.Send('!ft')
        Sleep(250)
        self.myauto.Send('{DOWN 3}{TAB}')
        Sleep(250)
        self.myauto.Send('m1')
        Sleep(250)
        self.myauto.Send('{ENTER}')
        Sleep(250)
        self.myauto.Send('!{F4}')
        Sleep(500)

        appName='Microsoft Word'
        self.setUserPreferences("doc_protection", "disabled", "")
        self.setUserPreferences("open_untrusted_docs_only", "enabled", "false")
        self.openAppOnSandbox(docxfile + '.docx', 'OpusApp', 'docx')

        edit = 1
        if os.path.exists(pathToASD):
            lastSaved = os.path.getmtime(pathToASD)
        WinActivate('%s.docx' % docxfile)
        WinWaitActive('%s.docx' % docxfile)
        self.myauto.Send("%s" % edit)#Make the next edit, no need to manually save

        lastSaved = 0
        mtime = 0
        for edit in range(100000001, 100000501):
            if os.path.exists(pathToASD):
                lastSaved = os.path.getmtime(pathToASD)
            WinActivate('%s.docx' % docxfile)
            WinWaitActive('%s.docx' % docxfile)
            self.myauto.Send("{END}+{HOME}{DEL}%s" % edit)#Make the next edit, no need to manually save
            countTime = 0
            for countTime in range(1,14):
                if os.path.exists(pathToASD):
                    mtime = os.path.getmtime(pathToASD)
                    if mtime != lastSaved:
                        break
                Sleep(5000)
            acc.assertFalse(mtime==lastSaved, 'No autosave file generated for edit %s' % edit)
            if mtime != lastSaved:
                result = self.checkEditInASD(edit,pathToASD)
                acc.assertTrue(result, 'Autosave did not save change %s' % (edit-100000000))

        self.myauto.Send('!{F4}')
        if WinWaitActive("Microsoft Word", "", 5):
            self.myauto.Send('n')
        self.exitEnterprise()

        self.openNewFile('Word', lastVer)#reset the autosave interval to the default
        self.myauto.Send('!ft')
        self.myauto.Send('{DOWN 3}{TAB}')
        Sleep(250)
        self.myauto.Send('m10')
        Sleep(250)
        self.myauto.Send('{ENTER}')
        Sleep(250)
        self.myauto.Send('!{F4}')
        acc.finalAssert(self)



if __name__ == '__main__':
    common.runTestsFromModule(eAppLoop, AUTOMATION_SUPPORT)
