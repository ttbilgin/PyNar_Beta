import os
import sys
import requests
import subprocess
import urllib
import importlib.util

from PyQt5.QtWidgets import QMessageBox

from Components.MessageBox.CustomizeMessageBox import CustomizeMessageBox_Ok

parentdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
# sys.path.append(parentdir) # nuitka'da sorun çıkarıyor.
from configuration import Configuration

class detectos:
    def writeIni(self):
        self.c = Configuration()
        self.systemName = self.osEnvironment()
        try:
            self.checkAppJar()
            if self.c.getSystem() != self.systemName:
                try:
                    self.c.updateConfig('System', 'system', self.systemName)
                except:
                    self.standartWrite()
        except:
            self.standartWrite()

    def osEnvironment(self):
        if sys.platform in ["win32", "cygwin"]:
            return "windows"
        elif sys.platform == "darwin":
            return "mac"
        else:
            desktopEnv = os.environ.get("XDG_MENU_PREFIX")
            if desktopEnv is not None:
                desktopEnv = desktopEnv.lower()
                if desktopEnv in ["xterm-", "gnome-", "mate-", "kde-"]:
                    return desktopEnv.replace("-","")
                elif desktopEnv == "xfce-":
                    return "pardus"

    def standartWrite(self):
        config = self.c.setStandard()
        config['System']['system'] = self.systemName

        base = self.c.checkPath(parentdir)

        iniPath = base + "/Config/pynar.ini"
        with open(iniPath, 'w', encoding='utf-8') as f:
            config.write(f)

    def checkAppJar(self):
        try:
            self.warn = False
            self.result_install = None
            self.package_name = 'appJar'
            spec = importlib.util.find_spec(self.package_name)
            if spec is None:
                res = self.connectedToInternet()
                if res:
                    self.setAppjarVersion()
                    self.result_install = self.appjarInstall()

                else:
                    path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
                    os.system('pip install ' + path + '/Data/packages/appJar-0.94.0.tar.gz')
        except Exception as err:
            if self.warn == False:
                CustomizeMessageBox_Ok("Bir Hata ile karşılaşıldı", QMessageBox.Critical)

    def appjarInstall(self):
        text = 'appJar'
        version = "==" + self.version
        process = subprocess.Popen(
            [os.path.basename(sys.executable), '-m', 'pip', 'install', text + version,
             "--disable-pip-version-check"],
            stdout=subprocess.PIPE, shell=self.c.getShell())
        while True:
            # output = process.stdout.readline()
            rc = process.poll()
            if rc == 1:  # Hata
                return False
            elif rc == 0:  # Başarılı
                return True
            elif rc is not None:
                # TODO:Loglama eklenince burayada log eklenmeli
                return False

    def setAppjarVersion(self):
        baseUrl = 'https://pypi.org/pypi/'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'}
        jsonDataUrl = baseUrl + urllib.parse.quote(self.package_name) + "/json"
        req = requests.get(jsonDataUrl, headers=headers)
        jsonData = req.json()
        self.version = jsonData['info']['version']

    def connectedToInternet(self):
        try:
            if requests.get('https://google.com').ok:
                return True
        except Exception as err:
            return False
