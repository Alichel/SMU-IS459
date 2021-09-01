import scrapy


class HWZSpider(scrapy.Spider):
    name = 'hardwarezone'

    start_urls = [
        'https://forums.hardwarezone.com.sg/forums/pc-gaming.382/',
    ]

    def parse(self, response):
        
        trans_table = {ord(c): None for c in u'\r\n\t'}
        for topic_list in response.xpath('//div[has-class("structItemContainer")]'):
            for thread in topic_list.xpath('//div[has-class("structItem-cell structItem-cell--main")]'):
                
                yield {
                    'topic':thread.xpath('div[has-class("structItem-title")]/a/text()').get(),
                }
        
                yield response.follow(thread.xpath('div[has-class("structItem-title")]/a/@href').get(), \
                    self.parse)

        for post in response.xpath('//div[has-class("block-body js-replyNewMessageContainer")]'):
            yield {
                # join all author into a single line
                'author': "; ".join(post.xpath('//*[@class="message-userDetails"]/h4/a/text()').getall()),

                # remove whitespace (\n\t) and join them into a single line
                'content': "; ".join(s.strip().translate(trans_table) for s in post.xpath('//div[has-class("bbWrapper")]/text()').extract()),

            }

        next_page = response.xpath('//div[has-class("pageNavSimple")]/a[has-class("pageNavSimple-el pageNavSimple-el--next")]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)



