from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time

MAX_PAGES = 20
MAX_TITLES = 1000

TARGET_CATEGORIES_MAP = {
    "IT·정보통신업": "10007",
    "미디어·광고업": "10005",
    "금융·은행업": "10002",
    "건설업": "10003",
    "문화·예술·디자인업": "10006"
}

def js_click(wd, element):
    wd.execute_script("arguments[0].click();", element)

def load_titles_from_page(wd):
    soup = BeautifulSoup(wd.page_source, "html.parser")
    results = []

    rows = soup.select("tr.post-td:not(:has(div.skeleton))")

    for row in rows:
        tds = row.find_all("td", recursive=False)
        if len(tds) < 2:
            continue

        title_div = tds[1].select_one("div")
        if not title_div:
            continue

        text = title_div.get_text(" ", strip=True)
        results.append(text)

    return results


def click_next_page(wd):
    spans = wd.find_elements(By.CSS_SELECTOR, "div.pager-wrap span")
    for span in spans:
        if span.text.strip() == ">":
            js_click(wd, span)
            return True
    return False

def open_jobkorea_tab(wd):
    tabs = wd.find_elements(By.CSS_SELECTOR, "ul.tab-button-wrap li")
    for tab in tabs:
        if "잡코리아" in tab.text:
            js_click(wd, tab)
            time.sleep(2)
            return

def open_category_dropdown(wd):
    opens = wd.find_elements(
        By.CSS_SELECTOR,
        "div.dropdown-content-wrap.isOpen"
    )
    if opens:
        return

    dropdowns = wd.find_elements(By.CSS_SELECTOR, "div.dropdown-btn-wrap")

    for dropdown in dropdowns:
        try:
            span = dropdown.find_element(By.TAG_NAME, "span")
            if span.text.strip() == "희망업종":
                wd.execute_script("arguments[0].click();", dropdown)
                time.sleep(1)
                return
        except:
            continue

    raise Exception("희망업종 dropdown을 찾지 못했습니다.")

def select_category(wd, category_name):
    target_value = TARGET_CATEGORIES_MAP[category_name]

    inputs = wd.find_elements(
        By.CSS_SELECTOR,
        "div.dropdown-content-wrap.isOpen input[type='checkbox']"
    )

    for inp in inputs:
        if inp.get_attribute("value") == target_value:
            wd.execute_script("arguments[0].click();", inp)
            time.sleep(2)
            return True

    return False

def reset_filter(wd):
    tags = wd.find_elements(
        By.CSS_SELECTOR,
        "div.search-bar-bottom-tag-list-wrap div.tag"
    )

    for tag in tags:
        try:
            close_btn = tag.find_element(By.CSS_SELECTOR, "span")
            wd.execute_script("arguments[0].click();", close_btn)
            time.sleep(0.5)
        except:
            continue

    time.sleep(1)

def crawl():
    wd = webdriver.Chrome()
    wd.get("https://job.skuniv.ac.kr/recruit-external/")
    time.sleep(2)

    open_jobkorea_tab(wd)

    all_titles = []

    for category in TARGET_CATEGORIES_MAP:
        print(f"[업종] {category} 시작")

        open_category_dropdown(wd)
        if not select_category(wd, category):
            print(f"{category} 선택 실패")
            continue

        page = 1
        while page <= MAX_PAGES:
            print(f"- {page} 페이지 수집 중")

            titles = load_titles_from_page(wd)
            all_titles.extend(titles)

            if len(all_titles) >= MAX_TITLES:
                wd.quit()
                return all_titles[:MAX_TITLES]

            if not click_next_page(wd):
                break

            time.sleep(1)
            page += 1

        reset_filter(wd)

    wd.quit()
    return all_titles

titles = crawl()
df = pd.DataFrame({"title": titles})
df.to_csv("../recruitment_info_analysis/jobkorea_recruitment_titles.csv", index=False, encoding="utf-8-sig")

print(f"총 수집 개수: {len(df)}")
print("jobkorea_recruitment_titles.csv 저장 완료")