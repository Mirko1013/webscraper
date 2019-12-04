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

#HTMLCollection 做到了随着DOM元素的改变进行动态的变化，而NodeList并不会即时更新元素集合中的值
#大多数情况下，NodeList对象都是一个实时变化（即时更新）的集合,但是，在另外一些情况下，NodeList是一个静态的集合
#这也就意味着随后对DOM元素的任何改动都不会影响NodeList 集合内的内容document.querySelectorAll()方法返回的就是一个静态的NodeList
TRIGGER_ELEMENT_CLICK = """
                            const callback = arguments[arguments.length - 1]
                            var css = arguments[0];
                            var el = document.querySelectorAll(css)[0];  
       
                            el.addEventListener('click', function() {
                                setTimeout(function(){callback(true);}, 500);
                            });  
                            el.click();          
                        """


SCROLL_TO_BOTTOM = """
                        const callback = arguments[arguments.length - 1];
                        function get_window_height() {
                            return window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight || 0;
                        }
                        function get_window_Yscroll() {
                            return window.pageYOffset || document.body.scrollTop || document.documentElement.scrollTop || 0;
                        }
                        function get_doc_height() {
                            return Math.max(document.body.scrollHeight || 0, document.documentElement.scrollHeight || 0, document.body.offsetHeight || 0, document.documentElement.offsetHeight || 0, document.body.clientHeight || 0, document.documentElement.clientHeight || 0);
                        }
                        
                        function get_scroll_percentage() {
                            return ((get_window_Yscroll() + get_window_height()) / get_doc_height()) * 100;
                        }
                        
                        window.addEventListener('scroll', function(){
                            var page_height = get_doc_height();
                            var viewport_height = get_window_height();
                            var y_scroll = get_window_Yscroll();
                            
                            if (page_height - viewport_height -y_scroll < 20) {
                                setTimeout(function(){callback(get_scroll_percentage());}, 500);
                            }
                       })
                        
                        window.scrollTo(0, get_doc_height());
                    
                   """

