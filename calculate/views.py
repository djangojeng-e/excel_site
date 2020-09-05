from django.shortcuts import render, redirect
from django.http import HttpResponse
import pandas as pd 
from .models import Document
import datetime
import os

# Create your views here.


def download(request):
    path = request.GET['path']
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    if os.path.exists(file_path):
        binary_file = open(file_path, 'rb')
        response = HttpResponse(binary_file.read(), contet_type="application/liquid; charset=utf-8")
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response

    else:
        message = '알수 없는 오류가 발생했습니다'
        return render(request, 'main/error.html', {"message": message}) 


def calculate(request):
    file = request.FILES['fileInput']
    # print('# 사용자가 등록한 파일의 이름: ', file)
    # 파일 저장하기 
    origin_file_name = file.name 
    user_name = request.session['user_name']
    now_HMS = datetime.today().strftime('%H%M%S')
    file_upload_name = now_HMS + '_' + user_name + '_' + origin_file_name
    file.name = file_upload_name
    document = Document(user_upload_file = file)
    document.save() 

    if request.method == "POST": 
        file = request.FILES['fileInput']
        print("# 사용자가 등록한 파일의 이름 : ",  file)
        df = pd.read_excel(file, sheet_name='Sheet1', header=0)
        print(df.head(5))

        # grade 별 value 리스트 만들기 
        grade_dic = {} 
        total_row_num = len(df.index)
        for i in range(total_row_num):
            print(i)
            data = df.loc[i]
            if not data['grade'] in grade_dic.keys():
                grade_dic[data['grade']] = [data['value']]
            else:
                grade_dic[data['grade']].append(data['value'])
        
        # grade 별 최소value 최대value 평균 구하기 
        grade_calculate_dic = {} 
        for key in grade_dic.keys():
            grade_calculate_dic[key] = {}
            print(grade_calculate_dic)
            grade_calculate_dic[key]['min'] = min(grade_dic[key])
            grade_calculate_dic[key]['max'] = max(grade_dic[key])
            grade_calculate_dic[key]['avg'] = float(sum(grade_dic[key]) / len(grade_dic[key]))
        print(grade_calculate_dic)

        # 결과 출력 
        grade_list = list(grade_calculate_dic.keys())
        grade_list.sort() 
        for key in grade_list:
            print("# grade", key)
            print("min: ", grade_calculate_dic[key]['min'], end='')
            print("/ max: ", grade_calculate_dic[key]['max'], end='')
            print("/ avg: ", grade_calculate_dic[key]['avg'], end='\n\n')
        
        # 이메일 주소 도메인별 인원 구하기 
        email_domain_dic = {}
        for i in range(total_row_num):
            data = df.loc[i]
            email_domain = (data['email'].split("@"))[1]
            if not email_domain in email_domain_dic.keys():
                email_domain_dic[email_domain] = 1
            else:
                email_domain_dic[email_domain] += 1
        print("## EMAIL 도메인별 사용 인원")
        for key in email_domain_dic.keys():
            print("#", key, ": ", email_domain_dic[key], "명")
        # return render(request, 'calculate/calculate_file_upload.html')
        grade_calculate_dic_to_session = {}
        for key in grade_list:
            grade_calculate_dic_to_session[int(key)] = {}
            grade_calculate_dic_to_session[int(key)]['max'] = float(grade_calculate_dic[key]['max'])
            grade_calculate_dic_to_session[int(key)]['avg'] = float(grade_calculate_dic[key]['avg'])
            grade_calculate_dic_to_session[int(key)]['min'] = float(grade_calculate_dic[key]['min'])
        request.session['grade_calculate_dic'] = grade_calculate_dic_to_session
        request.session['email_domain_dic'] = email_domain_dic
        return redirect('/result')
    else:
        return render(request, 'calculate/calculate_file_upload.html')


def result(request):
    if 'user_name' in request.session.keys():
        content = {}
        content['grade_calculate_dic'] = request.session['grade_calculate_dic']
        content['email_domain_dic'] = request.session['email_domain_dic']
        del request.session['grade_calculate_dic']
        del request.session['email_domain_dic']
        return render(request, 'main/result.html', content)
    else:
        return redirect('main_signin')




