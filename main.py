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
        self.nongzuowei="nangua"
        #self.nongzuowei = "xrz"

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
        for i in range(1, cnt):
            if i == 1:
                self.log(
                    "start find {},desc={},pic_file={},cnt={},confidence={}".format(i, desc, pic_file, cnt,
                                                                                    confidence))
            else:
                self.log("retry find desc={},pic_file={},cnt={},current_cnt={},confidence={}".format(
                    desc,pic_file, cnt, i, confidence))
            if region is None:
                pos = pyautogui.locateCenterOnScreen(pic_file, confidence=confidence, region=region)
            else:
                pos = pyautogui.locateCenterOnScreen(pic_file, confidence=confidence)
            if pos is not None:
                self.log("get desc={},pic_file={},cnt={},current_cnt={},confidence={}".format(
                    desc, pic_file, cnt, i, confidence))
                return pos

            time.sleep(0.92)
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

    def run(self):
        # record start info
        start_message = "start,with first_start_delay={}".format(self.first_start_delay)
        print(start_message)
        self.log(start_message)
        # time.sleep(self.first_start_delay)

        self.print_size()
        # self.test_move()
        # self.prepare_works()
        while True:
            try:
                hour = time.localtime().tm_hour
                if hour != self.hour:
                    self.hour = hour
                    self.prepare_works()

                self.run_one_v2()
            except Exception as err:
                self.log("error={}".format(err))


    def run_one_v2(self):
        self.goto_home()
        self.open_xrz()
        if self.can_seal():
            self.seal()
        self.goto_xrz()
        time.sleep(self.seal_interval)

    def run_sealonly(self):
        while True:
            self.seal()
            time.sleep(self.seal_interval)
    def run_v3(self):
        # record start info
        start_message = "start,with first_start_delay={}".format(self.first_start_delay)
        print(start_message)
        self.log(start_message)
        # time.sleep(self.first_start_delay)

        self.print_size()
        # self.test_move()
        self.prepare_works()
        while True:
            try:
                # hour = time.localtime().tm_hour
                # if hour != self.hour:
                pos = self.while_get_pic("nongzuowu.png", 5, 0.6, "nongzuowu",region=None)
                #break
                if pos is None:
                    # self.hour = hour
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
            #pyautogui.press('esc')

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
        time.sleep(20)
        # self.login_hub()
        # time.sleep(2)
        self.login_with_code()
        time.sleep(1)
        self.choice_shengcun()
        time.sleep(1)
        self.login_into_shengcun()
        time.sleep(30)
        if self.nongzuowei == "nangua":
            self.goto_nangua()
            time.sleep(10)
            self.open_nangua()
            time.sleep(1)
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

    def login_with_code(self):
        pyautogui.write('/login  ' + self.code, interval=self.default_input_interval)
        self.screenshot("login_with_code01")
        pyautogui.press('enter')
        self.screenshot("login_with_code02")
        time.sleep(0.5)

    def choice_shengcun(self):
        self.log("start choice shengcun")
        self.screenshot("choice_shengcun01")
        pyautogui.write("/bs bc", interval=self.default_input_interval)
        pyautogui.press('enter')

    # choice shengcun server , and goto
    def login_into_shengcun(self):
        #pyautogui.click(button='right')
        # ime.sleep(0.3)
        pos = self.while_get_pic('shengcun.png', cnt=5, confidence=0.85, desc="shengcun-server", region=None)

        self.screenshot("login_into_shengcun")
        self.click_pos(pos, "shengcun-server", 2)
        # time.sleep(10)
        # pyautogui.press('\t', 'enter')
        time.sleep(1)
        #pyautogui.hotkey("")

    # # goto anniu kaiguan
    # def goto_home(self):
    #     pyautogui.write('/home home', interval=self.default_input_interval)
    #     self.screenshot("goto_home")
    #     pyautogui.press('enter')
    #     self.screenshot("goto_home")
    #     time.sleep(5)

    def goto_xrz(self):

        pyautogui.write('/home h2', interval=self.default_input_interval)
        self.screenshot("goto_xrz01")
        pyautogui.press('enter')
        self.screenshot("goto_xrz02")

    def goto_nangua(self):
        pyautogui.write('/home h3', interval=self.default_input_interval)
        self.screenshot("goto_nangua")
        pyautogui.press('enter')
        self.screenshot("goto_nangua")

    # open xrz page
    def open_xrz(self):
        pyautogui.write('/bs sg200', interval=self.default_input_interval)
        pyautogui.press('enter')
        pyautogui.moveTo(100, 100)
        time.sleep(0.3)
        pos = self.while_get_pic('xrz.png', cnt=2, confidence=0.82, desc="xrz-seal-button", region=(2000/2, 800/2, 2500/2, 1100/2))
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

    def run2(self):
        # record start info
        start_message = "start,with first_start_delay={}".format(self.first_start_delay)
        print(start_message)
        self.log(start_message)
        time.sleep(self.first_start_delay)

        self.print_size()
        self.test_move()
        #self.prepare_works()
        while True:
            try:
                self.seal()
                time.sleep(self.seal_interval)
            except Exception as err:
                self.log("error={}".format(err))

    def close(self):
        cmd1=""" ps aux |grep MultiMC.app |grep -v grep  |grep MultiMC.app |awk '{print $2}' |while read pid ; do kill -9 $pid  ; done """
        os.system(cmd1)
        time.sleep(2)

        pass

    def open(self):
        os.system("open /Applications/MultiMC.app")
        time.sleep(5)
        pos = self.while_get_pic('instance.png', cnt=2, confidence=0.9, desc="instance",region=(0,0,800,800))
        self.click_pos(pos, "open goad instance", 1)
        time.sleep(0.2)
        pos = self.while_get_pic('run.png', cnt=2, confidence=0.9, desc="run", region=None)
        self.click_pos(pos, "run", 1)

        while True:
            pos1 = self.while_get_pic('lixianbtn.png', cnt=2, confidence=0.9, desc="lixianbtn", region=None)
            if pos1 is not None:
                pyautogui.press("enter")
                time.sleep(1)
            pos2 = self.while_get_pic('duoren.png', cnt=2, confidence=0.9, desc="duoren", region=None)
            if pos2 is not None:
                self.click_pos(pos2, desc="mem", click_cnt=2)
                time.sleep(1)
            pos3 = self.while_get_pic('mem.png', cnt=2, confidence=0.9, desc="duoren", region=None)
            if pos3 is not None:
                self.click_pos(pos3,desc="mem",click_cnt=2)
                time.sleep(1)

            pos = self.while_get_pic('xin.png', cnt=2, confidence=0.9, desc="duoren", region=None)
            if pos is not None:
                print("get xin")
                break
            time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'command', 'f')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'command', '/')
        time.sleep(1)
        pass


if __name__ == '__main__':
    cli = ForeverMemoryClient()
    cli.run_v3()
    #cli.run_sealonly()
