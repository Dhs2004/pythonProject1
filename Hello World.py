# -*- coding:gbk -*-

# ���ÿ�
from selenium import webdriver
from selenium.webdriver.common.by import By
import html
from selenium.common.exceptions import WebDriverException as WDEx

import time
from selenium.webdriver.common.action_chains import ActionChains
import cv2
import sys


##��ȡ��Ƶʱ���ķ���
def get_video_duration(filename):
    cap = cv2.VideoCapture(filename)
    if cap.isOpened():
        rate = cap.get(5)  # ��ȡ֡����
        frame_num = cap.get(7)  # ��ȡ��Ƶ�е�֡��
        duration = frame_num / rate  # ��֡��/֡����=��Ƶʱ��
        return duration
    else:
        print("��Ƶ��ȡ����")
    return -1


# ��ȡ��Ƶ��ǰ����λ��
# ����ط�get(cv2.CAP_PROP_POS_MSEC)�޷��������ص�ǰ֡����Ӧ��ʱ�䣬������0�����Կ�����cv2���һ��bug
def get_video_playsec(filename):
    cap = cv2.VideoCapture(filename)
    if cap.isOpened():
        return cap.get(cv2.CAP_PROP_POS_MSEC)
    else:
        print("��Ƶ��ȡ����")
    return -1


# �����еĽ�����
def progress_Bar(playSecond, duration):
    scale = 50
    start = time.perf_counter()
    internal = int((duration - playSecond) / scale) + 1
    print("��Ƶ��ʼ���ţ�")
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


# ���Źۿ���Ƶ�ĺ������������Ϊ��Ҫ����Ķ�Ӧ��ť
def watchVideo(em):
    try:
        em[0].click()

        while True:
            # Ѱ���Ƿ����video�ؼ������ж��Ƿ������Ƶ�������ж��Ƿ����
            driver.switch_to.frame("iframe")  # ת�봰���м䲿�ֶ�Ӧ��iframe
            state = driver.find_element(By.XPATH, '/html/body/div/div/p[1]/div')  # ��ȡ�Ƿ���ɵ�״̬
            flag = 0  # �����ж���Ƶ�Ƿ���Ҫ���в��ŵı�־

            # �жϸ�С���Ƿ��Ѿ���ɣ�δ�����flag��Ϊ1
            if state.get_attribute('class') != 'ans-attach-ct ans-job-finished':
                flag = 1
            else:
                break

            driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))  # ת�뵽���iframe���������Ӧ����iframe������
            video = driver.find_elements(By.TAG_NAME, "video")  # ��ȡvideo�ؼ�

            # ���ҳ���ϴ�����Ƶ����flag����Ϊ1������Ϊ0
            if len(video) > 0:
                flag = 1 * flag
            else:
                flag = 0 * flag
                break

            # ֻ����flag==1������£���Ƶ����Ҫ������
            if flag == 1:
                video = video[0]
                src = video.get_attribute('src')

                ActionChains(driver).move_to_element(video).click().perform()  # ���������Ƶ
                t = get_video_duration(src)  # ��ȡ��Ƶʱ��
                t0 = get_video_playsec(src)  # ��ȡ��ǰ���ŵ�ʱ��
                progress_Bar(t0, t)  # ֹͣ�ȴ���Ƶ�������

            # ������Ƶ/��Ƶ����ɣ��������һ����
            driver.switch_to.window(driver.window_handles[-1])
            driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div[4]").click()

        driver.switch_to.window(driver.window_handles[-1])
        driver.find_element(By.XPATH, "/html/body/div[3]/div/div[1]/a").click()  # û����Ƶ�򷵻�ѡ�ν���
    except:
        driver.switch_to.window(driver.window_handles[-1])
        driver.find_element(By.XPATH, "/html/body/div[3]/div/div[1]/a").click()  # û����Ƶ�򷵻�ѡ�ν���
        print('������һС����Ƶ.....')
    return -1


###���뵽ˢ��ȫ֪ʶ��ҳ�沢ʵ�ֵ�¼����
##ȫ�ֱ�������
# ˢ����վ
url = html.unescape("http://www.mooc.whu.edu.cn/portal")

# �˺�����
account = "2022302141118"
psd = "Dhs200404023015"

# ����ҳ����ȫ����ʹ�õ���΢��Edge�����
driver = webdriver.Edge()
driver.get(url)
driver.maximize_window()

# ���Ե�¼
try:
    a = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/input')
    a.click()
    # WebDriverWait(driver,10).until(EC.presence_of_all_elements_located())
    # driver.find_element(By.XPATH,'/html/body/div[3]/div/div[2]/div/a').click()
    # print('�����¼��ť�ɹ�')

    # �����˺����룬���е�¼
    driver.find_element(By.XPATH, '/html/body/div/div[2]/div[3]/div[2]/div[5]/div[2]/form/div[1]/input').send_keys(
        account)
    text = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[3]/div[2]/div[5]/div[2]/form/div[2]/input[1]')
    text.send_keys(psd)

    btn = driver.find_element(By.XPATH, '//*[@id="casLoginForm"]/p[2]/button')
    ActionChains(driver).move_to_element(btn).click().perform()

except WDEx as driver_error:
    print("��¼ʧ�ܣ��������˺ź������Ƿ���ȷ���������Ƿ�����")
    pass

# ��¼����γ̽���
try:
    # �л���frameҳ
    time.sleep(5)
    driver.find_element(By.XPATH,'//html/body/div[1]/div[2]/div[1]/div[3]/div/div[3]/div/div[1]/div/div/div[1]/p').click()

    time.sleep(1)
    lessons = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div/div[2]/div[2]/ul').find_elements(
        By.XPATH, "//li[@class = 'course clearfix']")
    lessons[0].click()
except WDEx as error:
    print(error)

# �л����������ɵ�window���壬��ʼ����ˢ��
try:
    driver.switch_to.window(driver.window_handles[-1])

    # �ҵ���һ����ɫ�ģ�Ҳ��δ��ɵĿγ�
    sections_todo = driver.find_elements(By.XPATH, "//em[@class='orange']")
    sections_loc = []
    for section in sections_todo:
        sections_loc.append(section.location)

    for loc in sections_loc:
        sections_todo = driver.find_elements(By.XPATH, "//em[@class='orange']")
        watchVideo([section for section in sections_todo if section.location == loc])

    print('��Ƶ�Ѿ�ˢ�꣬�����������Ŀ')
except WDEx as error:
    print(error)