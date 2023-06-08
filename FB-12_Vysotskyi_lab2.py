import matplotlib.pyplot as plt
from datetime import datetime
from spyre.spyre import server
import urllib.request
import pandas as pd
import os

REGIONS = {1: "Вінницька", 2: "Волинська", 3: "Дніпропетровська", 4: "Донецька", 5: "Житомирська", 6: "Закарпатська",
           7: "Запорізька", 8: "Івано-Франківська", 9: "Київська", 10: "Кіровоградська", 11: "Луганська",
           12: "Львівська", 13: "Миколаївська", 14: "Одеська", 15: "Полтавська", 16: "Рівенська", 17: "Сумська",
           18: "Тернопільська", 19: "Харківська", 20: "Херсонська", 21: "Хмельницька", 22: "Черкаська",
           23: "Чернівецька", 24: "Чернігівська", 25: "Республіка Крим"}


DATAFRAME = pd.DataFrame()


def download_files():
    for i in range(1, 26):
        url='https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={}&year1=1981&year2=2020&type=Mean'.format(i)
        wp = urllib.request.urlopen(url)
        text = wp.read()

        now = datetime.now()
        date_and_time_time = now.strftime("%d%m%Y%H%M%S")

        with open(f'NOAA_ID_region_{i}_{date_and_time_time}.csv', 'wb') as csv_file:
            csv_file.write(text)


def read_files_to_dataframe(directory_path, dataframe):
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            region_index = int(filename.split("_")[3])
            file_path = os.path.join(directory_path, filename)
            df = pd.read_csv(file_path, header=1, names=headers)
            df = df.drop(df.loc[df['VHI'] == -1].index)
            df['area'] = region_index  # додавання стовбця з індексами регіонів
            df['area'].replace(REGIONS, inplace=True)  # заміна індексів регіонів на нові
            dataframe = pd.concat([dataframe, df])  # додавання даних з поточного файлу до загального фрейму
    # dataframe = dataframe.drop('empty', axis=1)
    return dataframe


class MyWebApp(server.App):
    title = "NOAA Data Visualization"

    inputs = [
        {
            "type": 'dropdown',
            "label": 'Вибір параметра для аналізу',
            "options": [
                {"label": "VCI", "value": "VCI"},
                {"label": "TCI", "value": "TCI"},
                {"label": "VHI", "value": "VHI"}],
            "key": 'ticker',
            "action_id": "update_data"
        },
        {
            "type": 'dropdown',
            "label": 'Область',
            "options": [
                {"label": "Вінницька", "value": 1},
                {"label": "Волинська", "value": 2},
                {"label": "Дніпропетровська", "value": 3},
                {"label": "Донецька", "value": 4},
                {"label": "Житомирська", "value": 5},
                {"label": "Закарпатська", "value": 6},
                {"label": "Запорізька", "value": 7},
                {"label": "Івано-Франківська", "value": 8},
                {"label": "Київська", "value": 9},
                {"label": "Кіровоградська", "value": 10},
                {"label": "Луганська", "value": 11},
                {"label": "Львівська", "value": 12},
                {"label": "Миколаївська", "value": 13},
                {"label": "Одеська", "value": 14},
                {"label": "Полтавська", "value": 15},
                {"label": "Рівненська", "value": 16},
                {"label": "Сумська", "value": 17},
                {"label": "Тернопільська", "value": 18},
                {"label": "Харківська", "value": 19},
                {"label": "Херсонська", "value": 20},
                {"label": "Хмельницька", "value": 21},
                {"label": "Черкаська", "value": 22},
                {"label": "Чернівецька", "value": 23},
                {"label": "Чернігівська", "value": 24},
                {"label": "Республіка Крим", "value": 25}
            ],
            "key": 'region',
            "action_id": "update_data"
        },
        # Текстове поле для введення інтервалу тижнів
        {
            "type": 'dropdown',
            "label": 'Рік',
            "options": list([{"label": str(i), "value": i} for i in range(1982, 2021)]),
            "key": 'year',
            "action_id": "update_data"
        }


    ]

    controls = [{"type": "hidden", "id": "update_data"}]

    outputs = [
        {
            "type": "plot",
            "id": "plot",
            "control_id": "update_data",
            "tab": "Plot"
        },
        {
            "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True
        }
    ]

    def getHTML(self, params):
        range = params['range']
        return range

    def getData(self, params):
        region = params['region']
        year = params['year']
        dict = {
                1: "Вінницька",
                2: "Волинська",
                3: "Дніпропетровська",
                4: "Донецька",
                5: "Житомирська",
                6: "Закарпатська",
                7: "Запорізька",
                8: "Івано-Франківська",
                9: "Київська",
                10: "Кіровоградська",
                11: "Луганська",
                12: "Львівська",
                13: "Миколаївська",
                14: "Одеська",
                15: "Полтавська",
                16: "Рівенська",
                17: "Сумська",
                18: "Тернопільська",
                19: "Харківська",
                20: "Херсонська",
                21: "Хмельницька",
                22: "Черкаська",
                23: "Чернівецька",
                24: "Чернігівська",
                25: "Республіка Крим"
            }
        region = dict.get(int(region), "Помилка")


        print(DATAFRAME)
        return DATAFRAME[(DATAFRAME["area"] == region) & (DATAFRAME["Year"] == year)]

    def getPlot(self, params):
        ticker = params['ticker']

        df = self.getData(params)
        plt_obj = df.plot(x='Week', y=ticker, legend=False)
        plt_obj.set_ylabel(ticker)
        plt_obj.set_xlabel("Week")
        plt_obj.figure.savefig('plot.png')
        plt.close()

        return plt_obj


read_files_to_dataframe(r"D:\Studying\AD", DATAFRAME)


if __name__ == "__main__":
    download_files()
    DATAFRAME = read_files_to_dataframe(r"D:\Studying\AD", DATAFRAME)
    print(DATAFRAME)
    app = MyWebApp()
    app.launch(port=9093)
