from postscrapper import PostScrapper
from urls import urls_list

if __name__ == "__main__":
  post = PostScrapper()
  i = 1
  for url in urls_list:
    name = 'ex' + str(i) + '.txt'
    post.set_url(urls_list[i-1])
    post.get_content()
    post.write_in_txt(name)
    i += 1
    print(name)

