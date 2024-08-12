from icrawler.builtin import GoogleImageCrawler

google_crawler = GoogleImageCrawler(storage={'root_dir': 'C:\\Users\\Marvin\\Desktop\\NFT\\source\\images'})

filters = dict(
    size='large',
    #color='orange',
    license='commercial,modify')
	
	
google_crawler.crawl(keyword='Lebron James signs with Miami',filters=filters, max_num=10)
