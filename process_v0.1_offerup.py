import pandas as pd


def clean(data):
    """
    purpose to remove not relevant items like xbox, iphone 8 and so on
    :param data: the original dataframe
    :return: new dataframe
    """
    def dealer_title(series):
        series = series.lower()
        key_words = ['iphone x', 'iphonex']
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

    assert isinstance(data, pd.DataFrame)
    info_date = data['Time'].apply(dealer_date)
    info_date = info_date[info_date == -1].index.tolist()
    data = data.drop(axis=0, index=info_date, inplace=False)

    info_tit = data['Title'].apply(dealer_title)
    info_tit = info_tit[info_tit == -1].index.tolist()
    data = data.drop(axis=0, index=info_tit, inplace=False)

    info_pri = data['Price'].apply(dealer_price)
    info_pri = info_pri[info_pri == -1].index.tolist()
    data = data.drop(axis=0, index=info_pri, inplace=False)

    data = data.reset_index(drop=True)
    return data


file = 'old_scrap/IPhoneX_2019-11-21 19:28:16.667516_Result_Offerup.csv'
df = pd.read_csv(file)
df.drop(axis=1, columns='Unnamed: 0', inplace=True)
df = clean(df)
print(df['Time'])