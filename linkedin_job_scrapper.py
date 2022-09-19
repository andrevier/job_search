'''
Example of web scraping for a job position at linkedin.
This method needs the web page of the post and not the search page, where you 
search for open positions. First, you have to search the position. Once you 
found it, you copy the link and paste it in the variable called post_link. 
Then, the code follows the link with the webdriver and get the main 
informations, such as: Job title, Company, Place, and descriptions.

Log in is an option.

You can change the web driver to other browsers, such as Firefox.

You can extend this version to get other informations if you like.
DD-MM-YY
18/09/22
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

class PostScrapper:
  '''Class to manage the scrapping of useful informations in the post.'''
  def __init__(self, link):
    self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    self.post_link = link

    # Delay time to wait the browser to open.
    self.sleep_time = 4
    
    # Parameters for the search the informations in the page's html.
    self.job_title_selector = "top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title"
    self.job_title_selector_type = 'class'
    self.job_title_selector_tag = 'h1'

    self.company_selector = "topcard__org-name-link topcard__flavor--black-link"
    self.company_selector_type = 'class'
    self.company_selector_tag = 'a'
    
    self.place_selector = "topcard__flavor topcard__flavor--bullet"
    self.place_selector_type = 'class'
    self.place_selector_tag = 'span'
    
    self.criteria_selector = "description__job-criteria-text description__job-criteria-text--criteria"
    self.criteria_selector_type = 'class'
    self.criteria_selector_tag = 'span'

    self.post_selector = "show-more-less-html__markup show-more-less-html__markup--clamp-after-5"
    self.post_selector_type = 'class'
    self.post_selector_tag = 'div'

    # Attributes for the important informations in the post.
    self.title = ''
    self.company = ''
    self.place = ''
    self.criteria = []
    self.job_desc = []
  
  def get_content(self):
    '''Method to open the post's page, and get the content.'''
    self.driver.get(self.post_link)

    # Waiting some seconds to show the page in the browser.
    time.sleep(self.sleep_time)
    
    # Get the post source code and transform it into a Beautiful Soup object.
    soup = BeautifulSoup(self.driver.page_source, 'html.parser')
    
    # Look for the content in the BS object.
    # Title
    for data in soup.findAll(self.job_title_selector_tag, { self.job_title_selector_type: self.job_title_selector}):
      self.title = data.string.lstrip() + '\n\n'
    
    # Company
    for data in soup.findAll(self.company_selector_tag, {self.company_selector_type, self.company_selector }):
      self.company = data.string.lstrip() + '\n'
    
    # Place
    for data in soup.findAll(self.place_selector_tag, {self.place_selector_type, self.place_selector}):
      self.place = data.string.lstrip() + '\n'
    
    # Job's criteria: exp. level, woring time, area, and activity. 
    for data in soup.findAll(self.criteria_selector_tag, {self.criteria_selector_type, self.criteria_selector}):
      self.criteria.append(data.string.lstrip() + '\n')
    
    # Job description.
    for elem in soup.findAll(self.post_selector_tag, {self.post_selector_type, self.post_selector}):
      for p in elem.findAll('p'):
        if p.string == None:
          self.job_desc.append('\n')
        else:
          self.job_desc.append(p.string)
          self.job_desc.append('\n')
    
    # Close the browser.
    self.driver.close()
    return (self.title, self.company, self.place, self.criteria,
            self.post_link, self.job_desc)

  def write_in_txt(self, filename=''):
    '''Method to write the post content into a .txt file.'''
    with open(filename, 'w', encoding='utf-8') as f:
        # Position's title.
        f.write(self.title)

        # Position's company.
        f.write(self.company)

        # Criteria 
        for line in self.criteria:
            f.write(line)
        
        # Link
        f.write(self.post_link + '\n\n')

        # Post text.
        for line in self.job_desc:
            f.write(line)
    

if __name__ == '__main__':
  post = PostScrapper("https://www.linkedin.com/jobs/view/3233151332/")
  post.get_content()
  post.write_in_txt('ex1.txt')
  