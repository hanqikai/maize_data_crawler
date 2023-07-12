import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import urllib.request
import urllib
import math
import shutil

def get_browser():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')  # 设置无头模式
    chrome_options.add_argument('--ignore-certificate-errors')    # 忽略证书错误
    # 忽略 Bluetooth: bluetooth_adapter_winrt.cc:1075 Getting Default Adapter failed. 错误
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 忽略 DevTools listening on ws://127.0.0.1... 提示
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(options=chrome_options)
    return browser

def save_image_from_url(url, file_path):
    for _ in range(100):  # 下载不成功，那就重试一百次
        try:
            openhead=urllib.request.build_opener()
            openhead.addheaders = [("User-Agent", "Mozilla/5.0")]
            urllib.request.install_opener(openhead)
            urllib.request.urlretrieve(url, file_path)
            print('Image downloaded successfully.')
            return
        except:
            print('Network conditions is not good. Reloading.')
            time.sleep(5 + 5 * math.sin(_))
            continue
    print(f"{url} download failed!")

def get_content(url):
    browser = get_browser()
    browser.set_page_load_timeout(30)
    browser.implicitly_wait(30)
    browser.get(url)
    time.sleep(8)
    img_list = []
    answers = []
    question = browser.find_element(By.XPATH,'//*[@id="__layout"]/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/div').text
    ans_divs = browser.find_elements(By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div[2]/div/div[@class="asw-text"]')
    for ans in ans_divs:
        answers.append(ans.text)
    all_ans = ''.join(answers)
    img_divs = browser.find_elements(By.XPATH,'//*[@id="__layout"]/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/img')
    # 没有图片会返回空
    for img in img_divs:
        temp = img.get_attribute("src")
        if temp == "https://files.cnhnb.com/eyejs7/avatars/img-default.jpg": continue
        img_list.append(temp)
    browser.quit()
    return question, all_ans, img_list

def get_all_items(url):
    browser = get_browser()
    browser.set_page_load_timeout(160)
    browser.implicitly_wait(160)
    browser.get(url)
    time.sleep(5)
    print("已打开网页...")
    a = browser.find_element(By.XPATH,'//*[@id="__layout"]/div/div/div[2]/div/div[3]/div[2]/div[2]/span').text
    i = 1
    while a.startswith("加载下一页"):             
        try:
            browser.find_element(By.XPATH,'//*[@id="__layout"]/div/div/div[2]/div/div[3]/div[2]/div[2]/span').click()                        
            time.sleep(5)
            print(f"已经点击{i}次...")
            i += 1
        except:
            break
        a = browser.find_element(By.XPATH,'//*[@id="__layout"]/div/div/div[2]/div/div[3]/div[2]/div[2]/span').text
    url_list = []
    divs = browser.find_elements(By.XPATH, '//*[@id="__layout"]/div/div/div[2]/div/div[3]/div[2]/div[1]/div/div/div/a')
    for url in divs:
        url_list.append(url.get_attribute("href"))
    f = open("hnw_url_list.txt", mode='w', encoding='utf-8')
    for item in url_list:
        f.write(item)
        f.write("\n")
    f.close()
    browser.quit()
    return url_list

if __name__ == "__main__":
    # url_list_ = get_all_items("https://www.cnhnb.com/xt/ask/794/")
    f = open("hnw_url_list.txt", mode='r', encoding='utf-8')
    url_list = f.read().split("\n")
    f.close()
    while '' in url_list: url_list.remove('')
    # assert url_list == url_list_
    for item in range(0, len(url_list)):
        index = url_list[item].split('/')[-1].split('.')[0]
        folder = os.path.join(os.getcwd(), 'hnw', index)
        if not os.path.exists(folder) or len(os.listdir(folder)) == 0:
            if os.path.exists(folder) and len(os.listdir(folder)) == 0: shutil.rmtree(folder)
            print(f"正在处理：{url_list[item]}...，还有{len(url_list) - item - 1}条url待处理......")
            os.makedirs(folder)
            q, a, img_ = get_content(url_list[item])
            f = open(os.path.join(folder, "Q&A.json"), mode='w', encoding='utf-8')
            json.dump(obj={'url': url_list[item], 'question': q, 'answer': a, 'img_url': img_}, fp=f, ensure_ascii=False, indent=4)
            f.close()
            for i, img_url in enumerate(img_):
                save_image_from_url(img_url, f'{folder}\\{index}_{i}.jpg')
        else:
            print(f"{url_list[item]}已经被处理完成...，还有{len(url_list) - item - 1}条url待处理......")
        
    print("all_finished!")