from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View, TemplateView
import random
import json
# Create your views here.
class MyAjaxForms(View):
    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            numbers = random.randint(1, 10)
            return JsonResponse({'numbers': numbers})
        return render(request, 'pract/ajaxForm.html')
    
    # def post(self, request):
    #     data = json.loads(request.body)
    #     float_num = float(data['number'])
    #     return JsonResponse({'float': f'You got: {float_num}'})

    def post(self, request):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # print("---Incoming Reguest----")
            # print(request.headers)
            # print(request.content_type)
            # print(request.POST)
            # print(request.body)
            data= json.loads(request.body)
            print(data)
            return JsonResponse({'info': 'success'})
        return JsonResponse({'error': 'ajax failed'})