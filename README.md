# A Module for Crawling iMDB Movie Data and Subtitles

## Installation
* Requires Python 3. 
* (Recommended) Create and activate a new virtual environment.
* Install the requirements (including a particular version of `python-opensubtitles` from the GitHub repo):
```bash
pip install -r requirements.txt
```

## Crawling iMDB Data
See `imdb_crawl/spiders/imdb-collect.py`. To run a crawler, execute the following command:
```bash
scrapy crawl imdb-collect
```
For more information, please refer to the [Scrapy Documentation](https://docs.scrapy.org/en/latest/).

## Downloading Subtitles from OpenSubtitles
[OpenSubtitles.org](https://www.opensubtitles.org/en/search) has API limits of 200 per day for free users, 1000 for VIP. For this project, the majority of subtitles were acquired from a dump provided by OpenSubtitles team.

`dl_sub.py` is a script for downloading subtitles using OpenSubtitles API. Before using it, open the script and set `OPENSUBTITLES_ACCOUNT_NAME`, `OPENSUBTITLES_ACCOUNT_PASSWORD` to your credentials and `DOWNLOAD_LIMIT` based on your account limits. To run, simply execute:
```bash
python dl_sub.py
``` 

The subtitles will all be stored in `subtitles` folder unorganised. To organise them into proper folder structure, please use script `scripts/organise_subtitles.py`.

While the script is running, the logs will be saved at `logs/log.txt`, useful to see progress. To track logs live on your terminal, run:
```bash
tail -fn 1500 logs/log.txt
```