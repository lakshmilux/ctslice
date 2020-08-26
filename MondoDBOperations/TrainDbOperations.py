from datetime import datetime
from os import listdir
from ApplicationLogger.AppLogger import Logger
import pandas as pd
import json
import pymongo
from pymongo import MongoClient
import ssl


class DBOperations:
    """
                                        This class is used for Db connection,collection creation,insert data,storing data.


        """

    def __init__(self,path):
        self.path = "TrainDataBatchFiles/Trainslice.csv"
        self.path = path
        self.logger = Logger()

    def ConnectMongoDB(self):


        """
                        Method Name: dataBaseConnection
                        Description: This method creates the database with the given name and if Database already exists then opens the connection to the DB.
                        Output: Connection to the DB
                        On Failure: Raise ConnectionError

                        """
        try:

            self.client = pymongo.MongoClient(
                "mongodb+srv://lakshmiram:luxthebest$416@cluster0.4r0et.mongodb.net/TrainSliceDb?retryWrites=true&w=majority",
                 ssl=True,ssl_cert_reqs=ssl.CERT_NONE)
            self.db = self.client["TrainSliceDb"]
            #mongodb + srv: // lakshmiram: luxthebest$416 @ cluster0.4r0et.mongodb.net/TrainSliceDb?retryWrites = true & w = majority
            #self.client = MongoClient("localhost", 27017, maxPoolSize=50)
            #self.db = self.client["TrainSliceDb"]
            self.collection = self.db["TrainSliceCollection"]
            log_file = open("Training_Logs\Dbconnection.txt", 'a+')
            self.logger.log(log_file, "Successfully connected to  MongoDb server and created train and test collections")
            log_file.close()

        except ConnectionError:
            log_file = open("Training_Logs/Dbconnection.txt", 'a+')
            self.logger.log(log_file,  "Error while connecting to database: %s" %ConnectionError)
            log_file.close()
            raise ConnectionError


    def InsertData(self):

        """

           Method Name: Insert data
           Description: This method creates a collection in the given database which will be used to insert the data.
           Output: None
           On Failure: Raise Exception


        """

        try:
                df = pd.read_csv(self.path,dtype = str)
                data_json = json.loads(df.to_json(orient='records'))
                self.collection.insert_many(data_json)
                print((data_json))

                log_file = open("Training_Logs/InsertData.txt", 'a+')
                self.logger.log(log_file, "Collection for  train data is created successfully!!")
                log_file.close()

                df1 = pd.DataFrame.from_records(data_json)
                df1.to_csv("TrainingDatabase/Traindf.csv")


                log_file = open("Training_Logs/InsertData.txt", 'a+')
                self.logger.log(log_file, "Data is exported from mongodb into csv format.....")
                log_file.close()

        except Exception as e:

            log_file = open("Training_Logs/InsertData.txt", 'a+')
            self.logger.log(log_file, "Error : %s" %e)
            log_file.close()
