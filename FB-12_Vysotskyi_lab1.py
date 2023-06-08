from datetime import datetime
import urllib.request
import pandas as pd
import os

REGIONS = {1: "Вінницька", 2: "Волинська", 3: "Дніпропетровська", 4: "Донецька", 5: "Житомирська", 6: "Закарпатська",
           7: "Запорізька", 8: "Івано-Франківська", 9: "Київська", 10: "Кіровоградська", 11: "Луганська",
           12: "Львівська", 13: "Миколаївська", 14: "Одеська", 15: "Полтавська", 16: "Рівенська", 17: "Сумська",
           18: "Тернопільська", 19: "Харківська", 20: "Херсонська", 21: "Хмельницька", 22: "Черкаська",
           23: "Чернівецька", 24: "Чернігівська", 25: "Республіка Крим"}


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
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', "empty"]
    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            region_index = int(filename.split("_")[3])
            file_path = os.path.join(directory_path, filename)
            df = pd.read_csv(file_path, header=1, names=headers)
            df = df.drop(df.loc[df['VHI'] == -1].index)
            df['area'] = region_index  # додавання стовбця з індексами регіонів
            df['area'].replace(REGIONS, inplace=True)  # заміна індексів регіонів на нові
            dataframe = pd.concat([dataframe, df])  # додавання даних з поточного файлу до загального фрейму
    dataframe = dataframe.drop('empty', axis=1)
    return dataframe


def get_vhi_for_area_year(area, year):
    df = DATAFRAME[(DATAFRAME["area"] == area) & (DATAFRAME["Year"] == year)]
    vhi_series = df["VHI"]
    print("Ряд VHI для області {} за {} рік:".format(area, year))
    print(vhi_series)
    print("Мінімальне значення VHI:", vhi_series.min(), vhi_series[vhi_series == vhi_series.min()].index[0])
    print("Максимальне значення VHI:", vhi_series.max(), vhi_series[vhi_series == vhi_series.max()].index[0])


def find_extreme_drought_years(region, percentage):
    region_data = DATAFRAME[DATAFRAME["area"] == region]
    years = region_data["Year"].unique()
    extreme_drought_years = []
    for year in years:
        year_data = region_data[region_data["Year"] == year]
        affected_area_percentage = (year_data["VHI"] <= 15).mean() * 100
        if affected_area_percentage >= percentage:
            extreme_drought_years.append(year)
    print("Роки з екстремальними посухами, в регіоні {}, які торкнулись не менше {} відсотків області: ".format(region, percentage), extreme_drought_years)


def find_moderate_drought_years(region, percentage):
    region_data = DATAFRAME[DATAFRAME["area"] == region]
    years = region_data["Year"].unique()
    moderate_drought_years = []
    for year in years:
        year_data = region_data[region_data["Year"] == year]
        affected_area_percentage = ((year_data["VHI"] > 15) & (year_data["VHI"] <= 35)).mean() * 100
        if affected_area_percentage >= percentage:
            moderate_drought_years.append(year)
    print("Роки з помірними посухами, в регіоні {}, які торкнулись не менше {} відсотків області: ".format(region, percentage), moderate_drought_years)


if __name__ == "__main__":
    DATAFRAME = pd.DataFrame()
    download_files()
    DATAFRAME = read_files_to_dataframe(r"D:\Studying\AD", DATAFRAME)
    get_vhi_for_area_year("Одеська", "2002")
    find_extreme_drought_years("Одеська", 30)
    find_moderate_drought_years("Одеська", 30)
    print(DATAFRAME)
