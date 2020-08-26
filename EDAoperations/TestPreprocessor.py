
from ApplicationLogger.AppLogger import Logger
import pandas as pd
from sklearn.preprocessing import StandardScaler


class TestPreprocess:
    """
                                This class is used for test data preprocessing


     """
    def __init__(self,file_object,log_writer):
        self.Testing_file = "TestDatabase\Testdf.csv"
        self.logger = Logger()
        self.file_object = file_object
        self.log_writer = log_writer
        self.file_object = open("Testing_Logs/TestingEdaLog.txt", 'a+')

    def get_data(self):

        """
                      Method Name: get_data
                      Description: This method reads the data from source.
                      Output: A pandas DataFrame.
                      On Failure: Raise Exception


        """
        self.log_writer.log(self.file_object, 'Entered the get_data method of the Data_Getter class')

        try:
            data= pd.read_csv(self.Testing_file,nrows = 20) # reading the data file
            data = data.drop(['Unnamed: 0','reference','_id'],axis = 1)
            print("in testpreprocessor",data.columns)
            self.log_writer.log(self.file_object,'Data Load Successful.Exited the get_data method of the Data_Getter class')
            return data
        except Exception as e:
            self.log_writer.log(self.file_object,'Exception occured in get_data method of the Data_Getter class. Exception message: '+str(e))
            self.log_writer.log(self.file_object,
                                   'Data Load Unsuccessful.Exited the get_data method of the Data_Getter class')
            raise Exception()

    def FillingMissingValues(self,data):

        """
                               Method Name: Filling the Missing Values
                               Description: This method does mean imputation for the missing values
                               Output:A Pandas Dataframe
                               On Failure: Raise Exception


        """

        self.data = data


        try:

            for col in data.columns:
                if data[col].isna().sum() != 0:
                    data[col] = data[col].fillna(data[col].mean())
            return data


        except Exception as e:

            self.log_writer.log(self.file_object,"Mean imputation is completed")
            raise Exception()

    def Scaling(self,data):

        """
                                      Method Name: Scaling
                                      Description: This method brings the data into a single scale
                                      Output:A Pandas Dataframe
                                      On Failure: Raise Exception


               """

        self.log_writer.log(self.file_object, 'Entered into Scaling Method')

        try:

            ss = StandardScaler()
            data = pd.DataFrame(ss.fit_transform(data), columns=data.columns)
            return data

        except Exception as a:

            self.log_writer.log(self.file_object, "Standardscaling is not possible")
            raise Exception()




