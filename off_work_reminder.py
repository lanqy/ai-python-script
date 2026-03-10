# -*- coding: utf-8 -*-
"""
下班提醒工具
"""

import time
import datetime
from datetime import datetime as dt
import winsound
import threading


class Reminder:
    def __init__(self):
        self.running = True

    def show_reminder(self):
        """显示提醒窗口"""
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口

        # 播放提示音
        for i in range(3):
            winsound.Beep(1000, 500)
            time.sleep(0.2)

        # 显示提醒
        messagebox.showinfo(
            "下班提醒",
            "⏰ 下班时间到了！\n\n该回家啦，辛苦了一天！\n\n祝你回家愉快！"
        )

        root.destroy()

    def wait_until_time(self, target_hour, target_minute):
        """等待到指定时间"""
        while self.running:
            now = dt.now()

            # 计算目标时间
            target = dt(now.year, now.month, now.day, target_hour, target_minute)

            # 如果当前时间已经超过目标时间，设置到明天
            if now > target:
                target += datetime.timedelta(days=1)

            # 计算等待时间
            wait_seconds = (target - now).total_seconds()

            print("当前时间: %s" % now.strftime("%H:%M:%S"))
            print("提醒时间: %s" % target.strftime("%H:%M:%S"))
            print("等待时间: %.1f 分钟" % (wait_seconds / 60))
            print("按 Ctrl+C 取消提醒...\n")

            try:
                time.sleep(wait_seconds)

                # 时间到了，显示提醒
                print("\n" + "="*50)
                print("⏰ 下班时间到了！")
                print("="*50 + "\n")

                self.show_reminder()
                break

            except KeyboardInterrupt:
                print("\n提醒已取消")
                break
            except Exception as e:
                print("发生错误: %s" % str(e))
                break


def main():
    print("="*50)
    print("下班提醒工具")
    print("="*50 + "\n")

    # 设置提醒时间
    hour = 18
    minute = 30

    print("将在每天 %02d:%02d 提醒您下班\n" % (hour, minute))

    reminder = Reminder()
    reminder.wait_until_time(hour, minute)


if __name__ == "__main__":
    main()
