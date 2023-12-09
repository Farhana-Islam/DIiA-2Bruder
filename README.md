# DIIA Project for HFG

In this project we will be using receipt data from Holland Food Group to create a predictive model that can be used by store managers to order stock. We will combine the receipt data with holiday and weather data, to take these into account in the model. The model will predict sales per day, and these can be added up to get a number of products that need to be ordered for a period of time. 

## Table of Contents

- [Structure](#structure)
- [Installation](#installation)
- [Usage](#usage)
- [Environments](#environments)

## Structure
This project is split up into multiple steps:
1. Data extraction
2. Exploratory data analysis
3. Model development and evaluation

In step one, sales data is extracted from HFG's receipt files (in xml format) and saved to a csv. We only extract the data we are expecting to use, to avoid creating enourmous csv files. The code for this can be found in the _Data Retrieval_ folder. We also use weather and holiday data, which can be found in the _Data_ folder. The HFG data is not shared to this Github.

In step two, the weather and holiday data is added to the sales data, as well as some additional features like month and day of the week. Then, some exploratory data analysis is performed, looking at relationships between features and creating plots to help validate using the features in the models. The code for this can be found in the _Exploratory Data Analysis_ folder.

Step three focuses on model training and evaluation, as well as feature selection and making predictions. This can be found in the _Models_ folder, and is split into two files. The _model\_pipeline.ipynb_ includes the pipeline structure to automatically preprocess data, train and evaluate models, select the best model per product and use these to make predictions. However, not all models are functioning inside that file, which is why the _Combined\_model.ipynb_ is also included. This file runs part of the models (training, evaluation, predictions) and the output for the models that don't work in the first file can be created with the second. 

## Installation

There are several steps to this project, depending on what step you are working on you need to follow different instructions. A **requirements.txt** file has been created that included packages for all steps, so make sure to install them:

``` pip install -r requirements.txt ```

* Note: We recommend doing this in an evironment specifically for this project, that way no other packages or already existing versions get messed up. Instructions on how to set up an environment: [Environments](#environments)

### Installation for Retrieving Data
This step transforms xml files to a csv file. Therefore, it is required that you have the HFG xml files downloaded. It does not matter how they are organised (in folders or not), the code will run through all folders within your directory and find all xml files. So make sure there are no other xml files that do not belong to this project in the same directory.
The two files required for this step are **retrieve_data_v2.py** and **CustomThread.py**. Make sure to have those in the same directory. 


### Installation for Exploratory Data Analysis
For this step you need the csv file(s) created in the previous step. It also requires the **weather.json** and both the **holidays_de.xlsx** and **schoolholidays_de.xlsx** files. 

### Installation for Models
For this step you need the csv file(s) created in the previous step, which have the correct features added to them. 

## Usage

### Instructions for Retrieving Data
Before running anything, make sure to change the filepaths in the code in lines **107** and **110**. The first path should lead to the directory which has the xml data you want to extract (it can be in folders within that directory). I recommend running the code on a maximum of one month of sales data at a time. The second filepath is where the output csv file will be saved to, so choose a directory and filename for that. 

Then you can run the file in the terminal of your IDE/code editor (like VSCode or Pycharm). 

### Instructions for Exploratory Data Analysis
This code creates some statistics and some figures that we will be using in our presentations and report. It also outputs csv files of the preprocessed data.

### Instructions for Models
This code runs the models and the different steps needed for that. It outputs several xlsx files with predictions per product, as well as a csv with metrics per product.

## Environments
Follow the steps below to create a virtual environment. This will allow you to easily install the specific packages for this project without possibly messing up the version or other packages. 
1. Open your command prompt (CMD)
2. Set the directory to the folder that also has the code for this project (for example *retrieve_data_v2.py*):
```cd C:\Users\12345\Folder\Folder``` (use your own directory)
3. Create a virtual environment: ```py -m venv env```

How to use the virtual environment:

4. Your IDE/code editor might automatically recognize it and ask whether you want to use it for the workspace folder/as your python interpreter. Select **yes** if this happens. If this does not happen, select your interpreter manually (Google select interpreter or environment with the IDE you are using). 
5. To install packages or do anything from your command prompt in the environment you have to access it first. You do this by running ```.\env\Scripts\activate``` in your command prompt, in the same directory as your code (repeat **step 2** if you are not in there anymore). 
6. Now you can run any pip install like you normally would. To install all required packages at once, run: ```pip install -r requirements.txt``` 
7. If you want to exit the environment to do other things in your command prompt you can use ```deactivate```. Or just close the command prompt and open a new one, that works too. 

You do not need to activate the environment to be able to run the code (unless you would run it from your command prompt), you only need to do that to install the packages for the project or check the version of packages for example. 