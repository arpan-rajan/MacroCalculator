from recipe_scrapers import scrape_me


def scrapeWebsite(url):
    scraper = scrape_me(url)

    return scraper.title(), scraper.total_time(), scraper.ingredients(), scraper.instructions(), scraper.links()
