
from ApplicationLogger.AppLogger import Logger
import pandas as pd



class TrainPreprocess:

    """
                                    This class is used for train data preprocessing


    """



    def __init__(self,file_object,log_writer):
        self.Training_file = "TrainingDatabase\Traindf.csv"
        self.logger = Logger()
        self.file_object = file_object
        self.log_writer = log_writer
        self.file_object = open("Training_Logs/TrainingEdaLog.txt", 'a+')

    def get_data(self):
        """
        Method Name: get_data
        Description: This method reads the data from source.
        Output: A pandas DataFrame.
        On Failure: Raise Exception

        """
        self.log_writer.log(self.file_object, 'Entered the get_data method of the Data_Getter class')

        try:
            data= pd.read_csv(self.Training_file)
            data = data.drop(['Unnamed: 0','Unnamed: 0.1','_id'],axis = 1)
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


    def separate_label_feature(self,data):
        """
                        Method Name: separate_label_feature
                        Description: This method separates the features and a Label Coulmns.
                        Output: Returns two separate Dataframes, one containing features and the other containing Labels .
                        On Failure: Raise Exception
        """

        self.data = data
        self.log_writer.log(self.file_object, 'Entered the separate_label_feature method of the Preprocessor class')

        try:
            x = self.data.drop(['reference'], axis=1)
            print("X shape:",x.shape)
            y = self.data['reference']

            # Filter the Label columns
            self.log_writer.log(self.file_object,
                            'Label Separation Successful. Exited the separate_label_feature method of the Preprocessor class')
            return x,y

        except Exception as e:
            self.log_writer.log(self.file_object,
                            'Exception occured in separate_label_feature method of the Preprocessor class. Exception message:  ' + str(
                                e))
            self.log_writer.log(self.file_object,
                            'Label Separation Unsuccessful. Exited the separate_label_feature method of the Preprocessor class')
            raise Exception()


