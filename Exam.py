from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
from datetime import date
from datetime import timedelta  
from lxml import html
import time
import random
import json
import requests

class Exam():
    def __init__(self):
        self.startDate = date(2022, 3, 1)
        self.endDate = date(2022, 3, 20)
        self.indexDate = self.startDate
        
        url ='https://law.judicial.gov.tw/FJUD/Default_AD.aspx'
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"
        driver_path = "./chromedriver_99.exe"

        opt = webdriver.ChromeOptions()
        opt.add_argument('--user-agent=%s' % user_agent)
        
        self.browser = webdriver.Chrome(executable_path=driver_path, options=opt)
        self.browser.get(url)
        
        self.jsonData = []
        self.jsonDataCount = 0
    
    # 設定搜尋條件
    def setQueryConditions(self):
        # 確認 [法院] 是否選擇 [所有法院]
        courtState = self.browser.find_element(by=By.XPATH, value='//*[@id="jud_court"]/option[1]')
        if (not courtState.is_selected()):
            courtState.click()
            
        # 確認 [刑事] 是否勾選
        caseState = self.browser.find_element(by=By.XPATH, value='//*[@id="vtype_M"]/input')
        if (not caseState.is_selected()):
            caseState.click()
    
    # 輸入查詢日期 (一次查一天)
    def inputQueryDate(self):
        if (self.indexDate == None):
            self.indexDate = self.startDate
                
        self.browser.find_element(by=By.NAME, value="dy1").clear()
        self.browser.find_element(by=By.NAME, value="dy1").send_keys( str(self.indexDate.year - 1911) )
        
        self.browser.find_element(by=By.NAME, value="dm1").clear()
        self.browser.find_element(by=By.NAME, value="dm1").send_keys( str(self.indexDate.month ) )
        
        self.browser.find_element(by=By.NAME, value="dd1").clear()
        self.browser.find_element(by=By.NAME, value="dd1").send_keys( str(self.indexDate.day) )
        
        self.browser.find_element(by=By.NAME, value="dy2").clear()
        self.browser.find_element(by=By.NAME, value="dy2").send_keys( str(self.indexDate.year - 1911) )
        
        self.browser.find_element(by=By.NAME, value="dm2").clear()
        self.browser.find_element(by=By.NAME, value="dm2").send_keys( str(self.indexDate.month ) )
        
        self.browser.find_element(by=By.NAME, value="dd2").clear()
        self.browser.find_element(by=By.NAME, value="dd2").send_keys( str(self.indexDate.day) )
        
        self.indexDate += timedelta(days=1)  
    
    # 送出查詢
    def submitQuery(self):
        self.browser.find_element(by=By.ID, value="btnQry").click()
        
    #返回查詢頁面
    def backToSearch(self):
        self.browser.find_element(by=By.ID, value="fjud").click()
            
    # 抓[查詢結果]並回傳有否為空
    def checkResultIsNone(self):
        soup = bs(self.browser.page_source, 'html.parser')
        return soup.find("div", id="result-count").li.span.text == '0'
    
    # 取得[依裁判法院區分]的列表數量
    def getCourtLen(self):
        soup = bs(self.browser.page_source, 'html.parser')
        return len(soup.find("div", id="collapseGrpCourt").div.ul.find_all("li"))
    
    #點擊指定的法院區分
    def clickCourt(self, index):
        self.browser.find_element(by=By.XPATH, value= f'//*[@id="collapseGrpCourt"]/div/ul/li[{ index }]/a').click()
    
    # 將content轉換至查詢結果的iframe
    def switchToIframe(self):
        self.browser.switch_to.frame(self.browser.find_element(by=By.NAME, value='iframe-data'))
        
    # 將content轉換至預設外頁
    def swithToDefaultPage(self):
        self.browser.switch_to.default_content()
    
    # 取的檢索資料裡面的查詢結果列表
    # 一次資料20筆
    def getIframOnePageTableData(self):

        soup = bs(self.browser.page_source, 'html.parser')
        mainTable = soup.find("table", id="jud")

        dataLen = len(mainTable.find_all("tr"))

       
        for trIndex in range(1, dataLen):

            # 準備裝各案件及清空
            case = {}
            # 尋找table內的欄是否為摘要及每筆資料的第一列
            if (mainTable.find_all("tr")[trIndex].find("td", colspan="3") == None):
                #不是摘要則一欄一欄抓案號等資料
                content = mainTable.find_all("tr")[trIndex].find_all("td")


                case["title"] = content[1].text
                case["date"] = content[2].text
                case["article"] = content[3].text

                case["summary"] = mainTable.find_all("tr")[trIndex + 1].find("td", colspan="3").text

                self.jsonData.append(case)
                self.jsonDataCount += 1

            else:
                next
    
    # 確認下一頁按鈕為空
    def NextBtnIsNone(self):
        soup = bs(self.browser.page_source, 'html.parser')
        return soup.find("a", id="hlNext") is None
                        
    # 點擊下一頁查詢
    def clickIframeNextTable(self):
        self.browser.find_element(by=By.ID, value='hlNext').click()
        
    @staticmethod
    def randomSleep():
        time.sleep(round(random.uniform(0.5,2), 1))
    
    def closeBrowser(self):
        self.browser.close()
    
    def getResultFile(self):
        result = {}
        result["dateRange"] = self.startDate.strftime("%Y.%m.%d") + "-" + self.endDate.strftime("%Y.%m.%d")
        result["caseCount"] = self.jsonDataCount
        result["caseList"] = self.jsonData
        
        with open('judgementcrawler.json', 'w', encoding='utf-8') as f:
            for i in self.jsonData:
                json_str = json.dumps(i, ensure_ascii=False)
                f.write(json_str + '\n')
            #json.dumps(result, f, ensure_ascii=False, indent=4)
    
    
    def main(self):
        # 等待瀏覽器開好 (自由設定 /s)
        time.sleep(5)
        
        while (self.indexDate <= self.endDate):
            self.setQueryConditions()
            self.inputQueryDate()
            self.submitQuery()
            self.randomSleep()
            
            if (self.checkResultIsNone()):
                self.backToSearch()
                self.randomSleep()
                continue
                
            self.randomSleep()
            
            for courtIndex in range(1, self.getCourtLen() + 1):
                self.clickCourt(courtIndex)
                self.randomSleep()
                
                self.switchToIframe()
                
                while True:
                    self.getIframOnePageTableData()

                    if (self.NextBtnIsNone()):
                        self.swithToDefaultPage()
                        self.randomSleep()
                        break
                    
                    self.clickIframeNextTable()
                    self.randomSleep()
                    
            self.backToSearch()
            self.randomSleep()
        
        self.closeBrowser()
        self.getResultFile()
                
                
if __name__ == '__main__':
    Exam().main()
            
        
                
    


    