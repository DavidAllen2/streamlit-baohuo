from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import time
import os

# 日志文件路径与保留天数
log_file = "click_log.txt"
log_retention_days = 2

# 无头浏览器设置
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# 初始化 Chrome Driver（仅一次）
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 清理旧日志
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
                    cleaned_lines.append(line)
            else:
                cleaned_lines.append(line)

        with open(log_file, "w", encoding="utf-8") as f:
            f.writelines(cleaned_lines)

    except Exception as e:
        print(f"日志清理失败：{e}")

# 执行主逻辑
clean_old_logs()

try:
    driver.get("https://pingmike.streamlit.app/")

    # 等待“启动部署”按钮出现并可点击
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., '启动部署')]"))
    )

    # 查找并点击按钮
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
    error_msg = f"[{timestamp}] 错误：{str(e)}\n"
    print(f"发生错误：{e}")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(error_msg)

finally:
    driver.quit()
