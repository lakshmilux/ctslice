from flask import Flask, request, render_template
from flask import Response
from flask_cors import CORS, cross_origin
from TrainingModel import TrainModel
from PredictModel import prediction
from MondoDBOperations import TrainDbOperations
from MondoDBOperations import TestDbOperations
import os
import flask_monitoringdashboard as dashboard



os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL','en_US.UTF-8')


app = Flask(__name__)
dashboard.bind(app)
CORS(app)



@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        if request.form is not None:
            path = request.form['filepath']
            pred_val = TestDbOperations.DBOperations(path)  # object initialization
            pred_val.ConnectMongoDB()
            pred_val.InsertData()


            pred = prediction(path)  # object initialization

            # predicting for dataset present in database
            path,result = pred.predictionFromModel()

            #return Response("%s" % path )
            return Response(
                "Prediction File created at %s!!!" % path + "   " + "prediction results are given below %s" % result.to_html())

    except ValueError:
        print("Error Occurred! " +str(ValueError))
        return Response("Error Occurred! %s" %str(ValueError))
    except KeyError:
        print("Error Occurred! " + str(KeyError))
        return Response("Error Occurred! %s" %KeyError)
    except Exception as e:
        print("Error Occurred! " +str(e))
        return Response("Error Occurred! %s" %e)



@app.route("/train", methods=['POST'])
@cross_origin()
def trainRouteClient():

    try:
        if request.form['filePath'] is not None:
            path = request.form['filePath']
            train_valObj = TrainDbOperations.DBOperations(path) #object initialization
            train_valObj.ConnectMongoDB()
            train_valObj.InsertData()


            trainModelObj = TrainModel() #object initialization
            trainModelObj.trainingModel() #training the model for the files in the table


    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:

        return Response("Error Occurred! %s" % e)
    return Response("Training successfull!!")



if __name__ == "__main__":
    #app.run(host = '0.0.0.0', port=8080)
    app.run(debug = True,port = '5000')



