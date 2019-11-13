#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/10/21 10:44
# @Author  : mirko
# @FileName: JsUtils.py
# @Software: PyCharm

WINDOW_OPEN = "window.open(\"{0}\", \"{1}\")"

DOCUMENT_STATUS ="return document.readyState"

GET_ITEM_CSS_PATH = "var el = arguments[0]; function(el){"+ \
                    "if (!(el isinstanceof Element)) return;" + \
                            "var path=[]; "+ \
                            "while (el.nodeType === Node.ELEMENT_NODE) {" +\
                                "var selector = el.nodeName.toLowerCase();"+\
                                "if(el.id) {" +\
                                    "selector += \'#\' + el.id;" +\
                                "}else{" +\
                                    "var sib = el, nth = 1;" +\
                                    "whild (sib.nodeType === Node.ELEMENT_NODE && (sib = sib.perviousSibling) && nth++);" +\
                                    "selector += \":nth-child(\"+nth+\")\";" +\
                                "}" +\
                                "path.unshif(selector);" +\
                                "el = el.parentNode;" +\
                            "}" +\
                            "return path.join(\" > \");" +\
                    "}"

CLICK_ELEMENT = "var el = document.querySelectorAll(\'{css_selector}\')[0]; el.click();"