"""
This is the Entry point for Training the Machine Learning Model.


"""


# Doing the necessary imports
import pandas as pd
from ApplicationLogger import AppLogger
from EDAoperations import TestPreprocessor
import pickle
from sklearn.preprocessing import StandardScaler


class prediction:

    def __init__(self,path):
        self.file_object = open("Testing_Logs/Prediction_Log.txt", 'a+')
        self.log_writer = AppLogger.Logger()
        self.path = "TestDatabase/Testdf.csv"


    def predictionFromModel(self):
        # Logging the start of Training
        try:

            self.log_writer.log(self.file_object,'Start of Prediction')
            preprocessor = TestPreprocessor.TestPreprocess(self.file_object, self.log_writer)
            # Getting the data from the source

            """doing the test data preprocessing"""
            data = preprocessor.get_data()

            data = preprocessor.FillingMissingValues(data)
            print("filldata",data.shape)

            data = preprocessor.Scaling(data)
            print("scaledata", data.columns)

            result=[] # initialize balnk list for storing predicitons
            with open("PCAPickle/PCA.pickle", "rb") as f:
                pca = pickle.load(f)


            ss = StandardScaler()

            X_test_scaled_pca = pca.transform(ss.fit_transform(data))

            print("Xscaled:",X_test_scaled_pca.shape)
            loaded_model = pickle.load(open('DecTreePickle/dt.pickle', 'rb'))            #

            for val in (loaded_model.predict(X_test_scaled_pca)):
                 result.append(val)

            result = pd.DataFrame(result,columns=['ReferencePredictions'])
         # appends result to prediction file
            result = pd.concat([data,result],axis = 1)
            result = result.iloc[:,1:]
            print("final",result.columns)
            path="Prediction_Output_File/Predictions2.csv"
            result.to_csv("Prediction_Output_File/Predictions.csv",header=True)

            # logging the successful Testing
            self.log_writer.log(self.file_object,'End of Prediction')
            return path,result
        except Exception as ex:
            # logging the unsuccessful Testing
            self.log_writer.log(self.file_object, 'Error occured while running the prediction!! Error:: %s' % ex)
            raise ex
            return path



