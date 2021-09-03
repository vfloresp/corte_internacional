from PyPDF2 import PdfFileReader
from icecream import ic
from case_reader import CaseReader
import pandas as pd
import numpy as np
import os
import re


class FileReader():

    def __init__(self, path):
        self.path = path

    def read_files(self):
        citas_complete = []
        for root, _, files in os.walk(self.path):
            for file in files:
                path = os.path.join(root, file)
                cr = CaseReader(file)
                num_caso = cr.get_id(file)
                if int(num_caso) > 67:
                    ic('Procesando: ', file)
                    pdf_file = PdfFileReader(path)
                    citas_file = self.read_file(pdf_file)
                    if citas_file:
                        citas_complete += citas_file
        self.save_citas_complete(citas_complete, num_caso)
        """
        filename = 'Corte IDH. Caso Vélez Loor Vs. Panamá. Excepciones Preliminares, Fondo, Reparaciones y Costas. Sentencia de 23 de noviembre de 2010. Serie C No. 218'
        cr = CaseReader(filename)
        num_caso = cr.get_id(filename)
        if int(num_caso) > 67:
            pdf_file = PdfFileReader(
                '/Storage/CIAJ/corte_internacional/files/Corte IDH. Caso Vélez Loor Vs. Panamá. Excepciones Preliminares, Fondo, Reparaciones y Costas. Sentencia de 23 de noviembre de 2010. Serie C No. 218.pdf')
            self.read_file(pdf_file, num_caso)
            ic('Procesando: ', filename)
        """

    def read_file(self, pdf_file):
        n = pdf_file.getNumPages()
        citas_file = []
        for i in range(1, n):
            page = pdf_file.getPage(i)
            text = page.extractText()
            citas_page = self.process_text(text)
            if citas_page:
                citas_file += citas_page
        return citas_file

    def process_text(self, text):
        text_list = text.split()
        citas_page = self.get_citas(text_list)
        return citas_page

    def save_citas_complete(self, citas_complete, num_caso):
        df_citas_complete = pd.DataFrame(citas_complete)
        df_citas_complete['id_sentencia_origen'] = num_caso
        df_citas_complete.to_csv('citas_completas.csv', index=False)

    def get_citas(self, text_list):
        text_reversed = self.reverse_list(text_list)
        cita = {'texto': '', 'num': None}
        citas = []
        texto = []
        finCita = False
        for string in text_reversed:
            if finCita:
                try:
                    cita['num'] = int(string)
                except:
                    cita['num'] = np.nan
                cita['texto'] = self.inverted_list_to_text(texto)
                citas.append(cita)
                cita = {'texto': '', 'num': None}
                texto = []
                finCita = False
            else:
                texto.append(string)
            if string == 'Cfr.':
                finCita = True
        return citas

    def inverted_list_to_text(self, inverted_list):
        list = self.reverse_list(inverted_list)
        text = ' '
        join_text = text.join(list)
        return join_text

    def reverse_list(self, text_list):
        text_reversed = [s for s in reversed(text_list)]
        return(text_reversed)

    def process_first_page(self, text):
        text_split = text.splitlines()
        garbage = ['', ' ', ',', ', ']
        text_clean = [x for x in text_split if x not in garbage]
        caso = self.get_caso(text)
        jueces = self.get_jueces(text)

    def get_caso(self, text):
        flag = False
        caso = ' '
        for string in text:
            if flag:
                string = string if caso[-1] == ' ' else ' ' + string
                caso += string
            elif 'CASO' in string:
                flag = True
            if re.search(r'[12]\d{3}', string) != None:
                break
        return caso.strip()

    def get_jueces(self, text):
        index = text.index(':') + 1
        text_jueces = text[index:]
        jueces = []
        separadores = [';', 'y']
        temp = ''
        ultimo = False
        for string in text_jueces:
            if string[-1] in separadores or ultimo:
                string = string if temp == '' else temp + string
                jueces.append(string)
                temp = ''
                ultimo = True if string[-1] == 'y' else False
            else:
                temp += string
            if string == 'presente':
                break
        return jueces


if __name__ == '__main__':
    file_reader = FileReader('../files/')
    file_reader.read_files()
