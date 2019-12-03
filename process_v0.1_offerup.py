import pandas as pd
import os
import matplotlib.pyplot as plt


def clean(data, name):
    """
    purpose to remove not relevant items like xbox, iphone 8 and so on
    :param data: the original dataframe
    :return: new dataframe
    """
    def dealer_title(series):
        series = series.lower()
        dic = {
            'IPhone6': 'iphone 6',
            'IPhone6s': 'iphone 6s',
            'IPhone7': 'iphone 7',
            'IPhoneX': 'iphone x',
            'Pixel2': 'pixel 2',
            'Pixel3': 'pixel 3',
            'Pixel4': 'pixel 4',
            'SamsungGalaxyS7': 'samsung galaxy s7',
            'SamsungGalaxyS8': 'samsung galaxy s8',
            'SamsungGalaxyS9': 'samsung galaxy s9'
        }
        key_words = dic[name]
        if series.find(key_words[0]) == -1 and series.find(key_words[-1]) == -1:
            return -1
        return 1

    def dealer_price(series):
        if series == 'Sold!':
            return -1
        return 1

    def dealer_date(series):
        key_words = ['months', 'years', 'year']
        if series.find(key_words[0]) != -1 or series.find(key_words[1]) != -1 or series.find(key_words[2]) != -1:
            return -1
        return 1

    def dealer_cond(series):
        if series == 'For Parts':
            return -1
        return 1
    
    def dealer_description(series):
        series = series.lower()
        key_words = [' lock',' locked']
        if series.find(key_words[0]) != -1 or series.find(key_words[1]) != -1:
            return -1
        return 1

    assert isinstance(data, pd.DataFrame)
    info_date = data['Time'].apply(dealer_date)
    info_date = info_date[info_date == -1].index.tolist()

    info_tit = data['Title'].apply(dealer_title)
    info_tit = info_tit[info_tit == -1].index.tolist()

    info_pri = data['Price'].apply(dealer_price)
    info_pri = info_pri[info_pri == -1].index.tolist()

    info_cond = data['Condition'].apply(dealer_cond)
    info_cond = info_cond[info_cond == -1].index.tolist()
    
    #info_description = data['Description'].apply(dealer_description)
    #info_description = info_description[info_description == -1].index.tolist()

    info = info_date + info_tit + info_pri + info_cond #+ info_description
    info = list(set(info))
    data = data.drop(axis=0, index=info, inplace=False)
    data = data.reset_index(drop=True)
    print('the length of the data is: ',len(data))
    return data


def compare_csv(data_yst, data_td):
    '''
    Comparing two csv file from two consecutive days to get new and sold post
    
    :param yst: yesterday's scraping data
    :type yst: pd.DataFrame
    :param td: today's scraping data
    :type td: pd.DataFrame
    
    :return sold: the number of sold items
    :return new: the number of new items
    '''
    sold = 0
    new = 0
    
    ID_yst = data_yst['Item ID']
    ID_td = data_td['Item ID']
    
    for item in ID_td:
        if item not in ID_yst.values:
            new += 1
        
    for item in ID_yst:
        if item not in ID_td.values:
            sold += 1
        
    return sold, new


def compute_avg(df):
    '''
    Calculate the average price per type of conditions.
    
    :param df: input pandas dataframe for scraping of one day
    :type df: pd.DataFrame
    
    :return: average price for each condition
    '''
    s1 = df['Condition']
    s2 = df['Price'].astype('float32')
    avg = s2.mean()
    max_price = s2.max()
    min_price = s2.min()
    df = pd.concat([s1, s2], axis=1)
    grp = df.groupby(['Condition'])
    composition = s1.value_counts()
    composition.to_csv('composition_of_condition.csv')
    condition_avg = grp.mean()
    condition_avg.to_csv('avg_price_for_conditions.csv')
    return avg, condition_avg, max_price, min_price


def compare_avg(dir_name):
    """
    compare average price of different models in the same dir
    :param dir_name: the dir name
    :return:
    """
    path = dir_name
    files = os.listdir(path)
    res = 0
    for file in files:
        name = file.split('_')[0]
        file = path + '/' + file
        df = pd.read_csv(file, lineterminator='\n')
        df = clean(df, name)
        s2 = df['Price'].astype('float32')
        avg = s2.mean()
        res += avg
    return res/len(files)



"""
file = './B_Offerup_S7/SamsungGalaxyS7_2019-11-30 01:02:59.981149_Result_Offerup.csv'
df = pd.read_csv(file)
df.drop(axis=1, columns='Unnamed: 0', inplace=True)
name_all = file.split('/')[2].split('_')
name = name_all[0]
df = clean(df, name)
avg, conditional_avg, max_price,  min_price = compute_avg(df)
"""
path = './'
files = os.listdir(path)
compare_avg_list = []
for file in files:
    if file.split('_')[0] != 'B':
        continue
    ModelName = file.split('_')[2]
    compare_avg_list.append({"ModelName": ModelName, "AveragePrice":compare_avg(path + file)})
df_compare_avg = pd.DataFrame(compare_avg_list, columns=["ModelName", "AveragePrice"])
df_compare_avg.to_csv("./Compare_AvgPrice_B.csv", index=False)
#print(avg)
#print(max_price)
#print(min_price)
#print(conditional_avg)
#print(df['Title'])