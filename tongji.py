# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
import unittest, time, re
import io, time, sys

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
        day = '/html/body/form/table/tbody/tr[2]/td/div[1]/div[1]/table[1]/tbody/tr/td[3]/div/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[6]/td[{}]'.format(sys.argv[1])
        driver.find_element_by_xpath(day).click()
        self.doPass()

    def doPass(self):
        driver = self.driver
        while driver.find_element_by_css_selector("img[alt=\"Next\"]").find_element_by_xpath('..').get_attribute('onclick'):
            driver.execute_script(jstring)
            self.CleanText()
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
        elements = driver.find_elements_by_css_selector("tr[id^='ASPxPageControl1_grid1_DXDataRow'].dxgvDataRow_Aqua")
        for node in elements:
            try: node.find_element_by_link_text("1688.com")
            except NoSuchElementException: continue
            node.find_element_by_link_text("修改").click()
            driver.find_element_by_id("ASPxPageControl1_T1T").click()
            for item in driver.find_element_by_css_selector("tr[id^='ASPxPageControl1_grid1_DXDataRow'].dxgvDataRow_Aqua"):
                item.find_element_by_link_text("编辑").click()
                content = driver.find_element_by_class_name("ke-content").text
                if not "\n" in content:
                    driver.find_element_by_class_name("ke-content").text = ""
                    driver.find_element(By.XPATH("//input[@value='更新']")).click()
                    driver.back()
                else:
                    driver.back()
                    
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

if __name__ == "__main__":
   if len(sys.argv) < 2:
      print "Usage: one numerical argument"
      exit(1)
   unittest.main(argv=['tongji.py'])
