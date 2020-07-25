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

        # grade 별 value 리스트 만들기 
        grade_dic = {} 
        total_row_num = len(df.index)
        for i in range(total_row_num):
            data = df.loc[i]
            if not data['grade'] in grade_dic.keys():
                grade_dic[data['grade']] = [data['value']]
            else:
                grade_dic[data['grade']].append(data['value'])
        
        # grade 별 최소value 최대value 평균 구하기 
        grade_calculate_dic = {} 
        for key in grade_dic.keys():
            grade_calculate_dic[key] = {}
            grade_calculate_dic[key]['min'] = min(grade_dic[key])
            grade_calculate_dic[key]['max'] = max(grade_dic[key])
            grade_calculate_dic[key]['avg'] = float(sum(grade_dic[key]) / len(grade_dic[key]))

        # 결과 출력 
        grade_list = list(grade_calculate_dic.keys())
        grade_list.sort() 
        for key in grade_list:
            print("# grade", key)
            print("min: ", grade_calculate_dic[key]['min'], end='')
            print("/ max: ", grade_calculate_dic[key]['max'], end='')
            print("/ avg: ", grade_calculate_dic[key]['avg'], end='\n\n')
        return render(request, 'calculate/calculate_file_upload.html')
    else:
        return render(request, 'calculate/calculate_file_upload.html')

