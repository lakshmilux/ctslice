from datetime import datetime
from os import listdir
from ApplicationLogger.AppLogger import Logger
import pandas as pd
import json
from pymongo import MongoClient
import pymongo
import ssl


class DBOperations:
    """
                This class is used for Db connection,collection creation,insert data,storing the test data.


            """

    def __init__(self,path):
        self.testpath = "TestDataBatchFiles/test.csv"
        self.testpath = path
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
                "mongodb+srv://lakshmiram:luxthebest$416@cluster0.4r0et.mongodb.net/TestSliceDb?retryWrites=true&w=majority", ssl=True,ssl_cert_reqs=ssl.CERT_NONE)
            self.testdb = self.client["TestSliceDb"]
            #mongodb + srv: // lakshmiram:luxthebest$416@cluster0.4r0et.mongodb.net /TestSliceDb?retryWrites = true & w = majority
            #self.client = MongoClient("localhost", 27017, maxPoolSize=50)
            #self.testdb = self.client["TestSliceDb"]
            self.testcollection = self.testdb["TestSliceCollection"]
            log_file = open("Training_Logs\Dbconnection.txt", 'a+')
            self.logger.log(log_file, "Successfully connected to  MongoDb server and created train and test collections")
            log_file.close()

        except ConnectionError:
            log_file = open("Training_Logs\Dbconnection.txt", 'a+')
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
                dftest = pd.read_csv(self.testpath,dtype = str)
                data_jsontest = json.loads(dftest.to_json(orient='records'))
                self.testcollection.insert_many(data_jsontest)
                print((data_jsontest))

                log_file = open("Testing_Logs/InsertData.txt", 'a+')
                self.logger.log(log_file, "Collection for both train and test created successfully!!")
                log_file.close()

                df2 = pd.DataFrame.from_records(data_jsontest)
                df2.to_csv("TestDatabase/Testdf.csv")

                log_file = open("Testing_Logs/InsertData.txt", 'a+')
                self.logger.log(log_file, "Data is exported from mongodb into csv format.....")
                log_file.close()

        except Exception as e:

            log_file = open("Testing_Logs/InsertData.txt", 'a+')
            self.logger.log(log_file, "Error : %s" %e)
            log_file.close()

