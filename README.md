# Scraper to gather historical weather data

## Usage

### Command Line

```bash
cd spider
scrapy crawl weather -a geonames_file=./path/to/geonames.csv -o out.csv
```

### Docker

```bash
docker build -t weather-spider .
docker run -it --rm weather-spider -a /spider/geonames.csv
```

Note: You may want to mount a volume and provide the `geonames.csv` file
there, as well as the output file.

```bash
docker run -it --rm weather-spider -a /mnt/whatever/geonames.csv -o /mnt/whatever/out.csv
```
