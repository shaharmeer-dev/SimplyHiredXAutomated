import yaml
from Scrapper import Scrapper
import logging
from datetime import datetime
import os

# Create logs directory if it doesn't exist
if not os.path.exists('simplyhired_logs'):
    os.makedirs('simplyhired_logs')

# Configure logging
log_filename = f'simplyhired_logs/simplyhired_scraper_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()  # This will also print to console
    ]
)
logger = logging.getLogger(__name__)



i = Scrapper()

i.random_sleep(2, 5)



filter_titles =[]
with open("filterTitles.yml", "r") as file:
    config = yaml.safe_load(file)

    for title in config["job_titles"]:
        filter_titles.append(title)

logger.info(filter_titles)



for title in filter_titles:
    try:
        i.scrape_jobs_with_title(title)
    except Exception as e:
        logger.error(f"Error occurred for {title}: {e}")
        continue
