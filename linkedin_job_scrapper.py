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
from postscrapper import PostScrapper

if __name__ == '__main__':
  #link = "https://www.linkedin.com/jobs/view/3233151332/"
  link = "https://www.linkedin.com/jobs/view/3230861910/"
  #link = "https://www.linkedin.com/jobs/view/3225938561/"
  post = PostScrapper(link)
  post.get_content()
  post.write_in_txt('ex1.txt')
  
  