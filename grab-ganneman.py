# скачиваем каталог моно лекарств - препарат и описание
# https://apteka-ganneman.ru/%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3/%D0%BC%D0%BE%D0%BD%D0%BE%D0%BF%D1%80%D0%B5%D0%BF%D0%B0%D1%80%D0%B0%D1%82%D1%8B/%D0%BC%D0%BE%D0%BD%D0%BE%D0%BF%D1%80%D0%B5%D0%BF%D0%B0%D1%80%D0%B0%D1%82%D1%8B.html
import requests, bs4, openpyxl
from tqdm import *
prefix = 'https://apteka-ganneman.ru'
base_url = 'https://apteka-ganneman.ru/%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3/%D0%BC%D0%BE%D0%BD%D0%BE%D0%BF%D1%80%D0%B5%D0%BF%D0%B0%D1%80%D0%B0%D1%82%D1%8B/%D0%BC%D0%BE%D0%BD%D0%BE%D0%BF%D1%80%D0%B5%D0%BF%D0%B0%D1%80%D0%B0%D1%82%D1%8B.html'
headers = {'accept': '*/*',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}
session = requests.Session()
s0 = session.get(base_url, headers=headers)

b = bs4.BeautifulSoup(s0.text, "html.parser")


def dwn(catlist, fname):
    # создаем новый excel-файл
    wb = openpyxl.Workbook()

    # добавляем новый лист
    wb.create_sheet(title='Первый лист', index=0)
    # получаем лист, с которым будем работать
    sheet = wb['Первый лист']
    # заголовок
    cell = sheet.cell(row=1, column=1)
    cell.value = 'Название'
    cell = sheet.cell(row=1, column=2)
    cell.value = 'Описание'
    r = 2

    for item in tqdm(catlist):
        # if item.text == 'Бариум ацетикум':
        print(item.text, item.get('href'))
        prep_url = item.get('href')
        s = session.get(prefix + prep_url, headers=headers)
        bs = bs4.BeautifulSoup(s.text, "html.parser")
        bs1 = bs.select('.itemBody')[0]
        # удаляем не нужную таблицу сверху
        for tag in bs1.find_all('table'):
            tag.extract()
        print(bs1.text)

        prep_name = item.text.strip()
        prep_opis = bs1.text.strip()

        cell = sheet.cell(row=r, column=1)
        cell.value = prep_name
        cell = sheet.cell(row=r, column=2)
        cell.value = prep_opis
        r = r + 1

        wb.save(fname+'.xlsx')

monop = b.select('table')[0].select('a')
smesi = b.select('table')[1].select('a')
dwn(smesi, 'Smesi')

    #for pre in monop:
    #    print(pre.text, pre.get('href'))



#print(monop)
#print('-'*150)
#print(smesi)