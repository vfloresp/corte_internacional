from PyPDF2 import PdfFileReader
import os
import re


class FileReader():

    def __init__(self, path):
        self.path = path
        self.num_cita = 0

    def read_files(self):
        for root, _, files in os.walk(self.path):
            for file in files:
                path = os.path.join(root, file)
                pdf_file = PdfFileReader(path)
                self.read_file(pdf_file)

    def read_file(self, pdf_file):
        n = pdf_file.getNumPages()
        for i in range(n):
            page = pdf_file.getPage(i)
            text = page.extractText()
            if i == 0:
                self.process_first_page(text)
            else:
                self.process_text(text)

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

    def process_text(self, text):
        text_list = text.split()
        self.get_citas(text_list)

    def get_citas(self, text_list):
        text_reversed = self.reverse_list(text_list)
        citas = []
        cita = {'texto': '', 'num': None}
        texto = []
        finCita = False
        for string in text_reversed:
            if finCita:
                cita['num'] = int(string)
                self.num_cita = cita['num']
                cita['texo'] = self.inverted_list_to_text(texto)
                citas.append(cita)
                texto = []
                finCita = False
            else:
                texto.append(string)
            if string == 'Cfr.':
                finCita = True
        print(citas)
        return citas

    def inverted_list_to_text(self, inverted_list):
        list = self.reverse_list(inverted_list)
        text = ' '
        join_text = text.join(list)
        return join_text

    def reverse_list(self, text_list):
        text_reversed = [s for s in reversed(text_list)]
        return(text_reversed)


if __name__ == '__main__':
    file_reader = FileReader('../files/')
    file_reader.read_files()
