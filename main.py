from src.scraper import eBay
from db import DB

# Example of how the program should be run
db = DB()
db.connect()
db.setup_tables()
scraper = eBay()
scraper.scrape(keyword="jeans", quantity=500)
scraper.add_category_to_database()
scraper.add_listings_to_database()
db.connect().close()
