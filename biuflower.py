#! /usr/bin/python2
# -*- coding: utf-8-*-
from Tkinter import *
import tkMessageBox
import urllib2
import urllib
import zlib
import json
import os

def post(req,data):  
    '''Send post resquest
    '''
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())  
    response = opener.open(req, data) 
    global respInfo
    respInfo = response.info()
    return response.read()

#setting
class Setting_window:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        top.geometry('260x110')  
        input_frm = Frame(top)
        self.bkn_lab = Label(input_frm, text='bkn:', font=('Arial', 15)).grid(row=0)
        self.cookie_lab = Label(input_frm, text='cookie:', font=('Arial', 15)).grid(row=1)
        self.bkn_ipt = StringVar()
        self.e_bkn = Entry(input_frm, textvariable = self.bkn_ipt)
        self.cookie_ipt = StringVar()
        self.e_cookie = Entry(input_frm, textvariable = self.cookie_ipt)
        self.e_bkn.grid(row=0, column=1)
        self.e_cookie.grid(row=1, column=1)
        input_frm.pack()

        self.save = Button(top, text='save', command=self.save)
        self.save.pack()
        if os.path.exists('biuflower.json'):
            with open("biuflower.json","r") as cfg:
                cfg_json = json.loads(cfg.read())
                cookie_dic["cookie"] = cfg_json["cookie"]
                cookie_dic['bkn'] = cfg_json['bkn']
            self.e_bkn.insert(0,cookie_dic['bkn'])
            self.e_cookie.insert(0,cookie_dic['cookie'])
    def save(self):
        cookie_dic["cookie"] = self.e_cookie.get()
        cookie_dic["bkn"] = self.e_bkn.get()
        with open("biuflower.json",'w') as cfg:
            cfg_json = json.dumps(cookie_dic)
            cfg.write(cfg_json)
        tkMessageBox.showinfo("设置", "设置已保存")
        self.top.destroy()
def set_win():
    inputDialog = Setting_window(root)
    root.wait_window(inputDialog.top)


def biu():
    '''start biu
    '''
    if os.path.exists('biuflower.json'):
        with open("biuflower.json","r") as cfg:
            cfg_json = json.loads(cfg.read())
            cookie_dic["cookie"] = cfg_json["cookie"]
            cookie_dic['bkn'] = cfg_json['bkn']
        gc = gc_ipt.get()
        bkn = cookie_dic["bkn"]
        cookie = cookie_dic["cookie"]
        poi = poi_ipt.get().encode("utf-8")
        data = {}

        data["poi"] = poi

        #data encode as utf-8 urlencode.same as encode by dictionary
        string = "gc="+gc+"&is_sign=0&from=1&bkn="+bkn+"&"+urllib.urlencode(data)
        url = "http://qiandao.qun.qq.com/cgi-bin/sign"
        req = urllib2.Request(url)

        print string

        req_dic = {
            'host': "qiandao.qun.qq.com",
            'content-length': "37",
            'accept': "*/*",
            'content-type': "application/xml",
            'origin': "http//qiandao.qun.qq.com",
            'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.59 QQ/7.4.15203.201 Safari/537.36",
            'referer': "http//qiandao.qun.qq.com/index.html",
            'accept-language': "en-us,en",
            }
        for key in req_dic:
            req.add_header(key,req_dic[key])
        req.add_header("Content-Length",len(string)) #add COntent-Length
        req.add_header("cookie",cookie) #add COntent-Length

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
    else:
        tkMessageBox.showinfo("biu", "先设置bkn和cookie再biu吧")
# begin of GUI part
root = Tk()
root.title("签到练手GUI")
root.geometry('280x100')                 #是x 不是*
root.resizable(width=False, height=False) #宽不可变, 高可变,默认为True
frm = Frame(root)

Label(frm, text='gc:', font=('Arial', 15)).grid(row=0)
Label(frm, text='poi:', font=('Arial', 15)).grid(row=1)

gc_ipt = StringVar()
e_gc = Entry(frm, textvariable = gc_ipt)
poi_ipt = StringVar()
e_poi = Entry(frm, textvariable = poi_ipt)
e_gc.grid(row=0, column=1)
e_poi.grid(row=1, column=1)

#Button
Button(frm, text="set", command=set_win, width=10, height=1, font=('Arial', 10)).grid(row=3, column=0)
Button(frm, text="biu", command=biu, width=10, height=1, font=('Arial', 10)).grid(row=3, column=1)

frm.pack()
cookie_dic = {}
root.mainloop()