import sys,os
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.utils import get_collection_as_dataframe
from sensor.entity import config_entity
from sensor.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
from sensor.components.data_ingestion import DataIngestion



def test_logger_and_exception():
    try:
        pass
        #logging.info('Starting the test_logger_and_exception')
        #result =3/0
        #print(result)
        #logging.info('Stopping the test_logger_and_exception')
    except Exception as e:
        pass
        #logging.debug('Stopping the test_logger_and_exception')
        #raise SensorException(e,sys)

if __name__=="__main__":
    try:
        #test_logger_and_exception()
        get_collection_as_dataframe(database_name= "aps", collection_name="sensor")
        training_pipeline_config= config_entity.TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        print(data_ingestion_config.to_dict())
        data_ingestion=DataIngestion(data_ingestion_config=data_ingestion_config)
        print(data_ingestion.initiate_data_ingestion())

    except Exception as e:
        print(e)