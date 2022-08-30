import datetime
import os
import sys
import time

import pyautogui


class ForeverMemoryClient:

    def __init__(self):
        self.pic_cnt = 0
        self.log_file = "logs/out.log"
        self.code = "142857"
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

    def run_sealonly(self):
        while True:
            self.seal()
            time.sleep(self.seal_interval)

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
        self.seal_cnt += 1
        self.log("start seal {}".format(self.seal_cnt))
        pyautogui.keyDown('shift')
        pyautogui.click()
        pyautogui.keyUp('shift')
        self.log("end seal {}".format(self.seal_cnt))
        # pyautogui.press('esc')

    def can_seal(self):
        return True
        pos = self.while_get_pic("nongzuowu.png", 2, 0.90, "nongzuowu")
        return pos is not None

    def login_hub(self):
        self.log("start login  hub")
        pyautogui.write("/hub", interval=self.default_input_interval)
        pyautogui.press('enter')

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
        elif self.nongzuowei == "xrz":
            self.goto_xrz()
            time.sleep(10)
            self.open_xrz()
            time.sleep(1)

    def print_size(self):
        screenWidth, screenHeight = pyautogui.size()
        self.log("windows size={},{}".format(screenWidth, screenHeight))
        currentMouseX, currentMouseY = pyautogui.position()
        self.log("mouse size={},{}".format(currentMouseX, currentMouseY))

    def test_move(self):
        pyautogui.moveTo(500, 500, duration=2)
        time.sleep(1)
        pyautogui.moveTo(800, 500, duration=2)
        time.sleep(1)
        return

    def screenshot(self, filename):
        # pyautogui.screenshot("pics/{}_{}_{}.png".format(self.run_cnt, self.pic_cnt, filename))
        self.screenshot_cnt += 1

    def register(self):
        pyautogui.write('/register  ' + self.code + " " + self.code, self.default_input_interval)
        pyautogui.press('enter')

    def login_with_code(self):
        pyautogui.write('/login  ' + self.code, interval=self.default_input_interval)
        self.screenshot("login_with_code01")
        pyautogui.press('enter')
        self.screenshot("login_with_code02")
        time.sleep(0.2)

    def choice_shengcun(self):
        self.log("start choice shengcun")
        self.screenshot("choice_shengcun01")
        pyautogui.write("/bs bc", interval=self.default_input_interval)
        pyautogui.press('enter')

    def login_into_shengcun(self):
        pos = self.while_get_pic('shengcun.png', cnt=5, confidence=0.85, desc="shengcun-server", region=None)
        self.screenshot("login_into_shengcun")
        self.click_pos(pos, "shengcun-server", 2)
        time.sleep(0.2)

    def goto_area_0(self):
        pyautogui.write('/bs', interval=self.default_input_interval)
        pyautogui.press('enter')
        pos = self.while_get_pic('zhucheng.png', cnt=2, confidence=0.82, desc="zhucheng",region=None)
        self.click_pos(pos, "zhucheng", 1)
        time.sleep(0.2)

    def goto_area_2(self):
        pyautogui.write('/bs', interval=self.default_input_interval)
        pyautogui.press('enter')
        pos = self.while_get_pic('erqu.png', cnt=2, confidence=0.82, desc="xrz-seal-button",region=None)
        self.click_pos(pos, "first-seal-xrz", 1)
        time.sleep(0.2)

    def goto_xrz(self):

        pyautogui.write('/home h2', interval=self.default_input_interval)
        self.screenshot("goto_xrz01")
        pyautogui.press('enter')
        self.screenshot("goto_xrz02")

    def goto_nangua(self):
        pyautogui.write('/res tp panda_nangua.gj', interval=self.default_input_interval)
        self.screenshot("goto_nangua")
        pyautogui.press('enter')
        self.screenshot("goto_nangua")

    # open xrz page
    def open_xrz(self):
        pyautogui.write('/bs sg200', interval=self.default_input_interval)
        pyautogui.press('enter')
        pyautogui.moveTo(100, 100)
        time.sleep(0.3)
        pos = self.while_get_pic('xrz.png', cnt=2, confidence=0.82, desc="xrz-seal-button",
                                 region=(2000 / 2, 800 / 2, 2500 / 2, 1100 / 2))
        self.screenshot("open_xrz01")
        self.click_pos(pos, "first-seal-xrz", 1)
        self.screenshot("open_xrz02")
        self.log("pos={}".format(pos))
        time.sleep(0.3)

    def open_nangua(self):
        pyautogui.write('/bs sg200', interval=self.default_input_interval)
        pyautogui.press('enter')
        pyautogui.moveTo(100, 100)
        time.sleep(0.3)

        pos = self.while_get_pic('nangua.png', cnt=2, confidence=0.82, desc="nangua-seal-button", region=None)
        self.screenshot("nangua")
        self.click_pos(pos, "first-seal-nangua", 1)
        self.screenshot("nangua")
        self.log("pos={}".format(pos))
        time.sleep(0.3)


    def close(self):
        cmd1 = """ ps aux |grep MultiMC.app |grep -v grep  |grep MultiMC.app |awk '{print $2}' |while read pid ; do kill -9 $pid  ; done """
        os.system(cmd1)
        time.sleep(0.5)
        pass

    def sleep_while(self, sleep_interval, max_sleep_seconds, pic_file, desc, confidence):
        current_sleep_seconds = 0
        while True:
            pos = self.while_get_pic(pic_file, cnt=1, confidence=confidence, desc=desc, region=None)
            if pos is not None:
                return True,pos
            if current_sleep_seconds > max_sleep_seconds:
                return False,None
            time.sleep(sleep_interval)

    def open(self,user):
        os.system("open /Applications/MultiMC.app")
        self.sleep_while(0.5, 20, pic_file='instance.png',  confidence=0.9, desc="instance")
        pos = self.while_get_pic('instance.png', cnt=2, confidence=0.9, desc="instance", region=(0, 0, 800, 800))
        self.click_pos(pos, "open goad instance", 1)
        time.sleep(0.2)
        pos = self.while_get_pic('lixianqidong.png', cnt=2, confidence=0.9, desc="run", region=None)
        self.click_pos(pos, "run", 1)

        max_cnt=60
        cnt=0
        while cnt <max_cnt:
            pos1 = self.while_get_pic('lixianbtn.png', cnt=1, confidence=0.9, desc="lixianbtn", region=None)
            if pos1 is not None:
                pyautogui.write(user)
                pyautogui.press("enter")
                time.sleep(1)
            pos2 = self.while_get_pic('duoren.png', cnt=1, confidence=0.9, desc="duoren", region=None)
            if pos2 is not None:
                self.click_pos(pos2, desc="mem", click_cnt=2)
                break
            time.sleep(0.3)
            cnt+=1

        has,pos3=self.sleep_while(0.5, 30, pic_file='mem.png', confidence=0.9, desc="duoren")
        if has:
        # pos3 = self.while_get_pic('mem.png', cnt=1, confidence=0.9, desc="duoren", region=None)
            if pos3 is not None:
                self.click_pos(pos3, desc="mem", click_cnt=2)

        has ,pos=self.sleep_while(0.5, 30, pic_file='wanjiaxitong.png', confidence=0.9, desc="xin")
        if has:
            # pos = self.while_get_pic('wanjiaxitong.png', cnt=1, confidence=0.9, desc="xin", region=None)
            # if pos is not None:
            print("get xin")

        pyautogui.hotkey('ctrl', 'command', 'f')
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'command', '/')
        time.sleep(0.2)
        pass

    def register_users(self):
        index = 0
        user_pre="panda"
        for index in range (1,100):
            user= user_pre+str(index).zfill(4)
            self.close()
            self.open(user)
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
            time.sleep(20)
            self.goto_area_2()
            time.sleep(20)
        pass


if __name__ == '__main__':
    cli = ForeverMemoryClient()
    cli.register_users()
    #cli.run_v3()
    # cli.run_sealonly()
