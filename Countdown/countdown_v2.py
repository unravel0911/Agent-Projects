import time
import sys

def get_color_code(current, total):
    """基于剩余比例返回 ANSI 颜色代码"""
    percent = (current / total) * 100
    if percent > 60:
        return "\033[92m" # 绿色
    elif percent > 30:
        return "\033[36m" # 青色/橙色效果
    elif percent > 10:
        return "\033[93m" # 黄色
    else:
        return "\033[91m" # 红色

def countdown(time_sec):
    total_sec = time_sec
    reset_code = "\033[0m"
    
    while time_sec >= 0:
        mins, secs = divmod(time_sec, 60)
        timeformat = "{:02d}:{:02d}".format(mins, secs)
        
        # 获取当前比例对应的颜色
        color = get_color_code(time_sec, total_sec)
        
        # 动态刷新输出
        sys.stdout.write(f"\rRemaining Time: {color}{timeformat}{reset_code}")
        sys.stdout.flush()
        
        time.sleep(1)
        time_sec -= 1

    # 倒计时结束
    print("\n\033[1;91mTime Up!\033[0m")
    
    # 发出声音提醒 (\a 是系统提示音 ASCII 码)
    for _ in range(3):
        sys.stdout.write('\a')
        sys.stdout.flush()
        time.sleep(0.5)

if __name__ == "__main__":
    try:
        t_input = input("Enter the time in seconds: ")
        countdown(int(t_input))
    except ValueError:
        print("Error: Please enter a valid integer.")
    except KeyboardInterrupt:
        print("\nCountdown stopped by user.")