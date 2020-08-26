import pickle
import os
import shutil
from ApplicationLogger.AppLogger import Logger


class Model_Ops:
    """
                This class shall be used to save the model after training
                and load the saved model for prediction.



                """
    def __init__(self,file_object,log_writer):
        self.file_object = file_object
        self.log_writer = log_writer
        self.logger = Logger()
        self.model_directory='Models/'

    def save_model(self,model,filename):
        """
            Method Name: save_model
            Description: Save the model file to directory
            Outcome: File gets saved
            On Failure: Raise Exception

"""
        self.log_writer.log(self.file_object, 'Entered the save_model method of the File_Operation class')
        try:
            path = os.path.join(self.model_directory,filename) #create seperate directory for each cluster
            if os.path.isdir(path): #remove previously existing models for each clusters
                shutil.rmtree(self.model_directory)
                os.makedirs(path)
            else:
                os.makedirs(path) #
            with open(path +'/' + filename+'.sav',
                      'wb') as f:
                pickle.dump(model, f) # save the model to file
            self.log_writer.log(self.file_object,
                                   'Model File '+filename+' saved. Exited the save_model method of the Model_Finder class')

            return 'success'
        except Exception as e:
            self.log_writer.log(self.file_object,'Exception occured in save_model method of the Model_Finder class. Exception message:  ' + str(e))
            self.log_writer.log(self.file_object,
                                   'Model File '+filename+' could not be saved. Exited the save_model method of the Model_Finder class')
            raise Exception()

    def load_model(self,filename):
        """
                    Method Name: load_model
                    Description: load the model file to memory
                    Output: The Model file loaded in memory
                    On Failure: Raise Exception

        """
        self.log_writer.log(self.file_object, 'Entered the load_model method of the File_Operation class')
        try:
            with open(self.model_directory + filename + '/' + filename + '.sav','rb') as f:
                self.log_writer.log(self.file_object,
                                       'Model File ' + filename + ' loaded. Exited the load_model method of the Model_Finder class')
                return pickle.load(f)
        except Exception as e:
            self.log_writer.log(self.file_object,
                                   'Exception occured in load_model method of the Model_Finder class. Exception message:  ' + str(
                                       e))
            self.log_writer.log(self.file_object,
                                   'Model File ' + filename + ' could not be saved. Exited the load_model method of the Model_Finder class')
            raise Exception()

    def find_correct_model_file(self):
        """
                            Method Name: find_correct_model_file
                            Description: Select the correct model based on cluster number
                            Output: The Model file
                            On Failure: Raise Exception


                """
        self.log_writer.log(self.file_object, 'Entered the find_correct_model_file method of the File_Operation class')
        try:
            self.folder_name=self.model_directory
            self.list_of_model_files = []
            self.list_of_files = os.listdir(self.folder_name)
            for self.file in self.list_of_files:
                try:
                        self.model_name=self.file
                except:
                    continue
            self.model_name=self.model_name
            self.log_writer.log(self.file_object,
                                   'Exited the find_correct_model_file method of the Model_Finder class.')
            return self.model_name
        except Exception as e:
            self.log_writer.log(self.file_object,
                                   'Exception occured in find_correct_model_file method of the Model_Finder class. Exception message:  ' + str(
                                       e))
            self.log_writer.log(self.file_object,
                                   'Exited the find_correct_model_file method of the Model_Finder class with Failure')
            raise Exception()