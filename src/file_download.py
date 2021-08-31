from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import os


class FileManager():

    def __init__(self, url):
        self.current_files = None
        self.new_files = None
        self.missing_files = None
        self.url = url

    def update_db(self):
        self.current_files = self.find_existing_files()
        self.new_files = self.find_new_files(self.url)
        self.missing_files = self.find_missing_files(
            self.current_files, self.new_files)
        for file, url in self.missing_files.items():
            self.download_file(file, url)

    def find_new_files(self, url):
        response = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(response).read()
        soup = BeautifulSoup(webpage, 'lxml')
        links = soup.find_all('li')
        print(soup)
        pass

    def find_existing_files(self):
        existing_files = []
        for _, _, files in os.walk('../files/'):
            for file in files:
                existing_files.append(file)
        return existing_files

    def find_missing_files(self, current_files, new_files):
        new_filenames = list(new_files.keys())
        diff_names = list(set(new_filenames) - set(current_files))
        diff = new_files[diff_names]
        return diff

    def download_file(self, filename, file_url):
        resp = urlopen(file_url)
        file = open("../files/"+filename+".pdf", 'wb')
        file.write(resp.read())
        file.close()


if __name__ == '__main__':
    URL_CORTE = 'https://www.corteidh.or.cr/casos_sentencias.cfm'
    file_manager = FileManager(URL_CORTE)
    file_manager.download_file('Corte IDH Caso Martínez Esquivia Vs Colombia Interpretación de la Sentencia de Excepciones preliminares Fondo y Reparaciones Sentencia de 21 de junio de 2021 Serie C No. 428',
                               'https://www.corteidh.or.cr/docs/casos/articulos/seriec_428_esp.pdf')
