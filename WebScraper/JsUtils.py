#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/10/21 10:44
# @Author  : mirko
# @FileName: JsUtils.py
# @Software: PyCharm

WINDOW_OPEN = "window.open(\"{0}\", \"{1}\")"

DOCUMENT_STATUS ="return document.readyState"

JQUERY_AJAX_STATUS = "return window.jQuery != undefined && jQuery.active == 0"

GET_ITEM_CSS_PATH = """
                        var el = arguments[0];
                        var cssPath = function(el){
                          var names = [];
                          while (el.parentNode){
                            if (el.id){
                              names.unshift('#'+el.id);
                              break;
                            }else{
                              if (el==el.ownerDocument.documentElement) {
                                names.unshift(el.tagName.toLocaleLowerCase());                              
                              }
                              else{
                                for (var c=1,e=el;e.previousElementSibling;e=e.previousElementSibling,c++);
                                names.unshift(el.tagName.toLocaleLowerCase()+":nth-child("+c+")");
                              }
                              el=el.parentNode;
                            }
                          }
                          return names.join(" > ");
                        }
                        return cssPath(el)
                    """


TRIGGER_ELEMENT_CLICK = """
                            var el = document.querySelectorAll(\'{css_selector}\')[0]; 
                            console.log(el);
                            el.click();
                            console.log(document.querySelectorAll(\'div.thumbnail\'));
                        """