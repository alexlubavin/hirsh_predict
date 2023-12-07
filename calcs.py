import pandas as pd
import numpy as np

import streamlit as st
from streamlit.logger import get_logger

model_df = pd.read_excel('data.xlsx')

import pickle




# Loading models

with open('rinc_model.pickle', 'rb') as f:
  rinc_model = pickle.load(f)
  
with open('scopus_model.pickle', 'rb') as f:
  scopus_model = pickle.load(f)

with open('wos_model.pickle', 'rb') as f:
  wos_model = pickle.load(f)
  



# Columns

# 0   Ф.И.О.                                                       248 non-null    object 
#  1   Возраст                                                      248 non-null    int64  
#  2   Пол                                                          248 non-null    int64  
#  3   Стаж в НМИЦ ТПМ                                              248 non-null    int64  
#  4   Должность НМИЦ ТПМ                                           248 non-null    int64  
#  5   Хирш-РИНЦ                                                    248 non-null    int64  
#  6   Хирш-SCOPUS                                                  248 non-null    int64  
#  7   Хирш-WOS                                                     248 non-null    int64  
#  8   Текущий рейтинг НМИЦ ТПМ (баллы)                             248 non-null    float64
#  9   Ученая степень                                               248 non-null    int64  
#  10  Опубликованные статьи WOS-SCOPUS за последние 5 лет: да/нет  248 non-null    int64  
#  11  Число статей в зарубежных журналах за текущий год            248 non-null    int64  
#  12  Число статей в российских журналах за текущий год            248 non-null    int64  
#  13  Число статей в зарубежных журналах за последние 5 лет        248 non-null    int64  
#  14  Число статей в российских журналах за последние 5 лет        248 non-null    int64  
#  15  Хирш-РИНЦ истиный                                            248 non-null    int64  
#  16  Хирш-SCOPUS истинный                                         248 non-null    int64  
#  17  Хирш-WOS истинный                                            248 non-null    int64  

