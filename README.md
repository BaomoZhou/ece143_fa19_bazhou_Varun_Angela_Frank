# ece143_fa19_bazhou_Varun_Angela_Frank
The main folder contains all the python scripts (scraping, cleaning, processing, plots).
The subfolders contain all the data needed for the processing.<br>

Steps:
1. Data Scraping:<br>
For Offerup: You need to install Chrome webdriver of appropriate version according to the OS(webdrivers for linux and macos have been installed).
    ```shell
    . batch_scrape.sh
    ```
    Description: The script named "batch_scrape.sh" is used to scrape data of 10 cellphones automatically in sequence. 
    The script actually call a python file named "scrap_v0.2_offerup_10_models.py" 10 times to scrape data from 10 different phones. 
    The data generated is stored in subfolders whose names contain "\_Offerup\_":<br>
    e.x.:<br>
    "B_Offerup_IP6" means data of Iphone 6 from website Offerup. "B" means this data is used for analysis part B.<br>  
For Craigslist:<br>
    ```shell
    python Craigslist_v3.py 
    ```
    Description: The urls for scraping different phones have all been set in this file. 
    The data generated is stored in subfolder named "Craigslist_data".<br>  
2. Data Cleaning & Processing:<br>
For Offerup: 
    ```shell
    python process_offerup.py
    ```
    Description: Actually the python file named "process_offerup.py" is used to supply methods
    for plotting.<br>  
For Craigslist:
    ```shell
    python dataAnalysis_Craigslist.py
    ```
    Description: Actually the python file named "dataAnalysis_Craigslist.py" is also used to supply methods
    for plotting.<br>
3. Plotting:
    ```shell
   jupyter notebook: ECE143 project plot.ipynb
    ```
   Description: The methods for data cleaning and processing are called in jupyter notebook named "ECE143 project plot.ipynb".
   After that, the plotting work finished based on the processed data.<br>