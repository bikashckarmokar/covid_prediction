from rest_framework.views import APIView
from rest_framework.response import Response


class Welcome(APIView):
    def get(self, request):
        response = 'Welcome to covid prediction service'
        return Response(response)