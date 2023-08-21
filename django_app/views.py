from django.shortcuts import render
from .models import Student
from .serializers import StudentSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt 
from django.http import HttpResponse
import io

# Create your views here.

def index(request):
    return render(request, 'index.html')

def Student_details(request, pk):
    stu = Student.objects.get(id = pk)
    serialier = StudentSerializer(stu)
    json_data = JSONRenderer().render(serialier.data)
    return HttpResponse (json_data, content_type='application/json')

def Student_list(request):
    stu = Student.objects.all()
    serialier = StudentSerializer(stu, many = True)
    json_data = JSONRenderer().render(serialier.data)
    return HttpResponse (json_data, content_type='application/json')

@csrf_exempt
def Student_create(request):
    if request.method == "POST":
        json_data = request.body
        stream = io.BytesIO(json_data) 
        pythondata = JSONParser().parse(stream)
        serializer = StudentSerializer(data=pythondata)
        if serializer.is_valid():
            serializer.save()
            res = {'msg' : 'data inserted....'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type="application/json")
