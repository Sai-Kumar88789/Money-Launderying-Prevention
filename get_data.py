from aml.data_access.transaction_data import TransactionData
from aml.constant import database
from dotenv import load_dotenv
from aml.logger import logging
load_dotenv()
import os
if __name__=='__main__':
    # features_file_path ="elliptic_bitcoin_dataset/elliptic_txs_features.csv"
    # edgelist_file_path ="elliptic_bitcoin_dataset/elliptic_txs_edgelist.csv"
    # classes_file_path  ="elliptic_bitcoin_dataset/elliptic_txs_classes.csv"
    labled_data_file_path = "elliptic_bitcoin_dataset/labled_dataset/labled_data.csv"

    sd = TransactionData()
    rows = sd.session.execute(f"SELECT table_name FROM system_schema.tables WHERE keyspace_name = '{database.KEYSPACE_NAME}' ")
    collection_names = [row.table_name for row in rows]
    print(collection_names)

   
    if database.LABLED_DATA_COLLECTION_NAME in collection_names:
        sd.session.execute("DROP TABLE {database.KEYSPACE_NAME}.{database.LABLED_DATA_COLLECTION_NAME}")
    sd.save_csv_file(file_path=labled_data_file_path,keyspace_name=database.KEYSPACE_NAME,collection_name=database.LABLED_DATA_COLLECTION_NAME)
    # logging.info("Import the Transactional Edgelist csv file to database'")
    # if EDGELIST_COLLECTION_NAME in collection_names:
    #     sd.session.execute("DROP TABLE {KEYSPACE_NAME}.{EDGELIST_COLLECTION_NAME}")
    # sd.save_csv_file(file_path=edgelist_file_path,keyspace_name=KEYSPACE_NAME,collection_name=EDGELIST_COLLECTION_NAME)

    # logging.info("Import the Transactional Classes csv file to database'")
    # if CLASSES_COLLECTION_NAME in collection_names:
    #     sd.session.execute("DROP TABLE {KEYSPACE_NAME}.{CLASSES_COLLECTION_NAME}")
    # sd.save_csv_file(file_path=classes_file_path,collection_name=CLASSES_COLLECTION_NAME)

    
    #  to export the data from the collections
    # df = sd.export_collection_as_dataframe(
    #     save_file_path= SAVE_FILE_PATH,
    #     keyspace_name=KEYSPACE_NAME,
    #     collection_name=EDGELIST_COLLECTION_NAME
    # )
    # print(df.head())
    # print('Successfully Exported!')


