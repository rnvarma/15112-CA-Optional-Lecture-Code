##############################
########### PART 1 ###########
##############################

from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.google.com/")
assert("Google" in driver.title)

#driver.quit()

##############################
########### PART 2 ###########
##############################

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://www.google.com/")

elem = driver.find_element_by_name("q")
#elem = driver.find_element_by_id("lst-ib")
#elem = driver.find_element_by_class_name("gsfi")
#elem = driver.find_element_by_xpath('//*[@id="lst-ib"]')

'''
a note about the xpath:

the xpath finds an element based on its relative positioning
on a webpage
if the arrangement of a webpage changes, the class name
or element name may not change, but the xpath is likely to
change
this means your code may be broken if a webpage changes its
layout

however, sometimes xpaths are good because not all elements
have a name / id / class name etc. but elements always have
xpaths

do note that " appears in xpaths, always enclose xpaths in
' '

'''

#type something in the search box
elem.send_keys("xkcd")

#enter
elem.send_keys(Keys.RETURN)

#the following lines crash
#elemResult = driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div/h3/a')
#elemResult.send_keys(Keys.RETURN)

#driver.quit()

##############################
########### PART 3 ###########
##############################

from selenium import webdriver

driver = webdriver.Chrome()
driver.get("http://www.xkcd.com")

#driver.quit()

##############################
########### PART 4 ###########
##############################

from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.get("http://www.xkcd.com/archive")

pageSource = driver.page_source

#convert into a BeautifulSoup object for the library
soup = BeautifulSoup(pageSource, 'html.parser')

#the following line doesn't actually do anything useful
#it just makes the page source better formatted for
#human eyes
#print(soup.prettify().encode("ascii", "ignore"))

print(soup.title)
print(soup.title.name)

print(soup.get_text())

##############################
########### PART 5 ###########
##############################

from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.get("http://www.xkcd.com/archive")

pageSource = driver.page_source

#convert into a BeautifulSoup object for the library
soup = BeautifulSoup(pageSource, 'html.parser')

#filters

#find all elements with tag 'a'
links = soup.find_all('a')

for link in links:
    print(link)

#find all elements with tag 'a' and 'title'
links = soup.find_all(['a', 'title'])

for link in links:
    print(link)

#find all elements in the middle container
middleContainerTag = soup.find_all(id="middleContainer", class_="box")
print(middleContainerTag)

for child in middleContainerTag:
    print(child.get_text())

##############################
########### PART 5 ###########
##############################

from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.get("http://www.xkcd.com/archive")

pageSource = driver.page_source

#convert into a BeautifulSoup object for the library
soup = BeautifulSoup(pageSource, 'html.parser')

comic = soup.find_all('a', text = "Angular Momentum")

print(comic)

for element in comic:
    href = (element.get('href'))
	newUrl = 'http://xkcd.com%s' % href
	driver.get(newUrl)

	assert("Angular Momentum" in driver.title)
	print(driver.current_url)

#driver.quit()