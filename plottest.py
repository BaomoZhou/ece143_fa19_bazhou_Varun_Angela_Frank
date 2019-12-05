import matplotlib.pyplot as plt
import pandas as pd

def draw_avg_price_bar(model_name,filepath):
    '''
    this function will draw the bar graph for the average price of each
    cellphone model on each website
    
    :param filepath: the path pointed to the csv file
    :type filepath: str
    :param model_name: the name of the phone model
    :type model_name: str
        
    :return: a bar chart that compares the average price
    '''
    
    assert(isinstance(model_name,str)),'the model name should be of type string'
    assert(isinstance(filepath,str)),'the input filepath should be of type string'
    price_data = pd.read_csv(filepath)
    my_colors = ['#4a7c59','#64a1f4']
    ax1 = price_data.plot(title='Average Price of '+model_name+' on Both Websites',x=model_name+' Model',kind='bar',rot=1,color=my_colors)
    ax1.set_ylabel('Average Price in $')
    
def draw_new_post_bar(model_name,filepath):
    '''
    this function will draw the bar graph for the average number 
    of new post everyday for each cellphone model on each website
    
    :param filepath: the path pointed to the csv file
    :type filepath: str
    :param model_name: the name of the phone model
    :type model_name: str
        
    :return: a bar chart that compares the number of new post
    '''
    
    assert(isinstance(model_name,str)),'the model name should be of type string'
    assert(isinstance(filepath,str)),'the input filepath should be of type string'
    post_data = pd.read_csv(filepath)
    my_colors = ['#4a7c59','#64a1f4']
    ax1 = post_data.plot(title='New Post of '+model_name+' on Both Websites',x=model_name+' Model',kind='bar',rot=1,color=my_colors)
    ax1.set_ylabel('Number of New Post')
    #ax1.set(ylim=[20,130])
    
    
def draw_avg_price_line(filepath):
    '''
    this function will draw the line graph which includes prices from a 7-day data
    
    :param filepath: the path pointed to the csv file
    :type filepath: str
    
    :return: a line chart that tracks the change of price through a week
    '''
    
    assert(isinstance(filepath,str)),'the input filepath should be of type string'
    price_data = pd.read_csv(filepath)
    my_colors = ['#4a7c59','#64a1f4']
    ax1 = price_data.plot(title='Average Price for IPhone on Both Websites',x='Date',kind='line',rot=1,linestyle='-',marker='o',color=my_colors)
    ax1.set_ylabel('Average Price in $')
    
    


filepath = './test.csv'
filepath1 = './test2.csv'
filepath2 = './test3.csv'
model_name = 'IPhone'
draw_avg_price_bar(model_name,filepath)
draw_new_post_bar(model_name,filepath1)
draw_avg_price_line(filepath2)