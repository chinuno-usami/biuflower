#! /usr/bin/python2
# -*- coding: utf-8-*-
from Tkinter import *
import tkMessageBox
import urllib2
import urllib
import zlib
import json
def post(req,data):  
    '''Send post resquest
    '''
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())  
    response = opener.open(req, data) 
    # print response.read().decode('utf-8') 
    global respInfo
    respInfo = response.info()
    return response.read()

def biu():
    '''start biu
    '''
    gc = gc_ipt.get()
    bkn = bkn_ipt.get()
    # cookie = raw_input("cookie:")
    poi = poi_ipt.get().encode("utf-8")
    data = {}
    # data['gc'] = gc
    # data['bkn'] = bkn
    # data["poi"] = poi
    # data["is_sign"] = "1"
    # data["from"] = "1"
    data["poi"] = poi

    #data encode as utf-8 urlencode.same as encode by dictionary
    string = "gc="+gc+"&is_sign=0&from=1&bkn="+bkn+"&"+urllib.urlencode(data)
    url = "http://qiandao.qun.qq.com/cgi-bin/sign"
    req = urllib2.Request(url)

    # post_data = urllib.urlencode(data)
    # print post_data
    print string


    with open("header.txt",'r') as fp_head: #Load header file
        head_dic = {}

        for line in fp_head.readlines():
            line_lst = line.replace('\n','').replace('\r','').split(": ")
            if line_lst[0]:
                head_dic[line_lst[0]] = line_lst[1]
        for key in head_dic:
            req.add_header(key,head_dic[key])
        req.add_header("Content-Length",len(string)) #add COntent-Length


    # content = post(req,post_data)
    content = post(req,string)
    #decompress as gzip
    if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")) :
        content = zlib.decompress(content, 16+zlib.MAX_WBITS)
    print content.decode("utf-8").encode("gbk")

    content_dic = json.loads(content)
    if content_dic["ec"] == 0:
        tkMessageBox.showinfo("biu", "快去看看成功了没！")
    elif content_dic["ec"] == 1:
        tkMessageBox.showinfo("biu", "cookie过期了。重新抓包吧")
    else:
        tkMessageBox.showinfo("biu", "出错啦。检查看看有没有什么地方填错了")

# begin of GUI part
root = Tk()
root.title("签到练手GUI")
root.geometry('400x120')                 #是x 不是*
root.resizable(width=False, height=True) #宽不可变, 高可变,默认为True
frm = Frame(root)
#left
frm_L = Frame(frm)
Label(frm_L, text='gc:'.decode('gbk').encode('utf8'), font=('Arial', 15)).pack(side=TOP)
Label(frm_L, text='bkn:'.decode('gbk').encode('utf8'), font=('Arial', 15)).pack(side=TOP)
Label(frm_L, text='poi:'.decode('gbk').encode('utf8'), font=('Arial', 15)).pack(side=TOP)
frm_L.pack(side=LEFT)

#right
frm_R = Frame(frm)
gc_ipt = StringVar()
e1 = Entry(frm_R, textvariable = gc_ipt).pack(side=TOP)
bkn_ipt = StringVar()
e2 = Entry(frm_R, textvariable = bkn_ipt).pack(side=TOP)
poi_ipt = StringVar()
e2 = Entry(frm_R, textvariable = poi_ipt).pack(side=TOP)
frm_R.pack(side=RIGHT)
#Mid
frm_B = Frame(root)
Button(frm_B, text="biu", command=biu, width=10, height=1, font=('Arial', 10)).pack(side=TOP)
frm_B.pack(side=TOP)


frm.pack()

root.mainloop()