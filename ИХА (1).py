#!/usr/bin/env python
# coding: utf-8

# # Технический блок

from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from datetime import date

BROWSER = Chrome('/Users/ddiom/chromedriver')
URL = 'https://covid.rm.mosreg.ru/issues/new?tracker_id=29'
BROWSER.get(URL)

# # Блок получения данных
bd = {
    "SNILS": str,
    "Surname": str,
    "Name": str,
    "Patronim": str,
    "Phone": str,
    "Birthday": date,
    "Sex": str,
    "Address": str,
    "Dr": str,
    "City": str,
    "Job": str,
    "PatientType": str,
    "CurrentState": str,
    "KindProbe": str,
    "TypeProbe": str,
    "Location": str,
    "Organization": str,
    "TypeSick": str,
    "VerifSick": str,
    "DateOfCompletion": date
}

# Get data from form and add to dict


def getData(varName: str, browser=BROWSER):
    if varName == 'MKB_Dlg_MobilePhoneNumber':
        tempVar = browser.find_element_by_name(varName).getText()
        for phone in tempVar:

            ph = ""

            for sym in phone:
                if sym not in ['(', ')', '/', '-', '+', '=']:
                    ph = ph + sym
            if len(ph) <= 10:
                ph = "8" + ph
            elif ph[0] == "7":
                ph = "8" + ph[1:]
            else:
                pass

            for sym in tempVar:
                if sym not in ['(', ')', '/', '-', '+', '=']:
                    phone = phone + sym
        return phone
    else:
        return browser.find_element_by_name(varName).getText()


def sendData(varName: str, dataFromBD, browser=BROWSER, ):
    if varName[0:1] != "//":
        browser.find_element_by_name(varName).send_keys(dataFromBD)
    elif varName in ['issue[custom_field_values][57]', 'issue[custom_field_values][375]', 'issue[custom_field_values][377]']:
        Select(browser.find_element_by_name(
            varName)).select_by_value(dataFromBD)
    else:
        browser.find_element_by_xpath(varName).send_keys(dataFromBD)


bd['SNILS'] = getData('MKB_Dlg.SNILS')
bd['Surname'] = getData('MKB_Dlg_Family')
bd['Name'] = getData('MKB_Dlg_Name')
bd['Patronim'] = getData('MKB_Dlg_Patronim')
bd['Phone'] = getData('MKB_Dlg_MobilePhoneNumber')


# TODO@LechDude (проверь эти 3 переменные)
# Добавялем дату рождения

bd['Birthday'] = birthday
bd['Sex'] = sex
bd['Address'] = adress


# Write data to form
sendData('issue[custom_field_values][420]', bd['Surname'])
sendData('issue[custom_field_values][421]', bd['Name'])
sendData('issue[custom_field_values][422]', bd['Patronim'])
sendData('issue[custom_field_values][14]', bd['Birthday'])

if bd['Пол'] == 'Муж':
    sendData('issue[custom_field_values][11]', bd['Sex'][0])
else:
    sendData('issue[custom_field_values][11]', 'Ж')

sendData('issue[custom_field_values][15]', bd['Phone'])
sendData('issue[custom_field_values][424]', 'П')  # DocumentType
sendData('issue[custom_field_values][12]', bd['SNILS'])
sendData('issue[custom_field_values][7]', 'По')  # City
sendData('issue[custom_field_values][16]', bd['Address'])
sendData('issue[custom_field_values][18]', 'пенсионер')  # Job
# Patien Category
sendData('//select[@name="issue[custom_field_values][250]"]', 'О')
sendData("issue[custom_field_values][6]", 'В')

org = sendData('issue[custom_field_values][57]',
               'ГБУЗ МО Подольская областная клиническая больница')

# Дата забора
BROWSER.find_element_by_name('issue[custom_field_values][30]').click()

sendData('issue[custom_field_values][24]', 'Диомидов Данила Павлович')  # Dr.

# Вид пробы (мазок из нологлотки - по умолчанию)
BROWSER.find_element_by_css_selector(
    'input[type="radio"][value="Мазок/отделяемое из носоглотки и ротоглотки"]').click()

# Тип пробы (первичный - по умолчанию)
BROWSER.find_element_by_css_selector(
    'input[type="radio"][value="Первичный"]').click()

# Состояние пацента (удовлетровительно - по умолчанию)
sendData('issue[custom_field_values][373]', 'у')

# Диагноз по МКБ
sendData('issue[custom_field_values][375]', '504')

# Диагноз подтверждён
sendData('issue[custom_field_values][377]', '732')

# Дата забора пробы (текущий день)
current_date = date.today()
current_date = current_date.strftime('%d-%m-%Y')
current_date = current_date.split('-')
current_date = current_date[0]+current_date[1]+current_date[2]

# Передача даты в поле
sendData('issue[custom_field_values][147]', current_date)
