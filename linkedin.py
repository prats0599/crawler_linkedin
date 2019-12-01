import csv
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from parsel import Selector
import parameters

def validate_field(field):
    if field:
        pass
    else :
        field=""
    return field


writer=csv.writer(open(parameters.file_name,'w'))
writer.writerow(['Name','Job title','school','location','url'])

driver=webdriver.Chrome('C:\webdrivers\chromedriver')
driver.get("https://www.linkedin.com")
sign_in_page=driver.find_element_by_class_name('nav__button-secondary')
sign_in_page.click()


username=driver.find_element_by_name('session_key')
username.send_keys("pratyushparashar1999@gmail.com")
sleep(0.5)
password=driver.find_element_by_name('session_password')
password.send_keys("shibu_1999")
sleep(0.5)
sign_in_button=driver.find_element_by_xpath('//*[@type="submit"]')
sign_in_button.click()
sleep(5)

driver.get("https://www.google.com")
search_query=driver.find_element_by_name('q')
search_query.send_keys('site:linkedin.com/in/ AND "python developer" AND "London"')

search_query.send_keys(Keys.RETURN)

linkedin_urls=driver.find_elements_by_tag_name('cite')
linkedin_urls=[url.text for url in linkedin_urls]
sleep(0.5)

for linkedin_url in linkedin_urls:
    driver.get(linkedin_url)
    sleep(5)

    sel=Selector(text=driver.page_source) #driver.page_source is equivalent to scrapy's response.body
    name=sel.xpath('//h1/text()').extract_first()
    if "0 " in name:
        name=sel.xpath('//*[@class="inline t-24 t-black t-normal break-words"]/text()').extract_first()
    job_title=sel.xpath('//h2/text()').extract_first()
    location=sel.xpath('//h3/text()').extract_first()
    school=sel.xpath('//*[starts-with(@class,"pv-top-card-section__school")]/text()').extract_first()
    if school:
        school=school.strip()

    linkedin_url=driver.current_url

    name=validate_field(name)
    job_title=validate_field(job_title)
    school=validate_field(school)
    location=validate_field(location)
    linkedin_url=validate_field(linkedin_url)
    print("""
    \n
    name:{}
    Job title:{}
    school:{}
    location:{}
    url:{}""".format(name,job_title,school,location,linkedin_url))
    writer.writerow([name.encode('utf-8'),
    job_title.encode('utf-8'),
    school.encode('utf-8'),
    location.encode('utf-8'),
    linkedin_url.encode('utf-8')])
    try:
        connect=driver.find_element_by_xpath('//span[text()="Connect"]')
        connect.click()
        sleep(3)
    except:
        pass


driver.quit()
