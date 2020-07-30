# -*- coding: utf-8 -*-
import sys
import io
import telnetlib
import time
import optparse

host = 'ptt.cc'
# user = 
# password = 

def login(host, user ,password) :
    global telnet
    telnet = telnetlib.Telnet(host)
    time.sleep(1)
    content = telnet.read_very_eager().decode('big5','ignore')
    # print content
    if u"系統過載" in content :
        print "系統過載, 請稍後再來"
        sys.exit(0)

    if u"請輸入代號" in content:
        print "輸入帳號中..."
        telnet.write(user + "\r\n" )
        time.sleep(1)
        print "輸入密碼中..."
        telnet.write(password + "\r\n")
        time.sleep(5)
        content = telnet.read_very_eager().decode('big5','ignore')
        # print content
        if u"密碼不對" in content:
            print "密碼不對或無此帳號。程式結束"
            sys.exit()
            content = telnet.read_very_eager().decode('big5','ignore')
        if u"您想刪除其他重複登入" in content:
            print '刪除其他重複登入的連線....'
            telnet.write("y\r\n")
            time.sleep(10)
            content = telnet.read_very_eager().decode('big5','ignore')
        if u"請按任意鍵繼續" in content:
            print "資訊頁面，按任意鍵繼續..."
            telnet.write("\r\n" )
            time.sleep(2)
            content = telnet.read_very_eager().decode('big5','ignore')
        if u"您要刪除以上錯誤嘗試" in content:
            print "刪除以上錯誤嘗試..."
            telnet.write("y\r\n")
            time.sleep(5)
            content = telnet.read_very_eager().decode('big5','ignore')
        if u"您有一篇文章尚未完成" in content:
            print '刪除尚未完成的文章....'
            # 放棄尚未編輯完的文章
            telnet.write("q\r\n")   
            time.sleep(5)   
            content = telnet.read_very_eager().decode('big5','ignore')
        print "----------------------------------------------"
        print "------------------ 登入完成 -------------------"
        print "----------------------------------------------"
    else:
        print "沒有可輸入帳號的欄位，網站可能掛了"

def disconnect() :
        print "登出中..."
        # q = 上一頁，直到回到首頁為止，g = 離開，再見
        telnet.write("qqqqqqqqqg\r\ny\r\n" )
        time.sleep(3)
        # content = telnet.read_very_eager().decode('big5','ignore')
        # print content
        print "----------------------------------------------"
        print "------------------ 登出完成 ------------------"
        print "----------------------------------------------"
        telnet.close()

def get_opts():
    parser = optparse.OptionParser()
    parser.add_option("--user", dest="user", help="user name")
    parser.add_option("--password", dest="password", help="password")
    opts, args = parser.parse_args()
    return opts, args

if __name__=="__main__" :
    opts, args = get_opts()
    login(host, opts.user, opts.password)
    disconnect()