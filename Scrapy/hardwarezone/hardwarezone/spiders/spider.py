import scrapy


class KiasuSpider(scrapy.Spider):
    name = 'kiasuparent'

    start_urls = [
        # 'https://www.kiasuparents.com/kiasu/forum/viewforum.php?f=5',
        'https://forums.hardwarezone.com.sg/forums/pc-gaming.382/',
    ]

    def parse(self, response):
        for topic_list in response.xpath('//div[has-class("structItemContainer-group js-threadList")]'):
            for topic in topic_list.xpath('div/div'):
                yield {
                    # 'topic': topic.xpath('div/a/text()').get(),
                    'topic': topic.xpath('div[has-class("structItem-title")]/a/text()').get(),
                }
                yield response.follow(topic.xpath('div[has-class("structItem-title")]/a/@href').get(), \
                    self.parse)

        for post in response.xpath('//div[has-class("message-inner")]'):
            yield {
                'author': post.xpath('//*[has-class("message-name")]/a/text()').get(),
                'content': post.xpath('//div[has-class("bbWrapper")]/text()').get(),
            }

        next_page = response.xpath('//li[has-class("pageNav  pageNav--skipEnd")]/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
