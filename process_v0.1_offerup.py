import pandas as pd
import matplotlib.pyplot as plt


def clean(data):
    """
    purpose to remove not relevant items like xbox, iphone 8 and so on
    :param data: the original dataframe
    :return: new dataframe
    """
    def dealer_title(series):
        series = series.lower()
        key_words = ['iphone x', 'iphonex']
        ban_words = ['case', 'cases', 'trade']
        if series.find(key_words[0]) == -1 and series.find(key_words[-1]) == -1:
            return -1
        if series.find(ban_words[0]) != -1 or series.find(ban_words[1]) != -1 or series.find(ban_words[2]) != -1:
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



file = './IPhoneX_2019-11-29 23:55:05.938343_Result_Offerup.csv'
df = pd.read_csv(file)
df.drop(axis=1, columns='Unnamed: 0', inplace=True)
df = clean(df)
avg, conditional_avg, max_price, min_price = compute_avg(df)
print(avg)
print(max_price)
print(min_price)
print(conditional_avg)
#print(df['Title'])
