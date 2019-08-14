#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/16 11:09 AM
# @Author  : mirko
# @FileName: main.py
# @Software: PyCharm

import json
from Crawler.sitemap import Sitemap



if __name__ == '__main__':
    #
    # os.environ["PATH"] += ":" + os.path.abspath("./webdriver")
    #
    # options = Options()
    # driver = webdriver.Chrome(chrome_options=options)
    # driver.get("http://www.baidu.com")
    # driver.quit()

    sitemap_json = str()

    with open("sitemap.json", encoding="utf-8") as f:
        sitemap_json = json.load(f)

    sitemap = Sitemap(sitemap_json.get("_id"), sitemap_json.get("startUrl"), sitemap_json.get("selectors"))
    print("end")