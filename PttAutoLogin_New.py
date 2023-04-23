# -*- coding: UTF-8 -*-
import sys
import optparse
import random
import time
from PyPtt import PTT
from datetime import datetime

def login(user ,password) :
    ptt_bot = PTT.API()
    try:
        random.seed(datetime.now())
        random_time = random.randint(5, 300)
        for t in range(random_time,-1,-1):
            sys.stdout.write("wait for {} sec...\r".format(t))
            sys.stdout.flush()
            time.sleep(1)
        ptt_bot.login(user, password)
    except PTT.exceptions.LoginError:
        ptt_bot.log('登入失敗')
        sys.exit()
    except PTT.exceptions.WrongIDorPassword:
        ptt_bot.log('帳號密碼錯誤')
        sys.exit()
    except PTT.exceptions.LoginTooOften:
        ptt_bot.log('請稍等一下再登入')
        sys.exit()

    random.seed(datetime.now())
    random_time = random.randint(10, 100)
    for t in range(random_time,-1,-1):
        sys.stdout.write("wait for {} sec...\r".format(t))
        sys.stdout.flush()
        time.sleep(1)

    ptt_bot.log('登入成功')
    f = open('login_history_{}.txt'.format(user), "at+")
    f.write(time.strftime("%Y/%m/%d %H:%M:%S",time.localtime())+'\n')
    f.close()

    # if ptt_bot.unregistered_user:
    #     print('未註冊使用者')

    # if ptt_bot.process_picks != 0:
    #     print(f'註冊單處理順位 {ptt_bot.process_picks}')

    # if ptt_bot.registered_user:
    #     print('已註冊使用者')

    # call ptt_bot other api

    ptt_bot.logout()

def get_opts():
    parser = optparse.OptionParser()
    parser.add_option("--user", dest="user", help="user name")
    parser.add_option("--password", dest="password", help="password")
    opts, args = parser.parse_args()
    return opts, args

if __name__=="__main__" :
    opts, args = get_opts()
    print (f"user name: {opts.user}")
    login(opts.user, opts.password)
