# -*- coding: utf-8 -*-
import datetime
from urllib.parse import urlencode
import re

import scrapy

from ..items import SpiderItem


class WeatherSpider(scrapy.Spider):
    name = 'weather'
    allowed_domains = ['www.timeanddate.com']

    def __init__(self, geonames_file=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not geonames_file:
            raise ValueError('geonames_file argument must be supplied')
        with open(geonames_file, 'r') as f:
            self.geonames = [x.strip() for x in f.readlines()]
        self.start_date = datetime.datetime.now()

    def parse(self, response):
        """
        Parse the data from the weather table.

        :param response:
        :return:
        """

        if response.xpath(".//*[contains(text(), 'No data available for the given date. Try selecting a different day.')]"):
            self.logger.warn('No data available')
            return None

        table_rows = response.xpath('.//tbody/tr')

        for row in table_rows:
            item = SpiderItem()
            print(row)
            item['time'] = row.xpath('./th[1]/text()').extract()
            item['imgurl'] = row.xpath('./td[1]/img[1]/@src').extract()
            item['weather'] = row.xpath('./td[2]/text()').extract()
            item['date'] = response.meta['matchtext']
            item['county'] = response.meta['county']
            item['state'] = response.meta['state']
            item['matchtext'] = response.meta['matchtext']
            yield item

    def parse_location(self, response):
        """
        Get the location of the request from the webpage.

        :param response:
        :return:
        """
        # The title of the page contains all the location info
        title = response.xpath('//title/text()').extract()
        county, state = None, None
        if title:
            title = title[0]
            ptn = re.compile('Weather in .*? in (.*?), (.*?), .*')
            match = ptn.match(title)
            if match:
                county, state = match.groups()
        # yield the request to get the weather table data
        yield scrapy.Request(response.meta['weather_url'], meta=dict(
            county=county,
            state=state,
            matchtext=response.meta['matchtext']
        ))

    def start_requests(self):
        # last thursday?
        week_bin_end = self.start_date - datetime.timedelta(days=self.start_date.weekday() - 3)
        # for each weekday of Fri-Thu
        for weekday in (week_bin_end - datetime.timedelta(days=x) for x in range(7)):
            for geoname in self.geonames:
                params = urlencode(dict(
                    year=weekday.year,
                    month=weekday.month
                ))
                url = f'https://www.timeanddate.com/weather/{geoname}/historic?{params}'
                weather_params = urlencode(dict(
                    month=weekday.month,
                    year=weekday.year,
                    n=geoname,
                    mode='historic',
                    hd=weekday.strftime("%Y%m%d")
                ))
                weather_url = f'https://www.timeanddate.com/scripts/cityajax.php?{weather_params}'
                yield scrapy.Request(url, meta=dict(weather_url=weather_url, matchtext=weekday.strftime("%Y%m%d")), callback=self.parse_location)
