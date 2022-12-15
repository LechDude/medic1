#!/usr/bin/env python
# coding: utf-8

# # Технический блок

# In[3]:


get_ipython().system('pip install bs4')


# In[62]:


from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import datetime
from datetime import date


# In[5]:


browser = Chrome('/Users/ddiom/chromedriver')
url = 'https://covid.rm.mosreg.ru/issues/new?tracker_id=29'
browser.get(url)


# # Блок получения данных

# In[ ]:


bd = dict()
#Получаем и добавляем в бд СНИЛС
snils = browser.find_element_by_name('MKB_Dlg.SNILS')
bd['СНИЛС']= snils.getText()

#Получаем и добавляем в бд Фамилию
emias_surname = browser.find_element_by_name('MKB_Dlg_Family')
bd['Фамилия'] = emias_surname.getText()

#Получаем и добавляем в бд Имя
emias_name = browser.find_element_by_name('MKB_Dlg_Name')
bd['Имя'] = emias_surname.getText()

#Получаем и добавляем в бд Отчество
emias_patronim = browser.find_element_by_name('MKB_Dlg_Patronim')
bd['Отчество'] = emias_patronim.getText()

#Получаем номер телефона
emias_number = browser.find_element_by_name('MKB_Dlg_MobilePhoneNumber')
emias_number = emias_patronim.getText()

#Преобразуем в формат для формы
number = '8'+ emias_number
number = number.split('-')
number = number[0] + number[1] + number[2] + number[3]

#Добавляем номер в БД
bd['Номер'] = number

#Добавялем дату рождения

bd['Дата рождения'] = birthday
#Добавляем пол

bd['Пол'] = sex
#Добавляем адрес

bd['Адрес'] = adress

print(bd)


# In[75]:





# # Блок заполнения формы

# In[9]:


#Фамилия
surname_form = browser.find_element_by_name('issue[custom_field_values][420]')
surname.send_keys(bd['Фамилия'])


# In[11]:


#Имя
name_form = browser.find_element_by_name('issue[custom_field_values][421]')
name.send_keys(bd['Имя'])


# In[13]:


#Отчество
patronim_form = browser.find_element_by_name('issue[custom_field_values][422]')
patronim_form.send_keys(bd['Отчество'])


# In[15]:


#Рождение
birthday_form = browser.find_element_by_name('issue[custom_field_values][14]')
birthday_form.send_keys(bd['Дата рождения'])


# In[17]:


#Пол
sex_form = browser.find_element_by_name('issue[custom_field_values][11]')
if bd['Пол'] = 'Муж':
    sex_form.send_keys('М')
else:
    sex_form.send_keys('Ж')


# In[19]:


#Номер телефона
phone_number = browser.find_element_by_name('issue[custom_field_values][15]')
phone_number.send_keys(bd['Номер'])


# In[21]:


#Паспорт
passport =  browser.find_element_by_name('issue[custom_field_values][424]')
passport.send_keys('П')


# In[23]:


#ОМС - но надо будет заменить на СНИЛС
snils_form = browser.find_element_by_name('issue[custom_field_values][12]')
snils_form.send_keys(bd['СНИЛС'])


# In[25]:


#Город
city = browser.find_element_by_name('issue[custom_field_values][7]')
city.send_keys('По')


# In[27]:


#Адрес
adress_form = browser.find_element_by_name('issue[custom_field_values][16]')
adress_form.send_keys(bd['Адрес'])


# In[29]:


#Место работы
job = browser.find_element_by_name('issue[custom_field_values][18]')
job.send_keys('пенсионер')


# In[31]:


#Категория пациента
type_of_patient = browser.find_element_by_xpath('//select[@name="issue[custom_field_values][250]"]')
type_of_patient.send_keys('О')


# In[33]:


#Место забора мазка (по умолчанию - в поликлинике)
place = browser.find_element_by_name("issue[custom_field_values][6]")
place.send_keys('В')


# In[35]:


#Организация забора мазка
org = browser.find_element_by_name('issue[custom_field_values][57]')
dd = Select(org)
dd.select_by_value('ГБУЗ МО Подольская областная клиническая больница')


# In[70]:


#Дата забора

#date = datetime.datetime.now()

date_of_take = browser.find_element_by_name('issue[custom_field_values][30]')
date_of_take.click()
#date_of_take.clear()
#leep(1)
#ate_of_take.send_keys(date.strftime('%Y-%m-%d %H-%M'))


# In[71]:


#ФИО врача
doctor = browser.find_element_by_name('issue[custom_field_values][24]')
doctor.send_keys('Диомидов Данила Павлович')


# In[38]:


#Вид пробы (мазок из нологлотки - по умолчанию)
kind_of_proba = browser.find_element_by_css_selector('input[type="radio"][value="Мазок/отделяемое из носоглотки и ротоглотки"]')
kind_of_proba.click()


# In[39]:


#Тип пробы (первичный - по умолчанию)
type_of_proba = browser.find_element_by_css_selector('input[type="radio"][value="Первичный"]')
type_of_proba.click()


# In[41]:


#Состояние пацента (удовлетровительно - по умолчанию)
current = browser.find_element_by_name('issue[custom_field_values][373]')
current.send_keys('у')


# In[43]:


#Диагноз по МКБ
sick = browser.find_element_by_name('issue[custom_field_values][375]')
sick_dd = Select(sick)
sick_dd.select_by_value('504')


# In[44]:


#Диагноз подтверждён
verif = browser.find_element_by_name('issue[custom_field_values][377]')
verif_dd = Select(verif)
verif_dd.select_by_value('732')


# In[45]:


# Дата забора пробы (текущий день)
current_date = date.today()
current_date = current_date.strftime('%d-%m-%Y')
current_date = current_date.split('-')
current_date = current_date[0]+current_date[1]+current_date[2]
print(current_date)
#Передача даты в поле
current = browser.find_element_by_name('issue[custom_field_values][147]')
current.send_keys('14122022')


# In[73]:


x = {}
x['СНИЛС'] = '134-124-123 04'
a = '88005553535'
x['Номер'] = a
print(x)


# In[ ]:




