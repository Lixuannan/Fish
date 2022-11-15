import faulthandler
import logging
import threading
import os.path
import platform
import time
import sys

import git.exc
import requests
import selenium.webdriver
from PIL import Image
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from bs4 import BeautifulSoup
from git import *

from mainwindow import Ui_MainWindow


PYTHONFAULTHANDLER = 1
faulthandler.enable()


class SnapshotReq:
    def __init__(self, url: str, filename: str):
        self.url = url
        self.filename = filename


class Main(Ui_MainWindow):
    def __init__(self):
        print(os.getcwd())
        self.git_obj = None
        self.remote_obj = None
        self.repo = None
        self.path = ""
        self.start = 0.0
        self.end = 0.0
        self.uid = 8241
        self.git_url = ""
        self.git_username = ""
        self.git_password = ""
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
        if not os.path.isdir(f"{os.getcwd()}/.HydroTool"):
            os.mkdir(f"{os.getcwd()}/.HydroTool")
        # login oiclass.com in requests session
        self.login_session = requests.sessions.Session()
        self.chrome_option = selenium.webdriver.ChromeOptions()
        self.chrome_option.add_argument("--headless")
        self.chrome_option.add_argument("--disable-gpu")
        self.chrome_option.page_load_strategy = "eager"
        self.chrome_option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.login_driver = selenium.webdriver\
            .Chrome(options=self.chrome_option)

    def setupEverything(self, MainWindow):
        self.setupUi(MainWindow)
        self.browse_path.clicked.connect(self.get_file_path)
        self.start_button.clicked.connect(lambda: threading.Thread(target=self.main).start())
        self.push_to_remote.stateChanged.connect(self.set_state)

    def set_state(self):
        if self.push_to_remote.isChecked():
            self.remote_url.setEnabled(True)
            self.git_uname.setEnabled(True)
            self.token.setEnabled(True)
        else:
            self.remote_url.setEnabled(False)
            self.git_uname.setEnabled(False)
            self.token.setEnabled(False)

    def main(self):
        self.start = time.time()
        if self.uname.text() == "" or self.save_path.text() == "" \
                or self.password.text() == "" or self.uid_edit.text() == "":
            self.error("需要参数")
            return 1
        if self.push_to_remote.isChecked() and (self.remote_url.text() == "" or
           self.git_uname.text() == "" or self.token.text() == ""):
            self.error("需要参数")
            return 1
        self.data["uname"] = self.uname.text()
        self.data["password"] = self.password.text()
        self.login_session.post("http://oiclass.com/login", headers=self.headers, data=self.data)
        self.login_driver.get("http://oiclass.com/login/")
        self.login_driver.find_element(by="xpath",
                                       value=r'//*[@id="panel"]/div[4]/div/div/div/form/div[1]/div/label/input') \
            .send_keys(self.data["uname"])
        self.login_driver.find_element(by="xpath",
                                       value=r'//*[@id="panel"]/div[4]/div/div/div/form/div[2]/div/label/input') \
            .send_keys(self.data["password"])
        self.login_driver.find_element(by="xpath",
                                       value=r'//*[@id="panel"]/div[4]/div/div/div/form/div[5]/div/div/input[2]')\
            .click()
        self.info("正在获得所有AC的题目")
        self.get_problems()

        self.info(f"所有AC的题目：\n{self.ac_problems}\n共: {len(self.ac_problems)}项")
        self.info("正在获得所有测评记录")

        for i in self.ac_problems:
            self.get_record(pName=i)

        self.info(f"所有测评记录： {self.records}\nTotal: {len(self.records)}")
        self.info("正在从所有测评记录中提取AC代码")

        for i in self.records:
            self.get_code("http://oiclass.com" + i)

        if not self.do_not_save_snapshots.isChecked():
            self.info("正在获得题目的截图")
            threading.Thread(target=self.capture_full_screen).start()
        self.info("正在生成README.md文件")
        for i in os.walk(self.path):
            self.all_files.append(i[2])
        if self.all_files:
            self.all_files = self.all_files[0]
        else:
            self.error(f"{self.path} 中没有任何文件，失败")
            self.critical(f"在 {self.end - self.start}秒中失败")
        self.generate_md()
        if self.push_to_remote.isChecked():
            self.info(f"正在将所有文件推送到仓库： {self.remote_url.text()}中")
            self.push2remote()
        self.end = time.time()
        self.critical(f"在 {self.end - self.start}秒中失败")

    def check_git(self) -> bool:
        command_log = ""
        for i in os.popen("git"):
            command_log += i
        if "command not found" in command_log:
            return False
        return True

    def push2remote(self):
        if not self.check_git():
            self.info("系统并未安装git，正在尝试安装")
            for i in os.popen("brew install git"):
                self.info(i)
        try:
            self.repo = Repo(path=self.path)
        except git.exc.InvalidGitRepositoryError:
            self.repo = Repo.init(path=self.path)

        if not self.repo.remote():
            self.repo.create_remote(name="origin", url=self.remote_url.text())
        self.git_obj = self.repo.git
        self.remote_obj = self.repo.remotes[0]
        self.git_obj.add(".")
        self.git_obj.commit("-m", "update by HydroTool")
        self.remote_obj.push("main")

    def get_file_path(self):
        self.path = QFileDialog.getExistingDirectory()
        for i in range(len(self.path)):
            if i % 10 == 0:
                self.path
        self.save_path.setText(self.path)

    def generate_md(self):
        md_header = "# All the answer I write from [oiclass](http://oiclass.com)\n# " \
               "[Oiclass](http://oiclass.com)上的所有我写的题解\n"
        file = open(f"{self.path}/README.md", "wt")
        # file.write(f"---\ntitle: 题解\ndate: 2022-11-12 12:13:02\ntag: [\"Oiclass.com\"]\n"
        #            f"---\n")
        file.write(md_header)
        for j in self.all_files:
            if ".cpp" in j:
                with open(f"{self.path}/{j}", "rt") as fi:
                    self.info(f"Reading file {j}")
                    # file.write(f"## {str(j).split('.')[0]}:\n![](https://github.com/Lixuannan/oiclass-answers/"
                    #            f"raw/main/{str(j).split('.')[0]}.png)\n```cpp\n\n{fi.read()}\n```\n")
                    file.write(f"## {str(j).split('.')[0]}:\n![]({self.path}/{j})\n```cpp\n\n{fi.read()}\n```\n")

        file.close()
        self.info("完成 README.md 文件生成")

    def capture_full_screen(self):
        driver = self.login_driver
        for i in self.snapshot_reqs:
            driver.get(i.url)
            width = driver.execute_script("return document.documentElement.scrollWidth")
            height = driver.execute_script("return document.documentElement.scrollHeight")
            driver.set_window_size(width, height)
            with open(i.filename, "wb") as file:
                file.write(driver.get_screenshot_as_png())
            image = Image.open(i.filename)
            region = image.crop((80, 37, image.width - 380, image.height - 240))
            region.save(i.filename)
            self.info(f"题目截图: {i.filename} 完成")

    def get_record(self, pName: str):
        session = self.login_session
        self.info(f"为 {pName} 获取测评记录")
        problem_page = session.get(url=f"http://oiclass.com/p/{pName}/").text
        self.snapshot_reqs.append(SnapshotReq(f"http://oiclass.com/p/{pName}/",
                                              f"{self.path}/{pName}.png"))
        soup = BeautifulSoup(features="lxml", markup=problem_page)
        idx = soup.find_all(name="span", class_="bp4-tag bp4-large bp4-minimal problem__tag-item")
        for j in idx:
            if "ID" in j.text:
                idx = j.text.split(" ")[1]
                break
        self.info(f"题目PID: {idx}")
        record = ""
        try:
            record = session.get(url=f"http://oiclass.com/record?uidOrName=8241&pid={idx}&status=1").text
        except requests.exceptions.ConnectionError:
            self.error(
                "无法连接到 " + f"http://oiclass.com/record?uidOrName=8241&pid={idx}&status=1")
        soup = BeautifulSoup(markup=record, features="lxml")
        a = soup.find_all(name="a", class_="record-status--text pass")
        if a:
            self.records.append(a[0]["href"])
            self.info(f"测评记录: http://oiclass.com{a[0]['href']}")
        else:
            self.warning("无法以本模式获得测评记录, 尝试另一种模式")
            self.retry_by_old_way(idx)

    def get_code(self, record):
        session = self.login_session
        self.info(f"正在为测评记录 {record} 生成代码")
        b = []
        code = ""
        record_page = session.get(url=record, headers=self.headers).text
        if not ("Oops" in record_page):
            code = BeautifulSoup(record_page, "lxml").find("code").contents[0].text
        else:
            self.error("无法访问页面：" + record)
        if BeautifulSoup(record_page, "lxml"):
            b = BeautifulSoup(record_page, "lxml").find_all("b")
        for j in b:
            if "P" in j.text:
                b = j.text
                break
        if code:
            with open(self.path + "/" + b + ".cpp", "wt") as file:
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
            self.error(f"问题 {pName} 从来都没有被提交过，详情: http://oiclass.com/p/{pName}/")
            return 0
        self.info(f"尝试以提交题目： {pName} ")
        code = self.get_code("http://oiclass.com" + record)
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
        page = session.get(url=f"http://oiclass.com/user/{self.uid}").text
        soup = BeautifulSoup(markup=page, features="lxml")
        problems = soup.find_all(name="a")
        all_files = []
        for j in os.walk(self.path):
            all_files.append(j[2])
        if all_files:
            all_files = all_files[0]
        if self.skip_problems.isChecked():
            for j in problems:
                if "/p/" in j["href"]:
                    p = False
                    for k in all_files:
                        if k == j["href"].split("/")[2] + ".cpp" or k == j["href"].split("/")[2] + ".png":
                            p = True
                            break
                    if not p:
                        self.ac_problems.append(j.text)
        else:
            for j in problems:
                if "/p/" in j["href"]:
                    self.ac_problems.append(j.text)

    def info(self, msg):
        logging.info(msg)
        self.log.append("[信息] " + msg)

    def warning(self, msg):
        logging.warning(msg)
        self.log.append("[警告] " + msg)

    def error(self, msg):
        logging.error(msg)
        self.log.append("[错误] " + msg)

    def critical(self, msg):
        logging.critical(msg)
        self.log.append("[最重要信息] " + msg)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app = QApplication([])
    window = QMainWindow()
    main = Main()
    main.setupEverything(window)
    window.show()
    sys.exit(app.exec())
