from tqdm import tqdm
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import TimeoutException 
from tqdm import tqdm
import urllib.request
import urllib
import math


def get_browser():
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--ignore-certificate-errors')    # 忽略证书错误
    # 忽略 Bluetooth: bluetooth_adapter_winrt.cc:1075 Getting Default Adapter failed. 错误
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 忽略 DevTools listening on ws://127.0.0.1... 提示
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(options=chrome_options)
    return browser

def save_image_from_url(url, file_path):
    for _ in range(10):  # 下载不成功，那就重试一百次
        try:
            openhead=urllib.request.build_opener()
            openhead.addheaders = [("User-Agent", "Mozilla/5.0")]
            urllib.request.install_opener(openhead)
            urllib.request.urlretrieve(url, file_path)
            print('Image downloaded successfully.')
            return
        except:
            print('Network conditions is not good. Reloading.')
            time.sleep(5 + 3 * math.sin(_))
            continue
    print(f"{url} download failed!")

def get_content(url):
    browser = get_browser()
    browser.set_page_load_timeout(30)
    browser.implicitly_wait(30)
    try:
        browser.get(url)
    except TimeoutException:
        print(f"Page---{url}--- load timed out but we keep going!")
        pass
    time.sleep(4)
    question = browser.find_element(By.XPATH, '//*[@id="index_ques"]/h6').text
    img_list = []
    try:
        img_elements = browser.find_elements(By.XPATH, '//*[@id="index_ques"]/ul/li/a/img')
        for img in img_elements:
            src = img.get_attribute('src')
            src = src.replace("small/", '')
            img_list.append(src)
    except:
        print(f"这条url：{url}没有图片")
        pass
    people_info = browser.find_element(By.XPATH, '//*[@id="index_ques"]/p/span[1]/b').text
    time_ = browser.find_element(By.XPATH, '//*[@id="index_ques"]/p/span[3]').text
    loc = browser.find_element(By.XPATH, '//*[@id="index_ques"]/p/span[2]').text
    info = {"people": people_info, "time": time_, "location": loc}
    all_ans = []
    answers = browser.find_elements(By.XPATH, '//*[@id="index_replys"]/div/div[1]/p')
    for ans in answers:
        all_ans.append(ans.text)
    browser.quit()
    return question, all_ans, img_list.copy(), info

def get_all_items(key_words):
    try:
        f = open(f"njtg_url_list_{key_words}.txt", mode='r', encoding='utf-8')
        url_list = f.read().split("\n")

        f.close()
        while '' in url_list: url_list.remove('')
        g = open(f"have_process_{key_words}.txt", mode='r', encoding='utf-8')
        have_process = g.read().split("\n")

        g.close()

        while '' in have_process: have_process.remove('')
        url_list_after_sort = sorted(set(url_list), key=url_list.index)  # 保序去重
        for item in have_process: url_list_after_sort.remove(item)
        print("sorted finished...")
        for i in tqdm(range(len(url_list_after_sort))):
            cur_url = url_list_after_sort[i]
            index = cur_url.split("=")[-1]
            print(f"\n正在读取url：{cur_url}...")
            question, all_ans, img_list, info = get_content(cur_url)
            obj = {'url': cur_url, 'question': question, 'img_url': img_list, "info": info, 'answer': all_ans}
            if img_list != 0:
                folder = os.path.join(os.getcwd(), f'njtg_{key_words}', index)
                if not os.path.exists(folder): os.makedirs(folder)
                h = open(os.path.join(folder, "Q&A.json"), mode='w', encoding='utf-8')
                json.dump(obj, fp=h, ensure_ascii=False, indent=4)
                h.close()
                for j, img_url in enumerate(img_list):
                    save_image_from_url(img_url, f'{folder}\\{index}_{j}.jpg')
            g = open(f"have_process_{key_words}.txt", mode='a+', encoding='utf-8')
            g.write(cur_url + '\n')
            g.close()
    except:
        print("出错了...")
        return


if __name__ == "__main__":
    key_words = "玉米病害"
    for _ in range(1000):  # 因为网络原因总是停止运行，那么我们就利用循环自动重启
        get_all_items(key_words)