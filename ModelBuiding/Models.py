from sklearn.model_selection import GridSearchCV
from ApplicationLogger.AppLogger import Logger
from sklearn.decomposition import PCA
from sklearn.linear_model import ElasticNetCV
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor
import pickle
import numpy as np

class ModelBuilding:

   """
                                    This class is used for Building Different Models on the Data


   """

   def __init__(self,file_object,log_writer):

        self.logger = Logger()
        self.file_object = file_object
        self.log_writer = log_writer
        self.encv = ElasticNetCV()
        self.pca = PCA()
        self.dt = DecisionTreeRegressor()


   def BuildingPCA(self, x_train,x_test):

        """
                      Method Name: Buildingpca
                      Description: By this method only the data is reduced from 386 columns into 209 principal components
                      Output: A Pandas Dataframe.
                      On Failure: Raise Exception


        """

        self.x_train = x_train
        self.x_test = x_test
        try:
            self.log_writer.log(self.file_object, 'PCA Decomposition started')
            ss = StandardScaler()
            pca = PCA(0.95)
            pcamodel = pca.fit(ss.fit_transform(x_train))
            X_train_scaled_pca = pcamodel.transform(ss.fit_transform(x_train))
            X_test_scaled_pca = pcamodel.transform(ss.fit_transform(x_test))
            with open('PCAPickle/PCA.pickle', 'wb') as file:
                pickle.dump(pcamodel, file)
            return X_train_scaled_pca, X_test_scaled_pca

        except Exception as p:
            self.log_writer.log(self.file_object, 'PCA Decomposition failed :%s' % p)
            raise Exception()



   def DecisionTreeModel(self, X_train_scaled_pca, ytrain):

         """
                     Method Name: Decision Tree Model.
                     Description: This method uses the decision tree Regressor model on Data.
                     Output: Model with best parameters.
                     On Failure: Raise Exception.


         """
         self.log_writer.log(self.file_object, "Decision Tree Model Training started")
         try:
        # initializing with different combination of parameters
            self.param_grid = {"max_depth": range(8,10),"min_samples_split" : range(2,5),
                               "min_samples_leaf" : range(7,10)}

        # Creating an object of the Grid Search class
            self.grid = GridSearchCV(estimator=self.dt, param_grid=self.param_grid, cv=5, verbose=3,n_jobs=-1)
        # finding the best parameters
            self.grid.fit(np.array(X_train_scaled_pca), np.array(ytrain))

        # extracting the best parameters
            self.min_samples_split = self.grid.best_params_['min_samples_split']
            self.max_depth = self.grid.best_params_['max_depth']
            self.min_samples_leaf = self.grid.best_params_['min_samples_leaf']

        # creating a new model with the best parameters
            self.dt = DecisionTreeRegressor(max_depth=self.max_depth,
                                       min_samples_split=self.min_samples_split,
                                      min_samples_leaf=self.min_samples_leaf)
        # training the mew model
            self.dt.fit(np.array(X_train_scaled_pca), np.array(ytrain))

            with open('DecTreePickle/dt.pickle', 'wb') as file:
                    pickle.dump(self.dt, file)



            self.log_writer.log(self.file_object,
                            'Decision Tree best params: ' + str(
                                self.grid.best_params_) + '. Exited the get_best_params_for_decision tree method of the Model_Finder class')



            return self.dt

         except Exception as d:

             self.log_writer.log(self.file_object, "RandomForestModel Training stopped : %s" % d)
             raise Exception()


   def Elasticnetcv(self,X_train_scaled_pca,ytrain):

       """
                     Method Name: ElasticnetCV.
                     Description: This method uses the model elasticnetcv on the data.
                     Output: Model with best parameters.
                     On Failure: Raise Exception.


       """
       self.log_writer.log(self.file_object,"Elasticnetcv started")
       try:
             self.ecv = ElasticNetCV(cv=5, alphas=[0.1, 0.3, 0.5, 0.7, 1, 0.01, 0.001])
             self.ecv.fit(np.array(X_train_scaled_pca), np.array(ytrain))
             self.log_writer.log(self.file_object,
                    'Elasticcv ended')

             return self.ecv

       except Exception as d:

             self.log_writer.log(self.file_object, "RandomForestModel Training stopped : %s" % d)
             raise Exception()



   def GetBestModel(self,X_train_scaled_pca,ytrain,X_test_scaled_pca,ytest):

       """
                     Method Name: getbestmodel.
                     Description: This method finds the best model among the models we train on data.
                     Output: model with best score.
                     On Failure: Raise Exception.


       """
       self.log_writer.log(self.file_object,
                           'Entered the get_best_model method of the Model_Finder class')

       try:

           self.decision_tree_score = self.dt.score(X_test_scaled_pca, ytest)
           self.elasticnetcv_score = self.ecv.score(X_test_scaled_pca,ytest)
           print(self.decision_tree_score)
           print("elastic",self.elasticnetcv_score)
           if (self.decision_tree_score > self.elasticnetcv_score):
               return 'Decision Tree', self.dt
           else:
               return "ElasticNetCV" , self.ecv

       except Exception as e:
           self.log_writer.log(self.file_object,
                               'Exception occured in get_best_model method of the Model_Finder class. Exception message:  ' + str(
                                   e))
           self.log_writer.log(self.file_object,
                               'Model Selection Failed. Exited the get_best_model method of the Model_Finder class')
           raise Exception()
