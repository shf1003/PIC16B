# to run 
#scrapy crawl tmdb_spider -o results.csv

import scrapy

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    #the orignal page chosen to scrapy
    start_urls = ['https://www.themoviedb.org/tv/100088-the-last-of-us']
    
    """
    start from the original site we given as start_urls,
    navigate to Full cast & crew page
    return a parse request to a callback scrapy
    """
    def parse(self,response):
        #get link for next page
        next_page = response.css("p.new_button a::attr(href)").get()
        #join urls
        next_page = response.urljoin(next_page)
        #going to the next page,calling parse_full_credits function
        yield scrapy.Request(next_page,callback=self.parse_full_credits)       
   
    """
    start from the Full Cast & Crew page,
    to Request for the page of each actor listed on the page;
    return a yield scrapy of each listed actor
    """
    def parse_full_credits(self,response):
        #get link for all actors listed in this page,exlucing crew
        all_actors_url=response.css("ol.people.credits:not(.crew) a::attr(href)").getall()
        #loop though and join the links
        all_actors=["https://www.themoviedb.org" + a for a in all_actors_url]
        ##going to each actor's page,calling parse_actor_page
        for actor_link in all_actors:
            yield scrapy.Request(actor_link, callback=self.parse_actor_page)
        
   
    """
    start on the page of an actor,
    create a dictionary for each of the movies or TV shows on which that actor has worked
    return a yield dictionary with two key-value pairs
    """
    
    def parse_actor_page(self,response):
        
        #get actor's name from the title
        actor_name = response.css("h2.title a::text").get()
        #get names of movies and tv shows
        movies_name = response.css("table.credit_group a.tooltip bdi::text").getall()
        #create a dictionary or each of the movies or TV shows on which that actor has worked
        for movie_or_TV_name in movies_name:
            yield{"actor": actor_name,
            "movie_or_TV_name": movie_or_TV_name}
            




