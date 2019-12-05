import pandas as pd
import os
import math
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
        ban_words = ['case', 'cases']
        key_words = dic[name]
        if series.find(key_words) == -1 or series.find(ban_words[0]) != -1 or series.find(ban_words[-1]) != -1:
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
    #print('the length of the data is: ',len(data))
    return len(info_tit)+len(info_pri)+len(info_cond), data


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
        x, df = clean(df, name)
        s2 = df['Price'].astype('float32')
        avg = s2.mean()
        res += avg
    return round(res/len(files), 2)


def compare_newly_post(dir_name):
    """
    compare average price of different models in the same dir
    :param dir_name: the dir name
    :return:
    """
    path = dir_name
    files = os.listdir(path)
    res = 0
    files.sort()
    if len(files) == 0 or len(files) == 1:
        return 0
    for i in range(len(files) - 1):
        name_1 = files[i].split('_')[0]
        file_1 = path + '/' + files[i]
        df_1 = pd.read_csv(file_1, lineterminator='\n')
        x, df_1 = clean(df_1, name_1)

        name_2 = files[i+1].split('_')[0]
        file_2 = path + '/' + files[i+1]
        df_2 = pd.read_csv(file_2, lineterminator='\n')
        x, df_2 = clean(df_2, name_2)

        sold, new = compare_csv(df_1, df_2)
        res += new
    return math.ceil(res/(len(files) - 1))


def condition_handler_A(composition_list, condition_avg_list):
    """
    To add information of conditions
    :param condition_list: the container of dataframes
    :return: two dataframws after dealing
    """
    df_com = composition_list[0]
    df_con = condition_avg_list[0]
    for i in range(1, len(composition_list)):
        df_com = df_com.add(composition_list[i], fill_value=0)
    df_com = df_com/len(composition_list)
    count = 0
    for i in range(1, len(condition_avg_list)):
        df_con = df_con.add(condition_avg_list[i], fill_value=0)
        if len(condition_avg_list[i]) == 5:
            count += 1
    df_con = df_con / len(condition_avg_list)
    df_con.loc['Other (see description)', 'Price'] = df_con.loc['Other (see description)', 'Price'] * len(condition_avg_list) / count
    df_com = df_com.rename_axis("Number")
    list(df_con['Price'])
    list(df_com)
    return list(df_com),  list(df_con['Price'])


def distance(dt):
    under_ten = len(dt[(dt['Distance'] < 10)])
    ten_to_fifty = len(dt[(dt['Distance'] < 50)]) - under_ten
    fifty_above = len(dt[(dt['Distance'] >= 50)])
    return [under_ten, ten_to_fifty, fifty_above]

def csv_process_A(dir_name, ModelName):
    """
    compare average price and newly posted numbers of different models in the same dir
    :param dir_name:
    :return:
    """
    Date_dic = {0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'}
    path = dir_name
    files = os.listdir(path)
    files.sort()
    avg_per_day_list = []
    newly_per_day_list = []
    avg_per_week_list = []
    compostion_list = []
    condition_avg_list = []
    avg_per_week = 0
    avg_ratio_useful = 0
    under_ten, ten_to_fifty, fifty_above = 0, 0, 0
    for i, file in enumerate(files):
        if i == 0:
            continue
        name = file.split('_')[0]
        file = path + '/' + file
        df = pd.read_csv(file, lineterminator='\n')
        len_before = len(df)
        len_useless, df = clean(df, name)
        avg_ratio_useful += (len_before - len_useless)/len_before
        s_cond = df['Condition']
        s_pri = df['Price'].astype('float32')
        under_ten += distance(df)[0]
        ten_to_fifty += distance(df)[1]
        fifty_above += distance(df)[2]
        df_temp = pd.concat([s_cond, s_pri], axis=1)
        grp = df_temp.groupby(['Condition'])
        composition = s_cond.value_counts()
        #print(composition, name)
        condition_avg = grp.mean()
        #print(condition_avg)
        avg_per_day = s_pri.mean()
        avg_per_day_list.append({"Date": Date_dic[i-1],
                                 "AveragePrice": avg_per_day})
        compostion_list.append(composition)
        condition_avg_list.append(condition_avg)
        avg_per_week += avg_per_day

        if i < len(files) - 1:
            name_ = files[i+1].split('_')[0]
            file_ = path + '/' + files[i+1]
            df_ = pd.read_csv(file_, lineterminator='\n')
            nothing, df_ = clean(df_, name_)
            sold, new = compare_csv(df, df_)
            newly_per_day_list.append(new)

    df_compostion, df_condition_avg = condition_handler_A(compostion_list, condition_avg_list)
    avg_per_week = round(avg_per_week/(len(files) - 1),2)
    avg_per_week_list.append({"ModelName": ModelName, "AveragePricePerWeek": avg_per_week})
    df_avg_per_week = pd.DataFrame(avg_per_week_list, columns=["ModelName", "AveragePricePerWeek"])
    df_avg_per_week.to_csv("./AvgPrice_per_week_A_" + ModelName + ".csv", index=False)

    df_avg_per_day = pd.DataFrame(avg_per_day_list, columns=["Date", "AveragePrice"])
    df_avg_per_day.to_csv("./AvgPrice_per_day_A_" + ModelName + ".csv", index=False)
    df_compostion.to_csv("./Composition_condition_A_" + ModelName + ".csv", index=False)
    df_condition_avg.to_csv("./AvgPrice_condition_A_" + ModelName + ".csv", index=False)
    avg_ratio_useful = avg_ratio_useful/(len(files) - 1)
    return avg_ratio_useful, newly_per_day_list, (under_ten, ten_to_fifty, fifty_above), avg_per_week, \
           (df_compostion, df_condition_avg)
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
    if file.split('_')[0] == 'A':
        ModelName = file.split('_')[2]
        csv_process_A(path + file, ModelName)
    elif file.split('_')[0] == 'B':
        ModelName = file.split('_')[2]
        compare_avg_list.append({"ModelName": ModelName,
                                 "AveragePrice": compare_avg(path + file),
                                 "NewlyPostNum": compare_newly_post(path + file)})
df_compare_avg = pd.DataFrame(compare_avg_list, columns=["ModelName", "AveragePrice", "NewlyPostNum"])
df_compare_avg.to_csv("./Compare_AvgPrice+NewlyPostNum_B.csv", index=False)

#print(avg)
#print(max_price)
#print(min_price)
#print(conditional_avg)
#print(df['Title'])