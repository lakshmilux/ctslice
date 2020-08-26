"""
This is the Entry point for Training the Machine Learning Model.


"""


# Doing the necessary imports
from sklearn.model_selection import train_test_split
from ModelBuiding import Models
from ApplicationLogger import AppLogger
from ModelOperations import ModelSaving
from EDAoperations import TrainPreprocessor


class TrainModel:

    def __init__(self):
        self.log_writer = AppLogger.Logger()
        self.file_object = open("Training_Logs/ModelTrainingLog.txt", 'a+')

    def trainingModel(self):
        # Logging the start of Training
        self.log_writer.log(self.file_object, 'Start of Training')
        try:
            # Getting the data from the source



            """doing the data preprocessing"""

            preprocessor= TrainPreprocessor.TrainPreprocess(self.file_object,self.log_writer)

            data = preprocessor.get_data()

            data = preprocessor.FillingMissingValues(data)
            print(data.shape)


            x,y = preprocessor.separate_label_feature(data)

            # splitting the data into training and test set for each cluster one by one
            x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=1 / 3, random_state=355)

            model_finder = Models.ModelBuilding(self.file_object,self.log_writer) # object intilization

            X_train_scaled_pca,X_test_scaled_pca = model_finder.BuildingPCA(x_train,x_test)

            dt = model_finder.DecisionTreeModel(X_train_scaled_pca, y_train)
            Encv = model_finder.Elasticnetcv(X_train_scaled_pca,y_train)


            best_model_name,best_model=model_finder.GetBestModel(X_train_scaled_pca,y_train,X_test_scaled_pca,y_test)

                #saving the best model to the directory.
            file_op = ModelSaving.Model_Ops(self.file_object,self.log_writer)

            save_model=file_op.save_model(best_model,best_model_name)

            # logging the successful Training
            self.log_writer.log(self.file_object, 'Successful End of Training')
            self.file_object.close()

        except Exception:
            # logging the unsuccessful Training
            self.log_writer.log(self.file_object, 'Unsuccessful End of Training')
            self.file_object.close()
            raise Exception


