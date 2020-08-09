#/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import io
import telnetlib
import time
import optparse
import random
from datetime import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


host = 'ptt.cc'
# user = 
# password = 

def login(host, user ,password) :
    random.seed(datetime.now())
    random_time = random.randint(5, 300)

    print_utf8("登入ing...")
    global telnet
    telnet = telnetlib.Telnet(host)

    for t in range(random_time,-1,-1):
        sys.stdout.write("wait for {} sec...\r".format(t))
        sys.stdout.flush()
        time.sleep(1)

    content = telnet.read_very_eager().decode('big5','ignore')
    # print content
    if u"系統過載" in content :
        print_utf8("系統過載, 請稍後再來")
        sys.exit(0)

    if u"請輸入代號" in content:
        # print_utf8('輸入帳號中...')
        telnet.write(user + "\r\n" )
        time.sleep(1)
        # print_utf8("輸入密碼中...")
        telnet.write(password + "\r\n")
        time.sleep(5)
        content = telnet.read_very_eager().decode('big5','ignore')
        # print content
        if u"密碼不對" in content:
            print_utf8('密碼不對或無此帳號。程式結束')
            sys.exit()
            content = telnet.read_very_eager().decode('big5','ignore')
        if u"您想刪除其他重複登入" in content:
            print_utf8('刪除其他重複登入的連線....')
            telnet.write("y\r\n")
            time.sleep(10)
            content = telnet.read_very_eager().decode('big5','ignore')
        if u"請按任意鍵繼續" in content:
            # print_utf8("資訊頁面，按任意鍵繼續...")
            telnet.write("\r\n" )
            time.sleep(2)
            content = telnet.read_very_eager().decode('big5','ignore')
        if u"您要刪除以上錯誤嘗試" in content:
            print_utf8("刪除以上錯誤嘗試...")
            telnet.write("y\r\n")
            time.sleep(5)
            content = telnet.read_very_eager().decode('big5','ignore')
        if u"您有一篇文章尚未完成" in content:
            print_utf8('刪除尚未完成的文章....')
            # 放棄尚未編輯完的文章
            telnet.write("q\r\n")   
            time.sleep(5)   
            content = telnet.read_very_eager().decode('big5','ignore')
        f = open('login_history_{}.txt'.format(user), "at+")
        f.write(time.strftime("%Y/%m/%d %H:%M:%S\n\r",time.localtime()))
        f.close()
        print_utf8("登入完成!")
    else:
        print_utf8("沒有可輸入帳號的欄位，網站可能掛了")

def disconnect() :
        print_utf8("登出ing...")
        # q = 上一頁，直到回到首頁為止，g = 離開，再見
        telnet.write("qqqqqqqqqg\r\ny\r\n" )
        time.sleep(3)
        # content = telnet.read_very_eager().decode('big5','ignore')
        # print content
        print_utf8("登出完成!")
        telnet.close()

def print_utf8(string):
    print unicode(string, encoding="utf-8")

def get_opts():
    parser = optparse.OptionParser()
    parser.add_option("--user", dest="user", help="user name")
    parser.add_option("--password", dest="password", help="password")
    opts, args = parser.parse_args()
    return opts, args

if __name__=="__main__" :
    opts, args = get_opts()
    print "user name: "+opts.user
    login(host, opts.user, opts.password)
    disconnect()