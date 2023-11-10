import pymongo
import pandas as pd 
import json
# Provide the mongodb localhost url to connect python to mongodb.
client = pymongo.MongoClient("mongodb://localhost:27017/neurolabDB")

DATA_FILE_PATH = "/config/workspace/Sensor_fault_detection/aps_failure_training_set1.csv"
DATABASE_NAME = "aps"
COLLECTION_NAME = "sensor"


if __name__=="__main__":
    df = pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and columns : {df.shape}")

    # resting the index
    df.reset_index(drop=True, inplace=True)

    # convert dataframe to json to dump the these record in mongo db
    json_record = list(json.loads(df.T.to_json()).values())

    print(json_record[0])
    
    # Insert converted records to mongodb
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)

