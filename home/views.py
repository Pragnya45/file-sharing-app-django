from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *
from rest_framework.parsers import MultiPartParser
from django.http import FileResponse, Http404
import os, zipfile
from django.conf import settings

def generate_zip(uid):
    zip_dir = os.path.join(settings.BASE_DIR, 'public/static/zip')
    os.makedirs(zip_dir, exist_ok=True)

    zip_path = os.path.join(zip_dir, f"{uid}.zip")
    if not os.path.exists(zip_path):
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.writestr("README.txt", f"Generated ZIP for UID: {uid}")

    return zip_path


def stream_zip_file(request, uid):
    try:
        zip_path = generate_zip(uid)
        return FileResponse(open(zip_path, 'rb'), as_attachment=True, filename=f"{uid}.zip")
    except FileNotFoundError:
        raise Http404("ZIP file not found")


def home(request):
    return render(request ,'home.html')



def download(request , uid):
    return render(request , 'download.html' , context = {'uid' : uid})

class HandleFileUpload(APIView):
    parser_classes = [MultiPartParser]
    def post(self , request):
        try:
            data = request.data
            if 'files' not in data:
                return Response({
                    'status' : 400,
                    'message' : 'No files provided',
                    'data' : {}
                })
            serializer = FileListSerializer(data = data)
        
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status' : 200,
                    'message' : 'files uploaded successfully',
                    'data' : serializer.data
                })
            
            return Response({
                'status' : 400,
                'message' : 'somethign went wrong',
                'data'  : serializer.errors
            })
        except Exception as e:
            print(e)
            return Response({
                'status': 500,
                'message': 'Internal server error',
                'error': str(e)
            })