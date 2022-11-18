# Fish

# 鱼

## Let you work just like Fish in Hydro

## 让你工作得如鱼得水

[中文](./README_ZH.md)     [English](./README.md)

*This english README is translate by machine, sorry.*

##### This project is designed for more convenient use of [HydroOJ](https://hydro.js.org), functions:

- [x] Batch download AC title code

- [ ] Pushes the downloaded code to the git repository

- [ ] Filters comments and saves them

#### Common Hydro-based OJ: [Oiclass.com](http://www.oiclass.com), [Vijos](https://vijos.org/), [hydro-.ac](https://hydro.ac)

#### Implementation Principle

##### 1, frame:

- Python 3.11 is used to write programs

- Selenium + Chromedriver implements browser simulation

- Request Implements batch http requests

- pygit2 Implements git operations

- PySide 6 Implements communication between multiple threads on the UI

- BeautifulSoup implements html parsing and extracts data from it

- Pyinstaller compiles and packages code

##### 2, ideas:

    Algorithm: Crawling data and manipulating web pages through Selenium and Request, passing the data into BeautifulSoup for analysis and cleaning, and then going back to Requests and Selenium for further action (submit to OJ, get detailed data, etc.)

    UI: Use a textarea to output logs and set the operations and parameters on the left

##### Welcome everyone to submit PR *LOVE*
