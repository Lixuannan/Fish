# Fish

# 鱼

## Let you work just like Fish in Hydro

## 让你工作得如鱼得水

[中文](./README_ZH.md)     [English](./README.md)

##### 本项目用于更加方便的 [HydroOJ](https://hydro.js.org) 使用，功能：

- [x] 批量下载 AC 的题目的代码

- [ ] 将下载好的代码推送到 git 仓库

- [ ] 筛选评论并保存

#### 常见的基于 Hydro 的 OJ：[Oiclass.com](http://www.oiclass.com), [Vijos](https://vijos.org/), [Hydro.ac](https://hydro.ac)

### 实现原理

##### 1，框架:

* Python 3.11 用来编写程序

* Selenium + Chromedriver 实现浏览器模拟

* Request 实现批量 http 请求

* pygit2 实现 git 操作

* PySide 6 实现 UI 界面同时完成多线程之间的通信

* BeautifulSoup 实现 html 解析并提取其中的数据

* Pyinstaller 进行代码的编译与打包

##### 2，思路：

    算法：通过 Selenium 和 Request 进行数据的爬取和网页的操纵，然后将数据传入 BeautifulSoup 中分析清洗，然后回到 Requests 和 Selenium 进行进一步操作（提交到OJ、获取详细数据 etc.）

    UI：用一个 textarea 输出日志，在左边进行操作及参数的设定

### 运行：

```shell
pip3 install -r requirements.txt
python3 main.py
```

##### 欢迎大家积极提交 PR *笔芯*
