# -*- coding:gbk -*-

# 引用库
from selenium import webdriver
from selenium.webdriver.common.by import By
import html
from selenium.common.exceptions import WebDriverException as WDEx

import time
from selenium.webdriver.common.action_chains import ActionChains
import cv2
import sys


##获取视频时长的方法
def get_video_duration(filename):
    cap = cv2.VideoCapture(filename)
    if cap.isOpened():
        rate = cap.get(5)  # 获取帧速率
        frame_num = cap.get(7)  # 获取视频中的帧数
        duration = frame_num / rate  # 总帧数/帧速率=视频时间
        return duration
    else:
        print("视频读取有误！")
    return -1


# 获取视频当前播放位置
# 这个地方get(cv2.CAP_PROP_POS_MSEC)无法正常返回当前帧所对应的时间，仅返回0，所以可能是cv2库的一个bug
def get_video_playsec(filename):
    cap = cv2.VideoCapture(filename)
    if cap.isOpened():
        return cap.get(cv2.CAP_PROP_POS_MSEC)
    else:
        print("视频读取有误！")
    return -1


# 命令行的进度条
def progress_Bar(playSecond, duration):
    scale = 50
    start = time.perf_counter()
    internal = int((duration - playSecond) / scale) + 1
    print("视频开始播放：")
    while True:
        dur = time.perf_counter() - start
        if dur > duration:
            break
        i = int(dur / internal)
        a = "*" * i
        b = "." * (scale - i)
        c = (i / scale) * 100
        s = "\r{:^3.0f}%[{}->{}]{:2f}s".format(c, a, b, dur)
        sys.stdout.write(s)
        sys.stdout.flush()
        time.sleep(5)
    time.sleep(3)
    return -1


# 播放观看视频的函数，传入参数为需要点击的对应按钮
def watchVideo(em):
    try:
        em[0].click()

        while True:
            # 寻找是否存在video控件用于判断是否存在视频，且需判断是否完成
            driver.switch_to.frame("iframe")  # 转入窗体中间部分对应的iframe
            state = driver.find_element(By.XPATH, '/html/body/div/div/p[1]/div')  # 获取是否完成的状态
            flag = 0  # 用于判断视频是否需要进行播放的标志

            # 判断该小节是否已经完成，未完成则flag置为1
            if state.get_attribute('class') != 'ans-attach-ct ans-job-finished':
                flag = 1
            else:
                break

            driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))  # 转入到深层iframe，这里面对应到的iframe有两层
            video = driver.find_elements(By.TAG_NAME, "video")  # 获取video控件

            # 如果页面上存在视频，则flag继续为1，否则为0
            if len(video) > 0:
                flag = 1 * flag
            else:
                flag = 0 * flag
                break

            # 只有在flag==1的情况下，视频才需要被播放
            if flag == 1:
                video = video[0]
                src = video.get_attribute('src')

                ActionChains(driver).move_to_element(video).click().perform()  # 点击开启视频
                t = get_video_duration(src)  # 获取视频时间
                t0 = get_video_playsec(src)  # 获取当前播放的时间
                progress_Bar(t0, t)  # 停止等待视频播放完成

            # 听完视频/视频已完成，则进入下一部分
            driver.switch_to.window(driver.window_handles[-1])
            driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div[4]").click()

        driver.switch_to.window(driver.window_handles[-1])
        driver.find_element(By.XPATH, "/html/body/div[3]/div/div[1]/a").click()  # 没有视频则返回选课界面
    except:
        driver.switch_to.window(driver.window_handles[-1])
        driver.find_element(By.XPATH, "/html/body/div[3]/div/div[1]/a").click()  # 没有视频则返回选课界面
        print('播放完一小节视频.....')
    return -1


###进入到刷安全知识的页面并实现登录功能
##全局变量区域
# 刷课网站
url = html.unescape("http://www.mooc.whu.edu.cn/portal")

# 账号密码
account = "2022302141118"
psd = "Dhs200404023015"

# 打开网页，并全屏，使用的是微软Edge浏览器
driver = webdriver.Edge()
driver.get(url)
driver.maximize_window()

# 尝试登录
try:
    a = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/input')
    a.click()
    # WebDriverWait(driver,10).until(EC.presence_of_all_elements_located())
    # driver.find_element(By.XPATH,'/html/body/div[3]/div/div[2]/div/a').click()
    # print('点击登录按钮成功')

    # 输入账号密码，进行登录
    driver.find_element(By.XPATH, '/html/body/div/div[2]/div[3]/div[2]/div[5]/div[2]/form/div[1]/input').send_keys(
        account)
    text = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[3]/div[2]/div[5]/div[2]/form/div[2]/input[1]')
    text.send_keys(psd)

    btn = driver.find_element(By.XPATH, '//*[@id="casLoginForm"]/p[2]/button')
    ActionChains(driver).move_to_element(btn).click().perform()

except WDEx as driver_error:
    print("登录失败，请检个人账号和密码是否正确，或网络是否正常")
    pass

# 登录进入课程界面
try:
    # 切换进frame页
    time.sleep(5)
    driver.find_element(By.XPATH,'//html/body/div[1]/div[2]/div[1]/div[3]/div/div[3]/div/div[1]/div/div/div[1]/p').click()

    time.sleep(1)
    lessons = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div/div[2]/div[2]/ul').find_elements(
        By.XPATH, "//li[@class = 'course clearfix']")
    lessons[0].click()
except WDEx as error:
    print(error)

# 切换到最新生成的window窗体，开始进行刷课
try:
    driver.switch_to.window(driver.window_handles[-1])

    # 找到第一个黄色的，也即未完成的课程
    sections_todo = driver.find_elements(By.XPATH, "//em[@class='orange']")
    sections_loc = []
    for section in sections_todo:
        sections_loc.append(section.location)

    for loc in sections_loc:
        sections_todo = driver.find_elements(By.XPATH, "//em[@class='orange']")
        watchVideo([section for section in sections_todo if section.location == loc])

    print('视频已经刷完，请自行完成题目')
except WDEx as error:
    print(error)