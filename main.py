import datetime
import os
import sys
import time

import pyautogui
import requests
from xpinyin import Pinyin

class ForeverMemoryClient:

    def __init__(self):
        self.start_user_index = 0
        self.pic_cnt = 0
        self.log_file = "logs/out.log"
        self.code = "112235"
        self.default_input_interval = 0.05
        self.default_delay = 1
        self.first_start_delay = 5

        self.seal_interval = 10
        self.check_interval = 20 * 6

        self.run_cnt = 0
        self.screenshot_cnt = 0
        self.seal_cnt = 0
        self.hour = -1
        self.nongzuowei = "nangua"
        self.user_list = []
        # self.nongzuowei = "xrz"

        if "darwin" in sys.platform:
            self.os = "mac"
        else:
            self.os = "window"
        print(self.os)

    def log(self, msg):
        with open(self.log_file, 'a') as f:
            if msg is None:
                return
            level = "info"
            f.writelines("time={},level={},msg={}\n".format(str(datetime.datetime.now()), level, msg))

    # find pic location,
    def while_get_pic(self, pic_file, cnt, confidence, desc, region):
        pic_file = "imgs/" + self.os + "/" + pic_file
        self.log("start find  desc={},pic_file={},cnt={},confidence={}".format(
            desc, pic_file, cnt, confidence))
        for i in range(0, cnt):
            if i == 0:
                self.log(
                    "start find {},desc={},pic_file={},cnt={},confidence={}".format(i, desc, pic_file, cnt,
                                                                                    confidence))
            else:
                self.log("retry find desc={},pic_file={},cnt={},current_cnt={},confidence={}".format(
                    desc, pic_file, cnt, i, confidence))
            if region is None:
                pos = pyautogui.locateCenterOnScreen(pic_file, confidence=confidence, region=region)
            else:
                pos = pyautogui.locateCenterOnScreen(pic_file, confidence=confidence)
            if pos is not None:
                self.log("get desc={},pic_file={},cnt={},current_cnt={},confidence={}".format(
                    desc, pic_file, cnt, i, confidence))
                return pos

            time.sleep(0.43)
        self.log("not get desc={},pic_file={},cnt={},current_cnt={},confidence={}".format(
            desc, pic_file, cnt, cnt, confidence))
        return None

    def click_pos(self, pos, desc, click_cnt):
        if pos is None:
            self.log("pos is none,desc={}".format(desc))
            return
        pyautogui.moveTo(pos[0] / 2, pos[1] / 2, duration=0.5)

        if click_cnt == 1:
            pyautogui.click()
        if click_cnt == 2:
            pyautogui.doubleClick()
        time.sleep(1)

    def run_v4(self):
        start_message = "start,with first_start_delay={}".format(self.first_start_delay)
        print(start_message)
        self.log(start_message)
        self.read_users()
        self.close_app()
        self.open_pre()
        time.sleep(0.2)
        while True:
            if self.start_user_index >= len(self.user_list):
                self.start_user_index = 0
            self.open_v2(self.user_list[self.start_user_index])
            # time.sleep(4)
            self.login_with_code()
            self.choice_shengcun()
            self.login_into_shengcun()
            self.sleep_while2(0.2,40)
            self.goto_area_2()
            self.sleep_while2(0.2, 40)
            self.goto_nangua()
            #self.goto_nangua_ext()
            self.sleep_while2(0.2,40)
            self.goto_area_0_ext()
            self.sleep_while2(0.2, 40)
            time.sleep(1)
            self.seal()
            time.sleep(0.8)
            self.pay_money()
            self.start_user_index +=1
            self.update_index()
            self.close()


    # 有账号后:
    #
    #     账户列表文件。
    #
    #     for user in user_list:
    #         stop
    #         start
    #         login
    #         选择生存
    #         点击生存
    #         进入2区
    #         进入南瓜
    #         等待20s
    #         回到/home h0
    #         右键， 售卖
    #         打款个主账户

    def run_v3(self):

        start_message = "start,with first_start_delay={}".format(self.first_start_delay)
        print(start_message)
        self.log(start_message)
        self.prepare_works()
        while True:
            try:
                pos = self.while_get_pic("nongzuowu.png", 5, 0.6, "nongzuowu", region=None)
                if pos is None:
                    time.sleep(60)
                    self.prepare_works()
                self.seal()
                time.sleep(self.seal_interval)
            except Exception as err:
                self.log("error={}".format(err))

    def seal(self):
        pyautogui.rightClick()
        time.sleep(2)
        pos = self.while_get_pic("nangua.png", 5, 0.6, "nangua", region=None)
        self.click_pos(pos,desc="nangua",click_cnt=0)
        time.sleep(2.5)
        pyautogui.press("f")
        time.sleep(2)
        pyautogui.press("esc")

    def get_ip_port(self):
        cookies = {
            'http_waf_cookie': '5b66a1d2-bbb5-4d7ff9aa717c5c387745027836a86decfc09',
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            # 'Cookie': 'http_waf_cookie=5b66a1d2-bbb5-4d7ff9aa717c5c387745027836a86decfc09',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.70',
        }

        response = requests.get(
            'http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=0&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=1&lb=1&sb=0&pb=5&mr=1&regions=320000',
            cookies=cookies, headers=headers, verify=False)
        resp_json=response.json()
        print(resp_json)
        return resp_json["data"][0]["ip"],resp_json["data"][0]["port"]


    def prepare_works(self):
        print("prepare_work")
        self.pic_cnt = 0
        # self.entry_server()
        self.close()
        self.open()
        # time.sleep(20)
        # self.login_hub()
        time.sleep(2)
        self.login_with_code()
        # time.sleep(1)
        self.choice_shengcun()
        # time.sleep(1)
        self.login_into_shengcun()
        time.sleep(30)
        if self.nongzuowei == "nangua":
            self.goto_nangua()
            time.sleep(10)
            # self.open_nangua()
            # time.sleep(1)
            pass

    def register(self):
        pyautogui.write('/register  ' + self.code + " " + self.code, self.default_input_interval)
        pyautogui.press('enter')

    def login_with_code(self):
        pyautogui.write('/login  ' + self.code, interval=self.default_input_interval)
        pyautogui.press('enter')
        time.sleep(0.2)

    def choice_shengcun(self):
        self.log("start choice shengcun")
        pyautogui.press("t")
        pyautogui.write("/bs bc", interval=self.default_input_interval)
        pyautogui.press('enter')
        time.sleep(0.2)

    def login_into_shengcun(self):
        pos = self.while_get_pic('shengcun.png', cnt=5, confidence=0.85, desc="shengcun-server", region=None)
        self.click_pos(pos, "shengcun-server", 2)
        time.sleep(0.2)

    def goto_area_0(self):
        pyautogui.write('/bs', interval=self.default_input_interval)
        pyautogui.press('enter')
        pos = self.while_get_pic('zhucheng.png', cnt=2, confidence=0.82, desc="zhucheng", region=None)
        self.click_pos(pos, "zhucheng", 1)
        time.sleep(0.2)
    def goto_area_0_ext(self):
        pyautogui.write('/home h0', interval=self.default_input_interval)
        pyautogui.press('enter')
        time.sleep(0.2)

    def goto_area_2(self):
        pyautogui.write('/bs', interval=self.default_input_interval)
        pyautogui.press('enter')
        pos = self.while_get_pic('erqu.png', cnt=2, confidence=0.82, desc="xrz-seal-button", region=None)
        self.click_pos(pos, "erqu", 1)
        time.sleep(0.2)


    def goto_nangua(self):
        pyautogui.write('/res tp panda_nangua.gj', interval=self.default_input_interval)
        pyautogui.press('enter')
        time.sleep(15)
        pyautogui.write('/sethome h2 ', interval=self.default_input_interval)
        pyautogui.press('enter')
        time.sleep(0.6)

    def goto_nangua_ext(self):
        pyautogui.write('/home h2', interval=self.default_input_interval)
        pyautogui.press('enter')



    def open_nangua(self):
        pyautogui.write('/bs sg200', interval=self.default_input_interval)
        pyautogui.press('enter')
        pyautogui.moveTo(100, 100)
        time.sleep(0.3)

        pos = self.while_get_pic('nangua.png', cnt=2, confidence=0.82, desc="nangua-seal-button", region=None)
        self.click_pos(pos, "first-seal-nangua", 1)
        self.log("pos={}".format(pos))
        time.sleep(0.3)

    def close_app(self):
        cmd1 = """ ps aux |grep MultiMC.app |grep -v grep  |grep MultiMC.app |awk '{print $2}' |while read pid ; do kill -9 $pid  ; done """
        os.system(cmd1)
        time.sleep(0.5)
        pass

    def close(self):
        pyautogui.press("esc")
        pos_duankai = self.while_get_pic('duankai.png', cnt=2, confidence=0.9, desc="instance", region=None)
        self.click_pos(pos_duankai, "new", 1)
        time.sleep(0.2)
        time.sleep(3)

    def sleep_while(self, sleep_interval, max_sleep_seconds, pic_file, desc, confidence):
        current_sleep_seconds = 0
        while True:
            pos = self.while_get_pic(pic_file, cnt=1, confidence=confidence, desc=desc, region=None)
            if pos is not None:
                return True, pos
            if current_sleep_seconds > max_sleep_seconds:
                return False, None
            time.sleep(sleep_interval)

    def open_pre(self):
        os.system("open /Applications/MultiMC.app")

        self.sleep_while(0.5, 20, pic_file='instance.png', confidence=0.9, desc="instance")
        pos = self.while_get_pic('instance.png', cnt=2, confidence=0.9, desc="instance", region=(0, 0, 800, 800))
        self.click_pos(pos, "open goad instance", 1)
        time.sleep(0.2)
        pos = self.while_get_pic('run.png', cnt=2, confidence=0.9, desc="run", region=None)
        self.click_pos(pos, "run", 1)

        max_cnt = 120
        cnt = 0
        while cnt < max_cnt:
            pos1 = self.while_get_pic('lixianbtn.png', cnt=1, confidence=0.9, desc="lixianbtn", region=None)
            if pos1 is not None:
                pyautogui.write("mc__panda")
                pyautogui.press("enter")
                time.sleep(1)
            pos2 = self.while_get_pic('duoren.png', cnt=1, confidence=0.9, desc="duoren", region=None)
            if pos2 is not None:
                self.click_pos(pos2, desc="duoren", click_cnt=2)
                break
            time.sleep(0.3)
            cnt += 1
        pyautogui.hotkey('ctrl', 'command', 'f')
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'command', '/')
        time.sleep(0.2)
        pyautogui.moveTo(400,100)
        # has, pos3 = self.sleep_while(0.5, 30, pic_file='mem.png', confidence=0.9, desc="duoren")
        # # print(has,pos3)

        # has, pos3 = self.sleep_while(0.5, 30, pic_file='mem.png', confidence=0.9, desc="duoren")
        # if has:
        #     if pos3 is not None:
        #         self.click_pos(pos3, desc="mem", click_cnt=2)
        time.sleep(10)

    def set_account(self,user):
        # 设置user
        pos_zhanghu = self.while_get_pic('zhanghu.png', cnt=2, confidence=0.9, desc="zhanghu", region=None)
        self.click_pos(pos_zhanghu, "zhanghu", 1)
        time.sleep(0.3)

        pos_hongxian = self.while_get_pic('hongxian.png', cnt=2, confidence=0.9, desc="instance", region=None)
        self.click_pos(pos_hongxian, "proxy", 1)
        time.sleep(0.2)

        pos_crack = self.while_get_pic('crack.png', cnt=3, confidence=0.9, desc="crack", region=None)
        self.click_pos(pos_crack, "crack", 1)
        time.sleep(0.5)
        pyautogui.write(user)
        time.sleep(0.2)
        pos_add = self.while_get_pic('add.png', cnt=2, confidence=0.9, desc="crack", region=None)
        self.click_pos(pos_add, "add", 1)
        time.sleep(6)
        pyautogui.press("esc")
    def set_proxy(self,user):
        self.set_account(user)
        # 设置代理注册账户
        pos_proxy = self.while_get_pic('proxy.png', cnt=2, confidence=0.9, desc="instance", region=None)
        self.click_pos(pos_proxy, "proxy", 1)
        time.sleep(0.2)
        pos_hongxian = self.while_get_pic('hongxian.png', cnt=2, confidence=0.9, desc="instance", region=None)
        self.click_pos(pos_hongxian, "proxy", 1)
        time.sleep(0.2)

        pos_new = self.while_get_pic('new.png', cnt=2, confidence=0.9, desc="instance", region=None)
        self.click_pos(pos_new, "new", 1)
        time.sleep(0.2)
        ip, port = self.get_ip_port()
        pyautogui.press("\t")
        pyautogui.write(user)
        pyautogui.press("\t")
        pyautogui.write(str(ip))
        pyautogui.press("\t")
        pyautogui.write(str(port))
        pos_add = self.while_get_pic('add.png', cnt=2, confidence=0.9, desc="instance", region=None)
        self.click_pos(pos_add, "new", 1)
        time.sleep(0.2)
        pyautogui.press("esc")

    def open(self, user,index):
        self.set_account()
        self.set_proxy()
        has, pos3 = self.sleep_while(0.5, 30, pic_file='mem.png', confidence=0.9, desc="duoren")
        if has:
            if pos3 is not None:
                self.click_pos(pos3, desc="mem", click_cnt=2)
        has, pos = self.sleep_while(0.5, 30, pic_file='xiaoxin.png', confidence=0.9, desc="xin")
        if has:
            print("get xin")

        pass

    def open_v2(self, user):
        self.set_account(user)
        has, pos3 = self.sleep_while(0.5, 30, pic_file='mem.png', confidence=0.9, desc="duoren")
        if has:
            if pos3 is not None:
                self.click_pos(pos3, desc="mem", click_cnt=2)
        has, pos = self.sleep_while(0.5, 30, pic_file='xiaoxin.png', confidence=0.9, desc="xin")
        if has:
            print("get xin")
        pass
    def register_users(self):
        index = 0
        # user_pre = "panda"
        self.read_users()
        self.close_app()
        self.open_pre()

        while True:
            if self.start_user_index >=len(self.user_list):
                return
                self.start_user_index=0
            user = self.user_list[self.start_user_index]
            # self.close_proxy()
            # user = user_pre + str(index).zfill(4)

            # self.do_proxy()

            self.open(user,self.start_user_index)
            # time.sleep(20)
            # self.login_hub()
            time.sleep(2)
            self.register()
            self.login_with_code()
            # time.sleep(1)
            self.choice_shengcun()
            # time.sleep(1)
            self.login_into_shengcun()
            # self.goto_area_2()
            self.sleep_while(0.5, 20, pic_file='fm.png', confidence=0.9, desc="instance")
            self.get_point()

            # self.goto_area_2()
            # time.sleep(20)
            # self.goto_nangua()
            # time.sleep(20)
            self.start_user_index+=1
            self.update_index()
            self.close()
        pass

    def pay_money(self):
        time.sleep(3)
        amount_list = [4096, 2048, 1024, 512, 256, 128, 64, 32, 16]
        for amount in amount_list:
            pyautogui.press("t")
            time.sleep(0.2)
            pyautogui.write("/pay zhaojiedi1992 " + str(amount) )
            pyautogui.press("enter")
            time.sleep(2)

    def update_index(self):
        with open("current_index.txt",'w') as f:
            f.writelines([str(self.start_user_index)])

    def read_users(self):
        with open("users.txt", 'r') as f:
            lines = f.readlines()
        with open("current_index.txt",'r') as f:
            lines2=f.readlines()
            self.start_user_index=int(lines2[0])

        for line in lines:
            self.user_list.append(line.strip("\n"))

    def get_point(self):
        pyautogui.press("t")
        pyautogui.write("#goto -26.377 -39 17.7")
        pyautogui.press("enter")
        time.sleep(20)
        pyautogui.press("t")
        pyautogui.write("/sethome h0")
        pyautogui.press("enter")
        # time.sleep(20)
        # pyautogui.press("enter")
        time.sleep(0.2)
        pass

    def has_tp(self):
        pix = pyautogui.pixel(3235, 897)
        if abs(pix.red - 84 ) >10:
            return False
        if abs(pix.green - 252 ) >10:
            return False
        if abs(pix.blue -252 ) >10:
            return False
        return True

    def sleep_while2(self, sleep_interval, max_sleep_seconds):
        current_sleep_seconds = 0
        while True:
            tp=self.has_tp()
            if tp:
                return True
            if current_sleep_seconds > max_sleep_seconds:
                return False
            time.sleep(sleep_interval)


if __name__ == '__main__':
    cli = ForeverMemoryClient()
    #cli.generate_users()
    #cli.register_users()
    # cli.run_v3()
    # cli.run_sealonly()
    cli.run_v4()
    # time.sleep(10)
    # has, pos =cli.sleep_while(0.5, 20, pic_file='m.png', confidence=0.9, desc="instance")
    # print(has,pos)
    # pix = pyautogui.pixel(pos.x/2, pos.y/2)
    # print(pix)
    # pix = pyautogui.pixel(pos.x, pos.y)
    # print(pix)
