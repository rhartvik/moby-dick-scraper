import scrapy
import os

class GlutenbergSpider(scrapy.Spider):
  name = "glutenberg"

  def start_requests(self):
    urls = [
      'https://www.gutenberg.org/files/2701/2701-h/2701-h.htm',
    ]
    for url in urls:
      yield scrapy.Request(url=url, callback=self.parse)

  def parse(self, response):
    folder_name = 'moby_dick_text'
    if not os.path.exists(folder_name):
      os.makedirs(folder_name)

    for chapter_title in response.css('h2').re('CHAPTER (\d+\. .*)\.'):

      chapter_filename = folder_name + '/' + chapter_title
      with open(chapter_filename, 'wb') as f:
        f.write('put chapter contents here')
    with open('response', 'wb') as f:
      f.write(response.body)
    self.log('Saved response')
