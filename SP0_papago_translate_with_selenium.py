import os
import time
import glob
import pandas as pd
import numpy as np
from selenium import webdriver
from multiprocessing import Pool


def crawler(company_list, slogan_list, startindex, endindex):
    # HTML selector 선택
    chromedriver = "./chromedriver.exe"
    # 크롬 드라이버 옵션 설정
    options = webdriver.ChromeOptions()

    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    # options.add_argument("--headless")
    options.add_argument("disable_gpu")
    options.add_argument("lang=ko_KR")

    driver = webdriver.Chrome(chromedriver, options=options)
    driver.get("https://papago.naver.com")
    driver.implicitly_wait(10)

    input_box = driver.find_element_by_css_selector("textarea#txtSource")
    button = driver.find_element_by_css_selector("button#btnTranslate")
    x_button = driver.find_element_by_class_name("btn_text_clse___1Bp8a")

    companys = []
    slogans = []

    DATA_OUT_PATH = "./translated"

    for i in range(startindex, endindex):
        try:
            input_box.clear()
            input_box.send_keys(company_list[i])
            button.click()
            time.sleep(3)
            result = driver.find_element_by_css_selector("div#txtTarget").text
            companys.append(result)
            x_button.click()
            time.sleep(2)

        except Exception as e:
            print(e)

        try:
            input_box.clear()
            input_box.send_keys(slogan_list[i])
            button.click()
            time.sleep(3)
            result = driver.find_element_by_css_selector("div#txtTarget").text
            slogans.append(result)
            x_button.click()
            time.sleep(2)

        except Exception as e:
            print(e)

    df = pd.DataFrame(companys, columns=["company"])
    df["slogan"] = slogans
    df.to_csv(
        DATA_OUT_PATH + "/" + f"company_{startindex}_{endindex}", encoding="UTF-8", index=False
    )
    driver.close()


if __name__ == "__main__":
    DATA_IN_PATH = "./datasets"
    DATA_OUT_PATH = "./translated"

    if not os.path.exists(DATA_OUT_PATH):
        os.makedirs(DATA_OUT_PATH)
        print("--- Directory creation completed successfully ---")

    else:
        print("--- Directory already exists ---")

    df = pd.read_csv(DATA_IN_PATH + "/" + "slogans.csv", encoding="UTF-8")
    df = df.dropna()
    df = df.reset_index(drop=True)

    company_list = df["company"].to_list()
    slogan_list = df["slogan"].to_list()

    processes = 14
    rows = 9516  # 불러온 파일 행 수
    rows_step = np.linspace(0, rows, processes + 1, dtype=int)

    iterable = [
        [company_list, slogan_list, rows_step[i], rows_step[i + 1]] for i in range(processes)
    ]
    pool = Pool(processes=processes)
    pool.starmap(crawler, iterable)
    pool.close()
    pool.join()
    file_list = glob.glob(DATA_OUT_PATH + "/*")
    print(len(file_list))
    if len(file_list) == processes:
        df_concat = pd.DataFrame()
        for file in file_list:
            df_temp = pd.read_csv(file)
            df_concat = pd.concat([df_concat, df_temp], ignore_index=True)
        df_concat.to_csv(DATA_IN_PATH + "/" + f"Papago_slogan.csv", encoding="UTF-8", index=False)
        print(df_concat)
    print("Done!")
