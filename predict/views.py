import os
import joblib
import pandas as pd

from rest_framework.views import APIView
from rest_framework.response import Response

from covid_prediction.settings import BASE_DIR


class Predict(APIView):
    def post(self, request):
        data_dict = request.data
        df = pd.DataFrame(data=data_dict)

        model_path = os.path.join(BASE_DIR, 'predict/models/')
        model = joblib.load(model_path+"random_forest.joblib")
        prediction = model.predict(df)

        response = {
            'corona': prediction[0]
        }

        return Response(response)
