import matplotlib.pyplot as plt
import pandas as pd

def draw_avg_price_bar(model_name,filepath,filename,ylimit=None):
    '''
    this function will draw the bar graph for the average price of each
    cellphone model on each website
    
    :param filepath: the path pointed to the csv file
    :type filepath: str
    :param model_name: the name of the phone model
    :type model_name: str
    :param ylimit: this is the range limit of y axis
    :type ylimit: list
    :param filename: this is the saved figure's filename
    :type filename: str
        
    :return: a bar chart that compares the average price
    '''
    
    assert(isinstance(model_name,str)),'the model name should be of type string'
    assert(isinstance(filepath,str)),'the input filepath should be of type string'
    assert (isinstance(ylimit, list) or ylimit is None),'the input of ylimit should be of type list'
    assert (isinstance(filename, str)), 'the file name should be of type string'

    price_data = pd.read_csv(filepath)
    price_data.drop(axis=1, columns='Unnamed: 0', inplace=True)
    my_colors = ['#800080', '#017270']
    plt.figure()
    price_data.plot(x=model_name+'Model',kind='bar',rot=1,color=my_colors)
    plt.ylabel('Price {$}')
    plt.xlabel('')
    plt.title(model_name,fontdict = {'fontsize' : 25},pad=16)
    if ylimit is not None:
        plt.ylim(ylimit[0], ylimit[1])
    plt.savefig(filename,dpi=300)
    plt.show()

    
def draw_new_post_bar(model_name,filepath,filename,ylimit=None):
    '''
    this function will draw the bar graph for the average number 
    of new post everyday for each cellphone model on each website
    
    :param filepath: the path pointed to the csv file
    :type filepath: str
    :param model_name: the name of the phone model
    :type model_name: str
    :param ylimit: this is the range limit of y axis
    :type ylimit: list
    :param filename: this is the saved figure's filename
    :type filename: str
        
    :return: a bar chart that compares the number of new post
    '''
    
    assert(isinstance(model_name,str)),'the model name should be of type string'
    assert(isinstance(filepath,str)),'the input filepath should be of type string'
    assert(isinstance(ylimit,list) or ylimit is None),'the input of ylimit should be of type list'
    assert (isinstance(filename, str)), 'the file name should be of type string'

    post_data = pd.read_csv(filepath)
    post_data.drop(axis=1, columns='Unnamed: 0', inplace=True)
    my_colors = ['#800080', '#017270']
    plt.figure()
    post_data.plot(x=model_name+'Model',kind='bar',rot=1,color=my_colors)
    plt.title(model_name,fontdict = {'fontsize' : 25},pad=16)
    plt.ylabel('Number of New Post')
    plt.xlabel('')
    if ylimit is not None:
        plt.ylim(ylimit[0], ylimit[1])
    plt.savefig(filename,dpi=300)
    plt.show()

    
    
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
    
    