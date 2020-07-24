from django.shortcuts import render, redirect
from django.http import HttpResponse
import pandas as pd 

# Create your views here.


def calculate(request):
    if request.method == "POST": 
        file = request.FILES['fileInput']
        print("# 사용자가 등록한 파일의 이름 : ",  file)
        df = pd.read_excel(file, sheet_name='Sheet1', header=0)
        print(df.head(5))
        return render(request, 'calculate/calculate_file_upload.html')
    else:
        return render(request, 'calculate/calculate_file_upload.html')

