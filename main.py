import faulthandler
import logging
import threading
import os.path
import platform
import time
import sys

import requests
import pygit2
import _cffi_backend
import selenium.webdriver
from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from bs4 import BeautifulSoup
from qt_material import apply_stylesheet

from mainwindow import Ui_MainWindow


# 用来 DEBUG 的配置
PYTHONFAULTHANDLER = 1
faulthandler.enable()


# 定义测评记录类
class RecordData:
    def __init__(self, pName: str, url: str):
        self.pName = pName
        self.url = url

# 定义一个用来存储截取需求的类
class SnapshotReq:
    def __init__(self, url: str, filename: str):
        self.url = url
        self.filename = filename


# 主类
class Main(Ui_MainWindow, QObject):
    # 定义信号，分别是更新进度条和添加日志
    update_signal = Signal()
    add_log = Signal()

    def __init__(self, Mainwindow):
        # 将窗口实现
        self.setupUi(Mainwindow)
        # 实现 QObject 类
        super(Main, self).__init__()
        # 定义一大堆变量，基本顾名思义
        self.git_config = None
        self.main_thr = None
        self.git_obj = None
        self.remote_obj = None
        self.repo = None
        self.progress = 0
        self.total_progress = 0
        self.path = ""
        self.start = 0.0
        self.end = 0.0
        self.uid = 8241
        self.log_str = ""
        self.git_url = ""
        self.git_username = ""
        self.git_password = ""
        # 在 request.session 中登录 HydroOJ 使用的 post 表单
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
        self.login_session: requests.Session
        self.chrome_option: selenium.webdriver.ChromeOptions
        self.login_driver: selenium.webdriver.Chrome

    # 将信号连接到槽
    def setupSignal(self):
        self.browse_path.clicked.connect(self.get_file_path)
        self.start_button.clicked.connect(self.create_main)
        self.push_to_remote.stateChanged.connect(self.set_state)
        self.update_signal.connect(lambda: self.progressBar.setValue(self.progress * 100 // self.total_progress))
        self.add_log.connect(lambda: self.log.append(self.log_str))

    # 创建主算法线程
    def create_main(self):
        self.main_thr = threading.Thread(target=self.main).start()

    # 当推送到仓库被选中时解锁部分输入框
    def set_state(self):
        if self.push_to_remote.isChecked():
            self.remote_url.setEnabled(True)
            self.git_uname.setEnabled(True)
            self.token.setEnabled(True)
            self.email_edit.setEnabled(True)
        else:
            self.remote_url.setEnabled(False)
            self.git_uname.setEnabled(False)
            self.token.setEnabled(False)
            self.email_edit.setEnabled(False)

    # 主函数
    def main(self):
        self.start = time.time()
        # 判断参数是否齐全，不齐全就报错返回
        if self.uname.text() == "" or self.save_path.text() == "" \
                or self.password.text() == "" or self.uid_edit.text() == "":
            self.error("需要参数")
            return 1
        if self.push_to_remote.isChecked() and (self.remote_url.text() == "" or
           self.git_uname.text() == "" or self.token.text() == ""):
            self.error("需要参数")
            return 1
        # 更改"开始"按钮的文字和按钮的信号所传递到的槽
        self.start_button.setText("取消")
        self.start_button.clicked.connect(self.cancel)
        # 从 UI 获得用户名、密码等数据
        self.data["uname"] = self.uname.text()
        self.data["password"] = self.password.text()
        # 将 ChromeOptions 及 Chrome 实例化，为正式启动做准备
        self.chrome_option = selenium.webdriver.ChromeOptions()
        self.chrome_option.add_argument("--headless")  # 不显示界面，仅实现浏览器功能
        self.chrome_option.add_argument("--disable-gpu")  # 避免报错（google 官方说的）
        self.chrome_option.page_load_strategy = "eager"  # 将加载模式设置为"能用就好"而不是要等到加载完所有资源后才进行操作，节省时间
        self.chrome_option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 不告诉网站"我是模拟器"
        self.login_driver = selenium.webdriver\
            .Chrome(options=self.chrome_option)
        self.login_session = requests.sessions.Session()
        # 简单登陆一下 session 和 driver
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
        if not self.do_not_save_snapshots.isChecked():
            self.total_progress = len(self.ac_problems) * 3
        else:
            self.total_progress = len(self.ac_problems) * 2
        self.progress += 1
        self.info("正在获得所有测评记录")

        for i in self.ac_problems:
            self.get_record(pName=i)

        self.info(f"所有测评记录： {self.records}\nTotal: {len(self.records)}")
        self.info("正在从所有测评记录中提取AC代码")

        for i in self.records:
            self.get_code("http://oiclass.com" + i)

        if not self.do_not_save_snapshots.isChecked():
            self.info("正在获得题目的截图")
            thr = threading.Thread(target=self.capture_full_screen)
            thr.start()
            thr.join()
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
            self.info(f"正在将所有文件推送到仓库: {self.remote_url.text()} 中")
            self.push2remote()
        self.end = time.time()
        self.progress = self.total_progress
        self.update_signal.emit()
        self.login_driver.close()
        self.critical(f"在 {self.end - self.start} 秒中成功")

    # 更新进度条
    def update_progress(self):
        # 向槽："update_signal" 发送信号
        self.update_signal.emit()

    # 检查系统是否安装了 git
    @staticmethod
    def check_git() -> bool:
        command_log = ""
        for i in os.popen("git"):
            command_log += i
        if "command not found" in command_log:
            return False
        return True

    # 取消，但是实际上好像是强制停止，额~~~~~~~
    def cancel(self):
        self.start_button.setText("开始")
        self.start_button.clicked.connect(self.create_main)
        sys.exit(0)

    # 推送到远程代码仓库，还没实现
    def push2remote(self):
        if not self.check_git():
            self.info("系统并未安装git，正在尝试安装")
            for i in os.popen("brew install git"):
                self.info(i)
        ############
        # NEED DEV #
        ############

    def get_file_path(self):
        self.path = QFileDialog.getExistingDirectory()
        for i in range(len(self.path)):
            if i % 10 == 0:
                self.path
        self.save_path.setText(self.path)

    # 生成 md 文件，方便保存后的查阅
    def generate_md(self):
        md_header = f"# All the answer I write from [{self.oj_url.text()}]({self.oj_url.text()})\n# " \
               f"[{self.oj_url.text()}]({self.oj_url.text()})上的所有我写的题解\n"
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

    # 截图
    def capture_full_screen(self):
        driver = self.login_driver
        for i in self.snapshot_reqs:
            self.progress += 1
            self.update_progress()
            driver.get(i.url)
            # 通过 JS 获得页面的宽高
            width = driver.execute_script("return document.documentElement.scrollWidth")
            height = driver.execute_script("return document.documentElement.scrollHeight")
            # 设置虚拟浏览器的宽高，方便接全屏
            driver.set_window_size(width, height)
            with open(i.filename, "wb") as file:
                # 截屏并保存在 "i.filename" 中
                file.write(driver.get_screenshot_as_png())
            self.info(f"题目截图: {i.filename} 完成")

    # 获得测评记录
    def get_record(self, pName: str):
        self.progress += 1
        self.update_progress()
        self.info(f"为 {pName} 获取测评记录")
        # 爬评测记录界面
        problem_page = self.login_session.get(url=f"http://oiclass.com/p/{pName}/").text
        self.snapshot_reqs.append(SnapshotReq(f"http://oiclass.com/p/{pName}/",
                                              f"{self.path}/{pName}.png"))
        soup = BeautifulSoup(features="lxml", markup=problem_page)
        idx = soup.find_all(name="span", class_="bp4-tag bp4-large bp4-minimal problem__tag-item")
        for j in idx:
            if "ID" in j.text:
                # 获取题目的 PID （PID：详见 Hydro 官方的描述）
                idx = j.text.split(" ")[1]
                break
        self.info(f"题目PID: {idx}")
        record = ""
        # 爬取测评记录
        try:
            record = self.login_session.get(url=f"http://oiclass.com/record?uidOrName=8241&pid={idx}&status=1").text
        except requests.exceptions.ConnectionError:
            self.error(
                "无法连接到 " + f"http://oiclass.com/record?uidOrName=8241&pid={idx}&status=1")
        soup = BeautifulSoup(markup=record, features="lxml")
        a = soup.find_all(name="a", class_="record-status--text pass")
        if a:
            # 保存最近的一次 AC 记录的 URL
            self.records.append(RecordData(pName=pName, url=a[0]["href"]))
            self.info(f"测评记录: http://oiclass.com{a[0]['href']}")
        else:
            self.warning("无法以本模式获得测评记录, 尝试另一种模式")
            self.retry_by_old_way(idx)

    # 从测评记录中获得代码;
    def get_code(self, record_data: RecordData):
        print(str(type(record_data)))
        # 更新进度条
        self.progress += 1
        self.update_progress()
        self.info(f"正在为测评记录 {record_data.url} 生成代码")
        b = []
        code = self.login_session.get(url=record_data.url + "?download=true", headers=self.headers).content.decode("utf-8")
        if code:
            with open(self.path + "/" + record_data.pName + ".cpp", "wt") as file:
                file.write(f"// Created in {time.asctime(time.localtime(time.time()))}\n"
                           f"// System: {platform.platform()}\n// Python Version: {platform.python_version()}\n{code}")
        return code

    # 老方法：用题目页面显示出的记录进行代码的保存，这种方法可能导致存储的是你的一次提交时抄的题解（doge）
    def retry_by_old_way(self, pName):
        driver = self.login_driver
        record = BeautifulSoup(markup=self.login_session.get("http://oiclass.com/p/" + str(pName)).text,
                               features="lxml").find_all(name="a", class_="")
        for j in record:
            if "/record/" in j["href"]:
                record = j["href"]
                break
        if type(record) != str:
            self.error(f"问题 {pName} 从来都没有被提交过，详情: http://oiclass.com/p/{pName}/")
            return 0
        self.info(f"尝试以提交题目： {pName} ")
        code = self.get_code(RecordData(pName=pName, url=self.oj_url.text() + record))
        try:
            driver.get("http://oiclass.com/p/" + pName + "/submit/")
            js = r'var x = document.getElementsByClassNam' \
                 r'e("' + r'textbox monospace' + r'"); x.code.value = `' + code + '`'
            driver.execute_script(script=js)
            driver.find_element(by="xpath",
                                value=r'//*[@id="panel"]/div[3]/div/div[1]/div/div[2]/form/div[5]/div/input[2]').click()
        except:
            ...

    # 获取所有 AC 过的题目
    def get_problems(self):
        # 爬取个人简页页面
        page = self.login_session.get(url=f"http://oiclass.com/user/{self.uid}").text
        soup = BeautifulSoup(markup=page, features="lxml")
        problems = soup.find_all(name="a")  # 筛选所有 a 标签（不知道什么是 a 标签的去学前端）
        # 获得目录下所有保存过的题目
        all_files = []
        for j in os.walk(self.path):
            all_files.append(j[2])
        if all_files:
            all_files = all_files[0]
        # 如果勾选了跳过已提交以加速选项
        if self.skip_problems.isChecked():
            for j in problems:
                if "/p/" in j["href"]:
                    p = False
                    for k in all_files:
                        # 如果题目已经存在
                        if k == j["href"].split("/")[2] + ".cpp" or k == j["href"].split("/")[2] + ".png":
                            p = True
                            break  # 退出循环，不把题号加入所有题号中
                    if not p:
                        # 如果循环了一遍后找不到，那么说明这是新的题目，加入所有题号中
                        self.ac_problems.append(j.text)
        else:
            # 正常操作，将所有题号加入到列表中
            for j in problems:
                if "/p/" in j["href"]:
                    self.ac_problems.append(j.text)

    # 一大堆日志，随便写的，请吐槽
    def info(self, msg):
        logging.info(msg)
        self.log_str = "[信息] " + msg
        self.add_log.emit()

    def warning(self, msg):
        logging.warning(msg)
        self.log_str = "[警告] " + msg
        self.add_log.emit()

    def error(self, msg):
        logging.error(msg)
        self.log_str = "[错误] " + msg
        self.add_log.emit()

    def critical(self, msg):
        logging.critical(msg)
        self.log_str = "[最重要信息] " + msg
        self.add_log.emit()


if __name__ == '__main__':
    app = QApplication([])
    window = QMainWindow()
    main = Main(window)
    apply_stylesheet(app, theme='dark_blue.xml')  # 设置主题
    main.setupSignal()
    window.show()
    logging.basicConfig(level=logging.INFO)
    exit_code = app.exec()  # 运行
    sys.exit(exit_code)


