from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import urllib.parse
 
def getLinks(allLinks, driver):
 
	source = driver.page_source
	soup = BeautifulSoup(source, "html.parser")
 
	for product in soup.findAll('a', class_="a-link-normal s-access-detail-page  a-text-normal"):
		link = product.get('href')
		if link not in allLinks:
			allLinks.append((link, product.get('title')))
		else:
			continue
 
	return allLinks
 
# collects product links from the first page of amazon search results
def getProductLinks(keyword, driver):
 
	driver.get("http://www.amazon.com")
 
	searchElement = driver.find_element_by_id("twotabsearchtextbox")
	searchElement.send_keys(keyword, Keys.ENTER)
 
	allLinks = []
 
	result = getLinks(allLinks, driver)
 
	return result
 
def saveFiles(keyword, content):
	print("saving...", end = "")

	newPath = keyword + '.txt'
	newFile = open(newPath, 'wt')
  
	newFile.write(content)

	print("done")
 
def getProductInfo(keyword, products, count, driver):

	searched = 0
	content = ""
 
	for link in products:

		if searched == count:
			break
  
		try:
			content += "Link:" + link[0] + "\n" + "Title:" + link[1] + "\n\n"
			searched += 1
	 
		except:
			continue

	saveFiles(keyword, content)
 
		
  
def run(): 
	keyword = input("please enter a search term:")
	count = input("please enter number of items to search for:")
	count = int(count)
	driver = webdriver.Chrome()
 
	products = getProductLinks(keyword, driver)
	getProductInfo(keyword, products, count, driver)
 
	driver.quit()
 
if __name__=="__main__":
	run()