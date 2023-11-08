from sensor import utils
from sensor.entity import config_entity
from sensor.entity import artifact_entity
from sensor.logger import logging
from sensor.exception import SensorException
import os,sys
from sensor.utils import get_collection_as_dataframe
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

class DataIngestion:
    def __init__(self,data_ingestion_config:config_entity.DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise SensorException(e,sys)

    def initiate_data_ingestion(self,)->artifact_entity.DataIngestionArtifact:
        try:
            logging.info(f"{'>>'*20} Data Ingestion {'<<'*20}")
            #Exporting collection data to pandas dataframe.
            df:pd.DataFrame =utils.get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name,
                collection_name=self.data_ingestion_config.collection_name)

            
            #Save data in feature store
            df.replace(to_replace="na", value=np.NAN,inplace=True)
            
            #Create feature store folder if not available
            logging.info(f"create feature store folder if not available")
            feature_store_dir= os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir,exist_ok=True)

            #Save df to feature store folder
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False, header=True)
            logging.info(f"saved dataframe into feature stored folder")
            
            
            #Split dataframe into train test split
            logging.info("Performed train test split on the dataframe")
            train_df, test_df=train_test_split(df,test_size=self.data_ingestion_config.test_size)

            #Create dataset directory folder if not available
            dataset_dir= os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir,exist_ok=True)
             
            logging.info(f"Exporting train and test file path.")

            #Save train and test dataframe to folder
            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False, header=True)
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False, header=True)

            logging.info(f"Exported train and test file path.")

            #Prepare artifact
            data_ingestion_artifact=artifact_entity.DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path)

            logging.info(f"data_ingestion_artifact = {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise SensorException(e,sys)