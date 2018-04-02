import scrapy
from scrapy.selector import Selector
import os
import re

class GlutenbergSpider(scrapy.Spider):
  name = "glutenberg"

  def start_requests(self):
    urls = [
      'https://www.gutenberg.org/files/2701/2701-h/2701-h.htm',
    ]
    for url in urls:
      yield scrapy.Request(url=url, callback=self.parse)

  def parse(self, response):

    with open('response', 'wb') as f:
      f.write(response.body)
    self.log('Saved response')

    folder_name = 'moby_dick_text'
    if not os.path.exists(folder_name):
      os.makedirs(folder_name)

    chapters = re.split('<div style="height: 4em;">\s*\n\s*(<br\s*/>)+\s*\n\s*</div>', response.body)

    for chapter in chapters:
      selector = Selector(text=chapter)
      chapter_title = selector.css('h2').re_first('CHAPTER (\d+\. .*)\.')
      if (chapter_title is not None):
        chapter_contents = selector.xpath('//p/text()').extract()
        #chapter_contents = selector.css('p::text').extract()
        chapter_filename = folder_name + '/' + chapter_title
        with open(chapter_filename, 'wb') as f:
          for paragraph in chapter_contents:
            f.write(paragraph.encode('utf-8'))
            f.write('')
        self.log('Saved ' + chapter_title)
