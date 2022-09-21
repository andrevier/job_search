from postscrapper import PostScrapper
import urls

if __name__ == "__main__":
  post = PostScrapper()
  
  j = 61
  for url in urls.urls_list_21_09_22:
    name = 'ex' + str(j) + '.txt'
    post.set_url(url)
    post.get_content()
    post.write_in_txt(name)
    j += 1
    print(name)

