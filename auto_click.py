from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import time
import os

# 设置无头浏览器参数
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# 创建 Service 对象
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 日志文件路径
log_file = "click_log.txt"
log_retention_days = 2  # 保留天数

# 清理旧日志记录
def clean_old_logs():
    if not os.path.exists(log_file):
        return

    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        cleaned_lines = []
        cutoff = datetime.now() - timedelta(days=log_retention_days)

        for line in lines:
            if line.startswith("["):
                try:
                    timestamp_str = line.split("]")[0][1:]
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                    if timestamp >= cutoff:
                        cleaned_lines.append(line)
                except:
                    cleaned_lines.append(line)  # 非时间行保留
            else:
                cleaned_lines.append(line)

        with open(log_file, "w", encoding="utf-8") as f:
            f.writelines(cleaned_lines)

    except Exception as e:
        print(f"日志清理失败：{e}")

# 开始执行
clean_old_logs()

try:
    driver.get("https://app-8w4wwungk5qvcotqhlsvgr.streamlit.app/")
    time.sleep(30)  # 等待页面加载

    # 查找按钮
    buttons = driver.find_elements(By.XPATH, "//button[contains(., '启动部署')]")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if buttons:
        buttons[0].click()
        log_entry = f"[{timestamp}] 按钮已点击\n"
        print("检测到按钮，已点击。")
    else:
        log_entry = f"[{timestamp}] 未发现按钮，未执行点击\n"
        print("未检测到按钮，跳过。")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_entry)

except Exception as e:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] 错误：{str(e)}\n")
    print(f"发生错误：{e}")

finally:
    driver.quit()
