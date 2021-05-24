import os
import joblib
import pandas as pd

from rest_framework.views import APIView
from rest_framework.response import Response

from covid_prediction.settings import BASE_DIR
from .models import History


class HistoryData(APIView):
    def get(self, request):
        history_data = History.objects.all()
        data = {

        }
        for hist in history_data:
            print(hist)
        history_response = {'history_data': history_data}

        return Response(history_response)


class Predict(APIView):
    def post(self, request):
        data_dict = request.data
        df = pd.DataFrame(data=data_dict['symptoms'])
        personal_info_dict = data_dict['personal_info']

        model_path = os.path.join(BASE_DIR, 'predict/ml_models/')
        model = joblib.load(model_path+"random_forest.joblib")
        prediction = model.predict(df)

        response = {
            'corona': prediction[0]
        }

        personal_info_dict['corona'] = bool(prediction[0])

        hist_data = History.objects.create(
            name=personal_info_dict['name'],
            email=personal_info_dict['email'],
            mobile=personal_info_dict['mobile'],
            corona='Positive' if personal_info_dict['mobile'] else 'Negative'
        )

        return Response(response)
