# play a very important role. 
# read the dataset from some datasource 
import os
import sys 
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig
# any input required we will give through this class
@dataclass # we don't need to use __init__ to define our variables using dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifact',"train.csv") # all the outputs will be stored inside the artifact folder
    test_data_path: str=os.path.join('artifact',"test.csv")
    raw_data_path: str=os.path.join('artifact',"data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig() # those 3 paths will be saved inside this class variable 

    def initiate_data_ingestion(self):
        # this will help us to read our data from other databases
        logging.info("Entered the data ingestion method or component")
        try:
            df = pd.read_csv('notebook\data\stud.csv') # here we can change our code to read it from different sources like mongodb or mysql
            logging.info('Read the dataset as dataframe')
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok = True)

            df.to_csv(self.ingestion_config.raw_data_path,index = False, header = True)
            logging.info("Train test split initiated")
            train_set, test_set = train_test_split(df,test_size = 0.2,random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path,index = False, header = True)
            test_set.to_csv(self.ingestion_config.test_data_path,index = False, header = True)

            logging.info("Ingestion of the data is completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)
        
'''This class is responsible for the actual data ingestion process.
__init__ Method
Initializes an instance of DataIngestionConfig and stores it in self.ingestion_config. This instance holds the paths for the train, test, and raw data.
initiate_data_ingestion Method
Logs the start of the data ingestion process.
Tries to execute the data ingestion logic inside a try block, which allows for exception handling.
Reads a dataset from a specified CSV file (stud.csv) into a pandas DataFrame. This part can be modified to read data from various sources like databases.
Creates necessary directories for storing output files using os.makedirs.
Saves the raw data into a CSV file specified by self.ingestion_config.raw_data_path.
Splits the data into training and testing sets using train_test_split from scikit-learn, with a specified test size and random state for reproducibility.
Saves the split datasets into their respective CSV files as specified in the configuration.
Logs the completion of the data ingestion process.
Returns the paths to the train and test data files.'''
        
if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    data_transformation.initiate_data_transformation(train_data,test_data)
        