# play a very important role. 
# read the dataset from some datasource 
import os
import sys 
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
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
        
if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()
        