LOGGER = get_logger(__name__)
def run():
    st.set_page_config(
        page_title="Индекс Хирша",
        page_icon="https://gnicpm.ru/wp-content/themes/gnicpm/img/favicon.ico"
    )
    
    st.image('https://gnicpm.ru/wp-content/themes/gnicpm/img/logo-ru.png',
             caption=None, 
             width=75, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
    
    st.write(" # Прогнозирование индекса Хирша")
    st.subheader(""" при помощи интегрированной нейронной сети """)
    
    name = st.sidebar.selectbox(
    "Выберите сотрудника",
    (model_df['Ф.И.О.']))
    
    imployer_data = model_df.loc[model_df['Ф.И.О.'] == name]
    
    sidebar_data = imployer_data[['Возраст', 
                                  'Стаж в НМИЦ ТПМ', 
                                  'Хирш-РИНЦ', 
                                  'Хирш-SCOPUS', 
                                  'Хирш-WOS', 
                                  ]]
    
    st.sidebar.write(sidebar_data.T)
    
    
    
    # Default_values
    
    
    sex_dflt = int(imployer_data['Пол'])
    
    age_dflt = float(imployer_data['Возраст'])
    
    scy_dflt = int(imployer_data['Ученая степень'])
    
    status_dflt = int(imployer_data['Должность НМИЦ ТПМ'])
    
    stage_dflt = float(imployer_data['Стаж в НМИЦ ТПМ'])
    
    rinz_dflt = float(imployer_data['Хирш-РИНЦ'])
    
    scopus_dflt = float(imployer_data['Хирш-SCOPUS'])
    
    wos_dflt = float(imployer_data['Хирш-WOS'])
    
    score_dflt = float(imployer_data['Текущий рейтинг НМИЦ ТПМ (баллы)'])
    
    articles_dflt = int(imployer_data['Опубликованные статьи WOS-SCOPUS за последние 5 лет: да/нет'])
    
    curent_year_articles_for_dflt = float(imployer_data['Число статей в зарубежных журналах за текущий год'])
    
    curent_year_articles_rus_dflt = float(imployer_data['Число статей в российских журналах за текущий год'])
        
    curent_year_articles_for_5_dflt = float(imployer_data['Число статей в зарубежных журналах за последние 5 лет'])
    
    curent_year_articles_rus_5_dflt = float(imployer_data['Число статей в российских журналах за последние 5 лет'])

        
    # Fool_defense
    
    rinz_dflt = float(imployer_data['Хирш-РИНЦ'])
    scopus_dflt = float(imployer_data['Хирш-SCOPUS'])
    wos_dflt = float(imployer_data['Хирш-WOS'])
    
    
    hide_slider = True
    
    if name == '_':
        hide_slider = False
    
        
    # Title_header
    
    title = imployer_data['Ф.И.О.'].tolist()
    title = title[0]
    
    st.subheader(" ")
    st.subheader(title)
    
    
    # TEST !!!!!!!!
    
    #st.subheader(type(name))
    
    
    # Variabels
    
    st.subheader(" ")
    sex_radio = st.radio('Пол', ['Женский', 'Мужской'], index=sex_dflt)    
    if sex_radio == 'Мужской':
        sex = 1.0
    else:
        sex = 0.0
        
        
    
    age = st.slider('Возраст, лет', min_value=18.0, max_value=90.0, value=age_dflt, step=1.0, 
                   format=None, key=None, help='Введите текущий возраст сотрудника ', 
                   on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
    
    
    st.subheader(" Текущий статус сотрудника ")
    




    scy_radio = st.radio('Ученая степень', ['Нет', 'Кандидат наук', 'Доктор наук'], index=scy_dflt)
    if scy_radio == 'Нет':
        scy = 0.0
    elif scy_radio == 'Кандидат наук':
        scy = 1.0
    elif scy_radio == 'Доктор наук':
        scy = 2.0
    else:
        scy = 3.0
        


    
    status_radio = st.radio('Должность в НМИЦ ТПМ', ['Младший научный сотрудник', 
                                            'Научный сотрудник', 
                                            'Старший научный сотрудник',
                                            'Ведущий научный сотрудник',
                                            'Руководитель лаборатории',
                                            'Руководитель отела и выше'], index=status_dflt)
    
    if status_radio == 'Младший научный сотрудник':
        status = 0.0
    elif status_radio == 'Научный сотрудник':
        status = 1.0
    elif status_radio == 'Старший научный сотрудник':
        status = 2.0
    elif status_radio == 'Ведущий научный сотрудник':
        status = 3.0
    elif status_radio == 'Руководитель лаборатории':
        status = 4.0
    else:
        status = 2.0
        


    
    stage = st.slider('Стаж в НМИЦ ТПМ, лет', min_value=0.0, max_value=70.0, value=stage_dflt, step=1.0, 
                   format=None, key=None, help='Введите стаж сотрудника в НМИЦ ТПМ ', 
                   on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
    
    age_dflt = age_dflt - stage_dflt + stage
    
    
    rinz = st.slider('Хирш-РИНЦ', min_value=0.0, max_value=50.0, value=rinz_dflt, step=1.0, 
                   format=None, key=None, help='Введите текущий индекс Хирша РИНЦ ', 
                   on_change=None, args=None, kwargs=None, disabled=hide_slider, label_visibility="visible")
    
    
    scopus = st.slider('Хирш-SCOPUS', min_value=0.0, max_value=50.0, value=scopus_dflt, step=1.0, 
                   format=None, key=None, help='Введите текущий индекс Хирша SCOPUS ', 
                   on_change=None, args=None, kwargs=None, disabled=hide_slider, label_visibility="visible")
    
    
    wos = st.slider('Хирш-WOS', min_value=0.0, max_value=50.0, value=wos_dflt, step=1.0, 
                   format=None, key=None, help='Введите текущий индекс Хирша WOS ', 
                   on_change=None, args=None, kwargs=None, disabled=hide_slider, label_visibility="visible")
    
    
    score = st.slider('Рейтинг НМИЦ ТПМ, баллы', min_value=0.0, max_value=150.0, value=score_dflt, step=1.0, 
                   format=None, key=None, help='Введите текущий рейтинг в НМИЦ ТПМ ', 
                   on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
    
    
    st.subheader(" ")
    st.subheader(" Результаты научной деятельности ")
       
        
    articles = st.checkbox('Публикации WoS или Scopus за 5 лет', 
                                value=articles_dflt, 
                                key=None, 
                                help='Минимум одна публикация в изданиях WoS или Scopus за последние 5 лет', 
                                on_change=None, disabled=False, label_visibility="visible")
    
    
    curent_year_articles_for = st.slider('Статей в иностранных журналах за текущий год', min_value=0.0, max_value=20.0, value=curent_year_articles_for_dflt, step=1.0, 
                   format=None, key=None, help='Количество опубликованных статей в зарубежных журналах в течение последнего года ', 
                   on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
    
    
    curent_year_articles_rus = st.slider('Статей в российских журналах за текущий год', min_value=0.0, max_value=20.0, value=curent_year_articles_rus_dflt, step=1.0, 
                   format=None, key=None, help='Количество опубликованных статей в российских журналах в течение последнего года ', 
                   on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
    
    
    curent_year_articles_for_5 = st.slider('Статей в иностранных журналах за последние 5 лет', min_value=0.0, max_value=100.0, value=(curent_year_articles_for_5_dflt - curent_year_articles_for_dflt + curent_year_articles_for), 
                                                                                                                                     step=1.0, 
                   format=None, key=None, help='Количество опубликованных статей в зарубежных журналах в течение последних 5 лет ', 
                   on_change=None, args=None, kwargs=None, disabled=hide_slider, label_visibility="visible")
    
    
    curent_year_articles_rus_5 = st.slider('Статей в российских журналах за последние 5 лет',
                                           min_value=0.0, max_value=100.0, value=(curent_year_articles_rus_5_dflt - curent_year_articles_rus_dflt + curent_year_articles_rus), 
                                           step=1.0, 
                   format=None, key=None, help='Количество опубликованных статей в российских журналах в течение последних 5 лет ', 
                   on_change=None, args=None, kwargs=None, disabled=hide_slider, label_visibility="visible")
    

# Getting data to predict

    data = [age, 
            sex, 
            stage,
            status,
            rinz, 
            scopus, 
            wos, 
            score, 
            scy, 
            articles, 
            curent_year_articles_for, 
            curent_year_articles_rus, 
            curent_year_articles_for_5, 
            curent_year_articles_rus_5]
    
    data = pd.DataFrame(data)
    X = data.T
    

# Getting predict

    hirsh_rinc_predict = rinc_model.predict(X).round(0)
    hirsh_scopus_predict = scopus_model.predict(X).round(0)
    hirsh_wos_predict = wos_model.predict(X).round(0)
    
    
    
# Report   


    rinz_report = int(hirsh_rinc_predict)
    scopus_report = int(hirsh_scopus_predict)
    wos_report = int(hirsh_wos_predict)
    
    if int(hirsh_rinc_predict) < int(rinz_dflt):
        rinz_report = int(rinz_dflt)
    
    if int(hirsh_scopus_predict) < int(scopus_dflt):
        scopus_report = int(scopus_dflt)
        
    if int(hirsh_wos_predict) < int(wos_dflt):
        wos_report = int(wos_dflt)
    
    

    st.subheader(" ")
    st.subheader(" ")
    st.subheader(" ")
    
    st.subheader(" Пятилетний прогноз нейронной сети: ")
    
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header(rinz_report)
        st.write('Прогнозируемый через 5 лет индекс Хирша РИНЦ')

    with col2:
        st.header(scopus_report)
        st.write('Прогнозируемый через 5 лет индекс Хирша Scopus')

    with col3:
        st.header(wos_report)
        st.write('Прогнозируемый через 5 лет индекс Хирша WoS')

    
    st.subheader(" ")    
    st.subheader(" ")    
    st.subheader(" ")    
    st.subheader(" ")
    st.subheader(" ")
    st.subheader(" ")    
    
    st.markdown(""" Реализация идеи: научный сотрудник НМИЦ ТПМ А. В. Любавин +7-915-857-88-65 """)
    
if __name__ == "__main__":
    run()
