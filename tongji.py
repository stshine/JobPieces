# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
import unittest, time, re
import io, time, sys

replaceRegx = re.compile("       *")
jstring = ""
with io.open('TongjiEnhance.user.js', encoding='utf-8') as f:
   jstring = f.read()


class Tongji(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://tongji.1958.cc:8106/"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.source = ""
    
    def test_tongji(self):
        driver = self.driver
        driver.get(self.base_url + "/Projects/ProjectsList.aspx")
        driver.find_element_by_id("yhm_I").clear()
        driver.find_element_by_id("yhm_I").send_keys("shenhe1")
        driver.find_element_by_id("pwd_I").clear()
        driver.find_element_by_id("pwd_I").send_keys("123456")
        driver.find_element_by_css_selector("span").click()
        # driver.find_element_by_name("btn1").click()
        wait = WebDriverWait(driver, 30)
        driver.find_element_by_id("ASPxPageControl1_ASPxDateEdit1_B-1Img").click()
        wait.until(EC.visibility_of_element_located((By.ID, "ASPxPageControl1_ASPxDateEdit1_DDD_PW-1")))
        driver.find_element_by_id("ASPxPageControl1_ASPxDateEdit1_DDD_C_PMCImg").click()
        driver.find_element_by_id("ASPxPageControl1_ASPxDateEdit1_DDD_C_PMCImg").click()
        # driver.find_element_by_id("ASPxPageControl1_ASPxDateEdit1_DDD_C_T").click()
        # wait.until(EC.visibility_of_element_located((By.ID, "ASPxPageControl1_ASPxDateEdit1_DDD_C_FNP_PW-1")))
        # selector = Select(driver.find_element_by_id("ASPxPageControl1_ASPxDateEdit1_DDD_C_FNP_m"))
        # selector.select_by_visible_text("十月")
        # selector = Select(driver.find_element_by_id("ASPxPageControl1_ASPxDateEdit1_DDD_C_FNP_y"))
        # selector.select_by_visible_text("2014")
        # driver.find_element_by_id("ASPxPageControl1_ASPxDateEdit1_DDD_C_FNP_BO").click()
        # selector = Select(driver.find_element_by_id("ASPxPageControl1_ASPxDateEdit1_DDD_C_mt"))
        # selector.select_by_visible_text(31)
        day = '/html/body/form/table/tbody/tr[2]/td/div[1]/div[1]/table[1]/tbody/tr/td[3]/div/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[4]/td[{}]'.format(sys.argv[1])
        driver.find_element_by_xpath(day).click()
        self.doPass()

    def doPass(self):
        driver = self.driver
        while driver.find_element_by_css_selector("img[alt=\"Next\"]").find_element_by_xpath('..').get_attribute('onclick'):
            # self.CleanText()
            driver.execute_script(jstring)
            # time.sleep(0.5)
            driver.find_element_by_css_selector("button[type=\"button\"]").click()
            while True:
                try:
                    driver.find_element_by_xpath("//*[contains(.,'🔘')]")
                    time.sleep(2)
                except:
                    break
            driver.find_element_by_css_selector("img[alt=\"Next\"]").click()

    def CleanText(self):
        driver = self.driver
        for i in range(0, 19):
            try:
               node =  driver.find_element_by_id("ASPxPageControl1_grid1_DXDataRow{}".format(i))
               node.find_element_by_xpath('//td[contains(.,"1688") and @class = "dxgv"]')
               node.find_element_by_xpath('//td[contains(.,"未审核") and @class = "dxgv"]')
            except NoSuchElementException: continue
            node.find_element_by_link_text("修改").click()
            driver.find_element_by_id("ASPxPageControl1_T1T").click()
            length = len(driver.find_elements_by_css_selector("tr[id^='ASPxPageControl1_ASPxGridView1_DXDataRow']"))
            for j in range(0, 3):
                print(j)
                try: item = driver.find_element_by_id("ASPxPageControl1_ASPxGridView1_DXDataRow{}".format(j))
                except NoSuchElementException: break
                self.source = driver.page_source
                item.find_element_by_link_text("编辑").click()
                WebDriverWait(driver, 50).until(self.compare_source) # ((lambda x: x.execute_script("return !Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack()")))
                time.sleep(1)
                driver.switch_to.frame("iframeitem")
                driver.find_element_by_xpath("//span[@title='HTML代码']").click()
                # driver.switch_to.frame(driver.find_element_by_class_name("ke-edit-iframe"))
                content = driver.find_element_by_class_name("ke-edit-textarea")
                newtext = content.get_attribute("value").replace("\n", "\n<br>")
                if not "<p>" in newtext:
                   newtext.replace("\n", "\n<br>")
                   newtext = replaceRegx.sub("\r\n<br>", newtext)
                print(newtext)
                content.clear()
                content.send_keys(newtext)
                driver.switch_to.default_content()
                driver.find_element_by_xpath("//input[@value='更新']").click()
                WebDriverWait(driver, 50).until(self.compare_source) # ((lambda x: x.execute_script("return !Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack()")))
                # print content
            driver.back()
            # driver.back()
                # if not "\n" in content:
                #     driver.find_element_by_class_name( "ke-content").text = ""
                
                #     driver.back()
                # else:
                #     driver.back()
                    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

    def compare_source(self, driver):
        try:
            return self.source != driver.page_source
        except WebDriverException:
            pass
     
if __name__ == "__main__":
   if len(sys.argv) < 2:
      print "Usage: one numerical argument"
      exit(1)
   unittest.main(argv=['tongji.py'])
