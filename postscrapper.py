from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

class PostScrapper:
  def __init__(self, url = ''):
    '''Class to manage the scrapping of useful informations in the post.'''
    self.driver = webdriver.Firefox()
    #self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    self.url = url

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
  
  def set_url(self, url):
    '''Method to set a new post's url.'''
    self.url = url
  
  @classmethod
  def html_to_text(cls, soup):
    '''Receive a tag object from BeautifulSoup and parse the sequence of tags
    into a text, separating the tags in lines.'''
    
    # Rip out all script and style elements and the strong tag.
    for script in soup(["script", "style", "strong"]):
        script.extract() 
    
    text = soup.get_text('\n')

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())

    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text

  def get_content(self):
    '''Method to open the post's page, and get the following itens:
    Job position
    Company
    Place
    Experience level
    Working time
    Area
    Description
    .'''
    self.driver.get(self.url)

    # Waiting some seconds to show the page in the browser.
    time.sleep(self.sleep_time)
    
    # Get the post source code and transform it into a Beautiful Soup object.
    soup = BeautifulSoup(self.driver.page_source, 'html.parser')
    
    # Look for the content in the BS object.
    # Title
    for data in soup.findAll(self.job_title_selector_tag, { self.job_title_selector_type: self.job_title_selector}):
      self.title = data.string.lstrip() + '\n\n'
      #self.title = PostScrapper.html_to_text(data)
    
    # Company
    for data in soup.findAll(self.company_selector_tag, {self.company_selector_type, self.company_selector }):
      self.company = data.string.lstrip() + '\n'
      #self.company = PostScrapper.html_to_text(data)
    
    # Place
    for data in soup.findAll(self.place_selector_tag, {self.place_selector_type, self.place_selector}):
      self.place = data.string.lstrip() + '\n'
      #self.place = PostScrapper.html_to_text(data)
    
    # Job's criteria: exp. level, working time, area, and activity. 
    for data in soup.findAll(self.criteria_selector_tag, {self.criteria_selector_type, self.criteria_selector}):
      self.criteria.append(data.string.lstrip() + '\n')

    # Job description.
    for elem in soup.findAll(self.post_selector_tag, {self.post_selector_type, self.post_selector}):
      # self.job_desc = elem
      self.job_desc = PostScrapper.html_to_text(elem)

    # Close the browser.
    self.driver.close()
    return (self.title, self.company, self.place, self.criteria,
            self.url, self.job_desc)

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
      f.write(self.url + '\n\n')

      # Job's description.
      f.write(self.job_desc)
