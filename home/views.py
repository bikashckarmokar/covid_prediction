from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response


def index(request):
    return render(request, 'build/index.html')


class Welcome(APIView):
    def get(self, request):
        response = 'Welcome to covid prediction service'
        return Response(response)