import pandas as pd
import xml.etree.ElementTree as ET
import re
import os
from CustomThread import ThreadWithReturnValue
import logging

logging.basicConfig(level=logging.DEBUG, filename='retrieve_data.log', format='%(asctime)s [%(levelname)s] %(message)s')	

def load_data(filepath):
    """ Load data from a csv file into a xml ElementTree object."""
    tree = ET.parse(filepath)
    root = tree.getroot()
    
    return root   

def check_for_sale(df_sales):
    """ Check if the file contains sales data."""
    if df_sales.empty:
        return False
    else:
        return True

def sale_or_return(df_sales):
    """ Check if the sale is a sale or a return."""
    if 'SaleDescription' in df_sales.columns:
        return 'Sale'
    else:
        return 'Unknown'

def retrieve_data(filepath, namespace, id):
    root = load_data(filepath)
    df = pd.DataFrame(columns=['customID', 'Date', 'SaleDescription', 'SaleItemID', 'SaleMerchandiseHierarchy'])
    
    sales = root.findall(".//{%s}Sale" % namespace)
    date = root.find(".//{%s}BeginDateTime" % namespace)
    
    desc_ns = "{%s}Description" % namespace
    item_ns = "{%s}ItemID" % namespace
    hier_ns = "{%s}MerchandiseHierarchy" % namespace
    
    for i in range(len(sales)):
        description = sales[i].find(desc_ns)
        item_id = sales[i].find(item_ns)
        hierarchy = sales[i].find(hier_ns)
        
        df.loc[i] = [None] * len(df.columns)
        df.loc[i]['SaleDescription'] = description.text
        if item_id is not None:
            df.loc[i]['SaleItemID'] = item_id.text
        else:
            df.loc[i]['SaleItemID'] = None
        if hierarchy is not None:
            df.loc[i]['SaleMerchandiseHierarchy'] = hierarchy.text
        else:
            df.loc[i]['SaleMerchandiseHierarchy'] = None
    
    df = df[df['SaleDescription'].notna()]
    df['customID'] = id
    df['Date'] = date.text
    return df

def combine_files(filepaths):
    """ Combine relevant data from multiple files into one dataframe."""
    df = pd.DataFrame(columns=['customID', 'Date', 'SaleDescription', 'SaleItemID', 'SaleMerchandiseHierarchy'])
    namespace = "http://www.nrf-arts.org/IXRetail/namespace/"
    # filepaths = filepaths[:1000]
    
    thread_batch = 100
    
    logging.info('Starting threads for retrieving data')
    for i in range(0, len(filepaths), thread_batch):
        logging.debug('Starting threads for files ' + str(i) + ' to ' + str(min(len(filepaths), i+thread_batch)))
        threads = []
        for j in range(0, thread_batch):
            if j+i >= len(filepaths): break
            threads.append(ThreadWithReturnValue(target=retrieve_data, args=(filepaths[j+i], namespace, j+i)))
            threads[j].start()
        for thread in threads:
            df_temp = thread.join()
            df = pd.concat([df, df_temp], ignore_index=True)
    logging.debug('Length of df: ' + str(len(df)))
    
    # for file in filepaths:
    #     df_temp = retrieve_data(file, namespace, 0)
    #     df = pd.concat([df, df_temp], ignore_index=True)
        
    return df

def get_filenames(directory):
    """ Get the filenames of all xml files in the Data folder."""
    filepaths = []
    #loop through folders in directory and add filepaths of xml files to list
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".xml"):
                filepaths.append(os.path.join(root, file))
                
    logging.debug('Number of files: ' + str(len(filepaths)))
        
    return filepaths

#track runtime
import time
start = time.time()

filepaths = get_filenames('C:/Users/20193222/OneDrive - TU Eindhoven/JADS/DiIA Project/April 2023')
# filepaths = get_filenames('Data')
df = combine_files(filepaths)
df.to_csv('Data/sales_data_apr_2023.csv', index=False)
end = time.time()
logging.info('Runtime: ' + str(end - start))
