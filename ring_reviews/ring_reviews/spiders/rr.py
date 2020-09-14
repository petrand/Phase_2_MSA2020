import scrapy


class RrSpider(scrapy.Spider):
    name = 'rr'
    allowed_domains = ['amazon.com']
    start_urls = ['https://amazon.com/Ring-Doorbell-Activated-Installation-existing/product-reviews/B01DM6BDA4/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&pageNumber=1']

    def parse(self, response):
        reviews = response.xpath('//div[@class="a-section review aok-relative"]//div[@class="a-row"]//a[@class="a-link-normal"]//span[@class="a-icon-alt"]/text()')
        comments = response.xpath('//span[@class="a-size-base review-text review-text-content"]//span')
        dates = response.xpath('//div[@class="a-section review aok-relative"]//span[@data-hook="review-date"]/text()')
        comment_head = response.xpath('//div[@class="a-section review aok-relative"]//span[@data-hook="review-voting-widget"]')
        titles = response.xpath('//div[@class="a-section review aok-relative"]//a[@data-hook="review-title"]//span/text()')

        for i in range(0,len(reviews)):
            comment = comments[i].getall()
            score = reviews[i].getall()
            date = dates[i].getall()
            title = titles[i].getall()
            helpful = comment_head[i].xpath('./div/span[@data-hook="helpful-vote-statement"]/text()').get()
            
            yield {"Score": score, "Title": title, "Helpful": helpful, "Date":date, "Comment": comment}
            
        yield scrapy.Request(str("https://amazon.com" + response.xpath('//ul[@class="a-pagination"]//li[@class="a-last"]//a/@href').get()), callback = self.parse)
    