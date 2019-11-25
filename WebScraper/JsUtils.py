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
                        function getDomPath(el) {
                          var stack = [];
                          while ( el.parentNode != null ) {
                            console.log(el.nodeName);
                            var sibCount = 0;
                            var sibIndex = 0;
                            for ( var i = 0; i < el.parentNode.childNodes.length; i++ ) {
                              var sib = el.parentNode.childNodes[i];
                              if ( sib.nodeName == el.nodeName ) {
                                if ( sib === el ) {
                                  sibIndex = sibCount;
                                }
                                sibCount++;
                              }
                            }
                            if ( el.hasAttribute('id') && el.id != '' ) {
                              stack.unshift(el.nodeName.toLowerCase() + '#' + el.id);
                            } else if ( sibCount > 1 ) {
                              stack.unshift(el.nodeName.toLowerCase() + ':eq(' + sibIndex + ')');
                            } else {
                              stack.unshift(el.nodeName.toLowerCase());
                            }
                            el = el.parentNode;
                          }
                        
                          return stack.slice(1); // removes the html element
                        }
                        return getDomPath(el).join(' > ');
"""

# "var el = arguments[0]; var cssPath = function(el){"  +
#                     "if (!(el isinstanceof Element)) return;" +
#                             "var path=[]; " +
#                             "while (el.nodeType === Node.ELEMENT_NODE) {" \
#                                 "var selector = el.nodeName.toLowerCase();"\
#                                 "if(el.id) {" +\
#                                     "selector += \'#\' + el.id;" +\
#                                 "}else{" +\
#                                     "var sib = el, nth = 1;" +\
#                                     "whild (sib.nodeType === Node.ELEMENT_NODE && (sib = sib.perviousSibling) && nth++);" +\
#                                     "selector += \":nth-child(\"+nth+\")\";" +\
#                                 "}" +\
#                                 "path.unshif(selector);" +\
#                                 "el = el.parentNode;" +\
#                             "}" +\
#                             "return path.join(\" > \");" +\
#                     "};"

CLICK_ELEMENT = "var el = document.querySelectorAll(\'{css_selector}\')[0]; el.click();"