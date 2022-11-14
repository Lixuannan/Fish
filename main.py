import os.path
import platform
import sys
import time
import logging

import requests
import selenium.webdriver
from PIL import Image
from mainwindow import Ui_MainWindow
from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect,
                            Qt)
from PySide6.QtGui import (QCursor,
                           QFont)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QSizePolicy, QTextBrowser,
                               QVBoxLayout, QWidget, QMainWindow, QFileDialog)
from bs4 import BeautifulSoup


class SnapshotReq:
    def __init__(self, url: str, filename: str):
        self.url = url
        self.filename = filename


class Main(Ui_MainWindow):
    def __init__(self):
        self.path = ""
        self.start = time.time()
        self.end = 0.0
        self.data = {
            "uname": "",
            "password": "",
        }
        self.records = []
        self.contents = []
        self.ac_problems = []
        self.snapshot_reqs = []
        self.all_files = []
        self.headers = {
            "Connection": "keep-alive",
            "Host": "oiclass.com",
            "Referer": "http://oiclass.com/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }
        # login oiclass.com in requests session
        self.login_session = requests.sessions.Session()
        # login oiclass.com in PhantomJS
        self.login_driver = selenium.webdriver.PhantomJS(executable_path="/Users/meizhenchen/phantomjs/bin/phantomjs")

    def setupEverything(self, MainWindow):
        self.setupUi(MainWindow)
        self.pushButton.clicked.connect(self.main)
        self.pushButton_2.clicked.connect(self.get_file_path)

    def main(self):
        self.data["uname"] = self.lineEdit.text()
        self.data["password"] = self.lineEdit_2.text()
        self.login_session.post("http://oiclass.com/login", headers=self.headers, data=self.data)
        self.login_driver.get("http://oiclass.com/login/")
        self.login_driver.find_element(by="name", value="uname") \
            .send_keys(self.data["uname"])
        self.login_driver.find_element(by="name", value="password") \
            .send_keys(self.data["password"])
        self.login_driver.find_element(by="xpath",
                                       value=r'//*[@id="panel"]/div[4]/div/div/div/form/div[5]/div/div')
        self.info("Getting all problems")
        self.get_problems()

        self.info(f"All problems:\n\t\t{self.ac_problems}\nTotal: {len(self.ac_problems)}")
        self.info("Getting records")

        for i in self.ac_problems:
            self.get_record(pName=i)

        self.info(f"All records: {self.records}\nTotal: {len(self.records)}")
        self.info("Getting codes from each record")

        for i in self.records:
            self.get_code("http://oiclass.com" + i)

        self.info("Generate snapshots")
        for i in self.snapshot_reqs:
            self.login_driver.get(i.url)
            self.capture_full_screen(filename=i.filename)
        self.info("Generating MarkDown file")
        for i in os.walk(self.path):
            self.all_files.append(i[2])
        self.all_files = self.all_files[0]
        self.generate_md()
        git_log = ""
        self.info("Push to https://github.com/lixuannan/oiclass-answers.git")
        for i in os.popen("zsh push.sh"):
            git_log += i
        self.info(f"Git logs:\n{git_log}")
        self.info("Applying to https://codingcow.eu.org")
        # apply_to_blog()
        self.end = time.time()
        self.critical(f"Done in {end - start}s")

    def get_file_path(self):
        self.path = QFileDialog.getExistingDirectory()

        self.label_3.setText(self.path)

    def generate_md(self):
        head = "# All the answer I write from [oiclass](http://oiclass.com)\n# " \
               "[Oiclass](http://oiclass.com)上的所有我写的题解\n"
        file = open(f"{self.path}README.md", "wt")
        # file.write(f"---\ntitle: 题解\ndate: 2022-11-12 12:13:02\ntag: [\"Oiclass.com\"]\n"
        #            f"---\n")
        file.write(head)
        for j in self.all_files:
            if ".cpp" in j:
                with open(f"{self.path}{j}", "rt") as fi:
                    self.info(f"Reading file {j}")
                    # file.write(f"## {str(j).split('.')[0]}:\n![](https://github.com/Lixuannan/oiclass-answers/"
                    #            f"raw/main/{str(j).split('.')[0]}.png)\n```cpp\n\n{fi.read()}\n```\n")
                    file.write(f"## {str(j).split('.')[0]}:\n![]({self.path}{j})\n```cpp\n\n{fi.read()}\n```\n")

        file.close()
        self.info("Done with generate MarkDown")

    def capture_full_screen(self, filename: str):
        driver = self.login_driver
        driver.maximize_window()
        with open(filename, "wb") as file:
            file.write(driver.get_screenshot_as_png())
        image = Image.open(filename)
        region = image.crop((80, 37, image.width - 380, image.height - 240))
        region.save(filename)
        self.info(f"Snapshot: {filename} was generated")

    def get_record(self, pName: str):
        driver = self.login_driver
        session = self.login_session
        self.info(f"Getting records for {pName} now !")
        problem_page = session.get(url=f"http://oiclass.com/p/{pName}/").text
        self.snapshot_reqs.append(SnapshotReq(f"http://oiclass.com/p/{pName}/",
                                              f"{self.path}{pName}.png"))
        soup = BeautifulSoup(features="lxml", markup=problem_page)
        idx = soup.find_all(name="span", class_="bp4-tag bp4-large bp4-minimal problem__tag-item")
        for j in idx:
            if "ID" in j.text:
                idx = j.text.split(" ")[1]
                break
        self.info(f"Index: {idx}")
        record = ""
        try:
            record = session.get(url=f"http://oiclass.com/record?uidOrName=8241&pid={idx}&status=1").text
        except requests.exceptions.ConnectionError:
            self.error(
                "Connect error when connect to " + f"http://oiclass.com/record?uidOrName=8241&pid={idx}&status=1")
        soup = BeautifulSoup(markup=record, features="lxml")
        a = soup.find_all(name="a", class_="record-status--text pass")
        if a:
            self.records.append(a[0]["href"])
            self.info(f"Record url: http://oiclass.com{a[0]['href']}")
        else:
            self.warning("No records fond, Trying retry by old way")
            retry_by_old_way(driver, session, idx)

    def get_code(self, record):
        session = self.login_session
        self.info(f"Getting codes from record: {record}")
        b = []
        code = ""
        record_page = session.get(url=record, headers=headers).text
        if not ("Oops" in record_page):
            code = BeautifulSoup(record_page, "lxml").find("code").contents[0].text
        else:
            self.error("Can't access the record page " + record)
        if BeautifulSoup(record_page, "lxml"):
            b = BeautifulSoup(record_page, "lxml").find_all("b")
        for j in b:
            if "P" in j.text:
                b = j.text
                break
        if code:
            with open(self.path + b + ".cpp", "wt") as file:
                file.write(f"// Created in {time.asctime(time.localtime(time.time()))}\n"
                           f"// System: {platform.platform()}\n// Python Version: {platform.python_version()}\n{code}")
        return code

    def retry_by_old_way(self, pName):
        session = self.login_session
        driver = self.login_driver
        record = BeautifulSoup(markup=session.get("http://oiclass.com/p/" + str(pName)).text,
                               features="lxml").find_all(name="a", class_="")
        for j in record:
            if "/record/" in j["href"]:
                record = j["href"]
                break
        if type(record) != str:
            self.error(f"Problem {pName} was not be submit before, please check: http://oiclass.com/p/{pName}/")
            return 0
        self.info(f"Try to submit problem {pName} in normal way")
        code = get_code(session, "http://oiclass.com" + record)
        try:
            driver.get("http://oiclass.com/p/" + pName + "/submit/")
            js = r'var x = document.getElementsByClassNam' \
                 r'e("' + r'textbox monospace' + r'"); x.code.value = `' + code + '`'
            driver.execute_script(script=js)
            driver.find_element(by="xpath",
                                value=r'//*[@id="panel"]/div[3]/div/div[1]/div/div[2]/form/div[5]/div/input[2]').click()
        except:
            ...

    def get_problems(self):
        session = self.login_session
        page = session.get(url="http://oiclass.com/user/8241").text
        soup = BeautifulSoup(markup=page, features="lxml")
        problems = soup.find_all(name="a")
        for j in problems:
            if "/p/" in j["href"]:
                self.ac_problems.append(j.text)

    def info(self, msg):
        logging.info(msg)
        self.textBrowser.setText("[info]" + msg)

    def warning(self, msg):
        logging.warning(msg)
        self.textBrowser.setText("[warning]" + msg)

    def critical(self, msg):
        logging.critical(msg)
        self.textBrowser.setText("[critical]" + msg)


if __name__ == '__main__':
    app = QApplication([])
    window = QMainWindow()
    main = Main()
    main.setupUi(window)
    main.setupEverything(window)
    window.show()
    sys.exit(app.exec())
