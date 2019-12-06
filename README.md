# ece143_fa19_bazhou_Varun_Angela_Frank
The src folder contains all the python scripts (scraping, cleaning, processing, plots).
The data folder contains all the data needed for the processing.<br>

Steps:
1. Data Scraping:<br>
For Offerup: You need to install Chrome webdriver for your own OS(webdrivers for linux and macos have been installed).
    ```shell
    cd src/scraper/
    . batch_scrape.sh
    ```
    Description: The script named "batch_scrape.sh" is used to scrape data of 10 cellphones automatically in sequence. 
    The script actually call a python file named "scrap_v0.2_offerup_10_models.py" for multiple times. 
    The data generated is stored in data folder.<br>  
For Craigslist:<br>
    ```shell
    python Craigslist_v3.py 
    ```
    Description: The urls for scraping different phones have all been set in this file. 
    The data generated is stored in data/Craigslist.<br>  
2. Data Cleaning & Processing:<br>
For Offerup: 
    ```shell
    cd src/processor/
    python process_offerup.py
    ```
    Description: Actually the python file named "process_offerup.py" is used to supply methods
    for plotting.<br>  
For Craigslist:
    ```shell
    cd src/processor/
    python dataAnalysis_Craigslist.py
    ```
    Description: Actually the python file named "dataAnalysis_Craigslist.py" is also used to supply methods
    for plotting.<br>
3. Plotting:
    ```shell
   jupyter notebook: 
   
    ```

1. add missing logos to the needing blank 
2. Add photos for Iphonex and Samsung S8 to slides like slide 9 and 10
3. section b too much information, gradually show them one by one with animation
4. The final chart should be higher && logo is better than name && backgroud color && easy for eyes
