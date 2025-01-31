import yaml
from Scrapper import Scrapper
i = Scrapper()

i.random_sleep(2, 5)



filter_titles =[]
with open("filterTitles.yml", "r") as file:
    config = yaml.safe_load(file)

    for title in config["job_titles"]:
        filter_titles.append(title)

print(filter_titles)



for title in filter_titles:
    try:
        i.scrape_jobs_with_title(title)
    except Exception as e:
        print(f"Error occurred for {title}: {e}")
        continue
