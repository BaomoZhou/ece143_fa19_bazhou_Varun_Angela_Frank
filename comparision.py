def compare_csv(yst,td):
    '''
    
    :param yst: address of yesterday's csv
    :type yst: str
    :param td: address of today's csv
    :type td: str
    '''
    
    sold_id = []
    new_id = []
    same_id = []
    
    data_yst = pd.read_csv(yst)
    data_td = pd.read_csv(td)
    
    ID_yst = data_yst['Item ID']
    ID_td = data_td['Item ID']
    
    for item in ID_td:
        if item not in ID_yst.values:
            new_id.append(item)
        else:
            same_id.append(item)
        
    for item in ID_yst:
        if item not in ID_td.values:
            sold_id.append(item)
        
    return sold_id,new_id,same_id