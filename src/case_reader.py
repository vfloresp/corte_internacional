from PyPDF2 import PdfFileReader
import pandas as pd
import numpy as np
import re
import os


class CaseReader():
    COLS = ['id_sentencia', 'caso_nombre', 'fecha']

    def __init__(self, path=None):
        self.df_cases = pd.DataFrame(columns=self.COLS)
        self.path = path

    def read_files(self):
        for root, _, files in os.walk(self.path):
            for file in files:
                path = os.path.join(root, file)
                id_sentencia = self.get_id(file)
                nombre = self.get_nombre(path)
                fecha = self.get_fecha(path)
                self.add_to_df(id_sentencia, nombre, fecha)
        self.save_cases()

    def add_to_df(self, id_sentencia, nombre, fecha):
        global cols
        new_row = pd.DataFrame(
            [[id_sentencia, nombre, fecha]], columns=self.COLS)
        self.df_cases = pd.concat([self.df_cases, new_row])

    def get_id(self, file_name):
        id_sentencia = file_name.split(' ')[-1].split('.')[0]
        return id_sentencia

    def get_nombre(self, file_name):
        nombre = re.search(r'(?<=Caso)[^\.]*.[^\.]*', file_name)[0]
        not_contains_vs = not 'Vs.' in nombre
        ends_vs = nombre.split(' ')[-1] == 'Vs.'
        if ends_vs:
            nombre = re.search(r'(?<=Caso)[^\.]*.[^\.]*.[^\.]*', file_name)[0]
        elif not_contains_vs:
            nombre = re.search(
                r'(?<=Caso)[^\.]*.[^\.]*.[^\.]*.[^\.]*', file_name)[0]
        return nombre

    def get_fecha(self, file_name):
        try:
            fecha = re.findall(r'(?<=Sentencia de).*?(?=\.)', file_name)[0]
            fecha = fecha.strip()
            if not fecha[0].isnumeric():
                fecha = re.findall(r'(?<=Sentencia de).*?(?=\.)', file_name)[1]
        except:
            try:
                fecha = re.search(r'(?<=Resolución de).*?(?=\.)', file_name)[0]
            except:
                fecha = np.nan
        return fecha

    def save_cases(self):
        self.df_cases.to_csv('casos.csv', index=False)


if __name__ == '__main__':
    PATH = '../files/'
    case_reader = CaseReader(PATH)
    case_reader.read_files()
