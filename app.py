from flask import Flask, url_for, render_template, redirect
from forms import PredictForm
from flask import request, sessions
import requests
from flask import json
from flask import jsonify
from flask import Request
from flask import Response
import urllib3
import json
# from flask_wtf import FlaskForm

app = Flask(__name__, instance_relative_config=False)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'development key' #you will need a secret key

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')

@app.route('/', methods=('GET', 'POST'))

def startApp():
    form = PredictForm()
    return render_template('index.html', form=form)

@app.route('/predict', methods=('GET', 'POST'))
def predict():
    form = PredictForm()
    if form.submit():

        # NOTE: generate iam_token and retrieve ml_instance_id based on provided documentation
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer '
                 + "eyJraWQiOiIyMDIxMTAxODA4MTkiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC01NTAwMDQ4TVgyIiwiaWQiOiJJQk1pZC01NTAwMDQ4TVgyIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiZmIyODY5M2MtOWQwOS00ZWRlLTljZGQtNGZmNGRhMDNiZmZiIiwiaWRlbnRpZmllciI6IjU1MDAwNDhNWDIiLCJnaXZlbl9uYW1lIjoiQW5qYWxpIiwiZmFtaWx5X25hbWUiOiJCIiwibmFtZSI6IkFuamFsaSBCIiwiZW1haWwiOiJhbmphbGliYW5rYXB1cjE5OThAZ21haWwuY29tIiwic3ViIjoiYW5qYWxpYmFua2FwdXIxOTk4QGdtYWlsLmNvbSIsImF1dGhuIjp7InN1YiI6ImFuamFsaWJhbmthcHVyMTk5OEBnbWFpbC5jb20iLCJpYW1faWQiOiJJQk1pZC01NTAwMDQ4TVgyIiwibmFtZSI6IkFuamFsaSBCIiwiZ2l2ZW5fbmFtZSI6IkFuamFsaSIsImZhbWlseV9uYW1lIjoiQiIsImVtYWlsIjoiYW5qYWxpYmFua2FwdXIxOTk4QGdtYWlsLmNvbSJ9LCJhY2NvdW50Ijp7ImJvdW5kYXJ5IjoiZ2xvYmFsIiwidmFsaWQiOnRydWUsImJzcyI6IjRjODFjOTYyNjY1YjQ0YzhiZmRiMmRlZDVkZDU2ODBjIiwiZnJvemVuIjp0cnVlfSwiaWF0IjoxNjM1NzQ5Mjk4LCJleHAiOjE2MzU3NTI4OTgsImlzcyI6Imh0dHBzOi8vaWFtLmNsb3VkLmlibS5jb20vaWRlbnRpdHkiLCJncmFudF90eXBlIjoidXJuOmlibTpwYXJhbXM6b2F1dGg6Z3JhbnQtdHlwZTphcGlrZXkiLCJzY29wZSI6ImlibSBvcGVuaWQiLCJjbGllbnRfaWQiOiJkZWZhdWx0IiwiYWNyIjoxLCJhbXIiOlsicHdkIl19.Pqk30cN1sbf1tos53eZb9AewHMTT2zSgL0Z1H28JyDgfja4imK4BZKKhGRByQyuD_z9LdpkJdMsF0p-xLakF9b0oYj09hNJzZQbjmbpg8deIpfu_Nacz4gy5AE6ONnxUgQlIcQYQ6cNUNOlSuGI_I3jOwyjf-cVWuOFg-vgmBuTts09nspk94o-odi1-Wng-4ez17OJNslIsapB1l5aSput8Raqec5vNWBjjLgwtknKqmMUePPkb1WbxCZqu088RtMdLO2JewJ2fFXHTJ8SqH8uCyQjwYtOyp6OOj676mJDb18vMhrZBe5FLvuWA3o0WgEmprHy_6Ad0oshwh15TwQ"}

        if(form.bmi.data == None): 
          python_object = []
        else:
          python_object = [form.age.data, form.sex.data, float(form.bmi.data),
            form.children.data, form.smoker.data, form.region.data]
        #Transform python objects to  Json

        userInput = []
        userInput.append(python_object)

        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        payload_scoring = {"input_data": [{"fields": ["age", "sex", "bmi",
          "children", "smoker", "region"], "values": userInput }]}

        response_scoring = requests.post("https://us-south.ml.cloud.ibm.com/ml/v4/deployments/9ca2cf07-2c5e-406a-b36c-282c34e1d9bf/predictions?version=2020-09-01", json=payload_scoring, headers=header)

        output = json.loads(response_scoring.text)
        print(output)
        for key in output:
          ab = output[key]
        

        for key in ab[0]:
          bc = ab[0][key]
        
        roundedCharge = round(bc[0][0],2)

  
        form.abc = roundedCharge # this returns the response back to the front page
        return render_template('index.html', form=form)