import scrapy
import logging
import io
from PyPDF2 import PdfFileReader
import urllib.request


class SpiderCitas(scrapy.Spider):
    name = "citas"

    def start_requests(self):
        url = "https://www.corteidh.or.cr/casos_sentencias.cfm"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        sentencias = response.xpath(
            '//*[@class="tr_normal search-result row"]/div/table/tbody/tr[1]/td[2]/a[1]/@href'
        ).getall()
        logging.info(sentencias)
        for sentencia in sentencias:
            yield scrapy.Request(url=sentencia, callback=self.parse_sentencia)

    def parse_sentencia(self, response):
        logging.info(response)
        resp = urllib.request.urlopen(response)
        file = open("file"+"pdf", "wb")
        file.write(resp.read())
        file.close()
        """with io.BytesIO(response) as f:
            pdf = PdfFileReader(f)
            info = pdf.getDocumentInfo()
            logging.info(info)
            """
