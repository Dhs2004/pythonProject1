import pandas as pd
import numpy as np
from uiautomation import WindowControl, MenuControl
wx = WindowControl(Name='微信')
print(wx)
wx.SwitchToThisWindow()
hw = wx.ListControl(Name='会话')
print('寻找会话绑定', hw)
df = pd.read_csv('data.csv', encoding='gb18030')
while True:
    we = hw.TextControl(searchDepth=4)
    while not we.Exists(0):
        pass
    print('查找未读消息', we)
    if we.Name:
        we.Click(simulateMove=False)
        last_msg = wx.ListControl(Name='消息').GetChildren()[-1].Name
        print('读取最后一条消息', last_msg)
        msg = df.apply(lambda x: x['回复内容'] if x['关键词'] in last_msg else None, axis=1)
        msg.dropna(axis=0, how='any', inplace=True)
        ar = np.array(msg).tolist()
        if ar:
            wx.SendKeys(ar[0].replace('{br}', '{Shift}{Enter}'), waitTime=0)
            wx.SendKeys('{Enter}', waitTime=0)
            wx.TextControl(SubName=ar[0][:5]).RightClick()
        else:
            wx.SendKeys('我没有理解你的意思', waitTime=0)
            wx.SendKeys('{Enter}', waitTime=0)
            wx.TextControl(SubName=last_msg[:5]).RightClick()



