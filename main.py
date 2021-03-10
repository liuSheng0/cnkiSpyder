'''
Author = liuSheng0
Time = 2021-02-22
'''
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from lxml import etree
from time import sleep
from random import uniform
import csv
import re
import urllib.request
from ways import get_data
from math import ceil
from sys import exit



def over_one_search():
    driver.switch_to.parent_frame()
    search_win = driver.find_element_by_id('expertvalue')
    search_win.clear()
    sleep(uniform(1,2))

def pasre_page(driver):
    try:
        html = etree.HTML(driver.page_source)
        trs = html.xpath('//tr[@bgcolor]')
    except:
        print("获取html错误...结束程序...")
        return -1
    for tr in trs:
        try:
            title = tr.xpath('./td//a[@class="fz14"]/text()')[0]
            print(title)
        except:
            title = "NaN"
        try:
            authors = tr.xpath('./td[@class="author_flag"]/a[@class="KnowledgeNetLink"]//text()')
            authors = "|".join(authors)
        except:
            authors = "NaN"
        try:
            source = tr.xpath('./td//a[@target="_blank"]/text()')[1]
        except:
            source = "NaN"
        try:
            times = tr.xpath('./td[@align="center"]/text()')[0].strip()
        except:
            times = "NaN"
        try:
            database = tr.xpath('./td[@align="center"]/text()')[1].strip()
        except:
            database = "NaN"
        try:
            counted = tr.xpath('./td//span[@class="KnowledgeNetcont"]/a/text()')
            if len(counted) == 0:
                counted = 0
            else:
                counted = counted[0]
            downloadCount = tr.xpath('./td//span[@class="downloadCount"]/a/text()')
            if len(downloadCount) == 0:
                downloadCount = 0
            else:
                downloadCount = downloadCount[0]
        except:
            downloadCount = "NaN"
        try:
            downloadURL = tr.xpath('./td[@align="center"]/a[@href and @class="briefDl_D"]')[0].attrib["href"]
        except:
            downloadURL = "NaN"
        data = {
                "title":title,
                "authors":authors,
                "source":source,
                "times":times,
                "database":database,
                "counted":counted,
                "downloadCount":downloadCount,
                "downloadURL":downloadURL,
                }
        csvwriter.writerow([title,authors,source,times,database,counted,downloadCount,downloadURL])

#main 

driver_path = r"./tools/chromedriver.exe"
#隐藏窗口
option=webdriver.ChromeOptions()
option.add_argument('headless')

driver = webdriver.Chrome(executable_path=driver_path
    , chrome_options=option)

url = "https://www.cnki.net/old"
driver.get(url)

#高级检索
home_page = driver.find_element_by_id('highSearch')
home_page.click()
driver.switch_to_window(driver.window_handles[1])
#专业检索
search_page = driver.find_element_by_id('1_3')
search_page.click()
datas = []
#读取检索字段
results = get_data()
#创建csv
f = open("result.csv", "w", encoding="utf-8")
csvwriter = csv.writer(f)
csvwriter.writerow([
        "title",
        "authors",
        "source",
        "times",
        "database",
        "counted",
        "downloadCount",
        "downloadURL"
])
for result in results:
    #输入检索表达式
    search_win = driver.find_element_by_id('expertvalue')
    search_win.send_keys(result)
    #点击检索按钮
    search_btn = driver.find_element_by_id('btnSearch')
    search_btn.click()
    #转到iframe
    iframe = driver.find_element_by_id('iframeResult')
    driver.switch_to.frame(iframe)
    sleep(uniform(1,2))
    #获取检索条数及页数（20条为一页）
    try:
        html = etree.HTML(driver.page_source)
        sum_count_path = html.xpath('//div[@class="pagerTitleCell"]/text()')[0]
        print(sum_count_path)
        sum_count = int(re.search(r'[0-9]+', sum_count_path).group())
        page_count = ceil(sum_count / 20)
    except:
        print("获取条目信息错误...结束此条爬取...")
        over_one_search()
        break
    for index in range(page_count):
        #分析信息,写入csv
        pasre_page(driver)#分析信息
        #获取页数
        print("第 " + str(index+1) + " 页/共 " + str(page_count) + " 页，共 " + str(sum_count) + " 条结果")
        if(index != page_count - 1):
            #进入下一页
            try:
                next_page = driver.find_elements_by_xpath('.//div[@class="TitleLeftCell"]/a')[-1]
                next_page.click()
                sleep(uniform(8,10))
            except:
                    check_img = driver.find_elements_by_id('CheckCodeImg')[0]
                    print('正在处理验证码...')
                    locations = check_img.location
                    print(locations)
                    sizes = check_img.size
                    rangle = (int(locations['x']),int(locations['y']),int(locations['x'] + sizes['width']),int(locations['y'] + sizes['height']))
                    print(rangle)
                    js_top = "var q=document.documentElement.scrollTop=0"
                    driver.execute_script(js_top)
                    savepath = "./image/checkcode.jpg"
                    driver.save_screenshot(savepath)
                    exit(1)
                    '''
                    content = driver.page_source
                    reg_imgurl = r'img src="/kns/checkcode.aspx\?t=.*?"'
                    checkimgurl = re.findall(reg_imgurl, content)[0]
                    reg_cle01 = r'img src='
                    checkimgurl = re.sub(reg_cle01, "", checkimgurl)
                    checkimgurl = re.sub(r'"', "", checkimgurl)
                    checkimgurl = "https://kns.cnki.net" + checkimgurl
                    print(checkimgurl)
                    urllib.request.urlretrieve(checkimgurl, "./image/checkcode.jpg")
                    exit(1)            
                    except:
                    print("跳转页面失败..结束此条爬取")
                    over_one_search()
                    break
                    '''
    #下一条
    try:
        over_one_search()
    except:
        print("跳转错误...结束程序...")
        exit(1)
f.close()
print("爬取结束...")
driver.quit()
exit(0)