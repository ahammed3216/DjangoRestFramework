from django.shortcuts import render
from django.http import HttpResponse ,JsonResponse
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated

#Generic Based  views

class GenericApiView(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,mixins.RetrieveModelMixin):

    #authentication_classes=[SessionAuthentication,BasicAuthentication]
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class=ArticleSerializers

    lookup_field='id'
    queryset = Article.objects.all()


    def get(self,request,id=None):
        queryset = Article.objects.all()
        if id:
            return self.retrieve(request)
        else:
            return self.list(queryset)

    def post(self,request):
        return self.create(request)

    def put(self,request,id):
        return self.update(request)

    def delete(self,request,id):
        return self.destroy(request)

#class Based API view

class ArticleView(APIView):

    def get(self,request):

        articles=Article.objects.all()
        serializer=ArticleSerializers(articles,many=True)

        return Response(serializer.data)
    
    def post(self,request):

        serializers=ArticleSerializers(data=request.data)

        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)

        else:
            return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailView(APIView):

    def get_object(self,id):
         try:
            article=Article.objects.get(id=id)
            return article

         except Article.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
            
        

    def get(self,request,id):
        article=self.get_object(id)
        serializer=ArticleSerializers(article)
        return Response(serializer.data)

    def put(self,request,id):
        article=self.get_object(id)
        serializer=ArticleSerializers(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        article=self.get_object(id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)








# Create your views here.

#@csrf_exempt
@api_view(['GET','POST'])
def articlelist(request):
    if request.method== 'GET':
        articles=Article.objects.all()
        serializer=ArticleSerializers(articles,many=True)
        #return JsonResponse(serializer.data,safe=False)
        return Response(serializer.data)

    elif request.method=='POST':
        serializers=ArticleSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)

        else:
            return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

#@csrf_exempt
@api_view(['GET','PUT','DELETE'])
def article_detail(request,id):
    try:
        article=Article.objects.get(id=id)

    except Article.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method=='GET':
        serializer=ArticleSerializers(article)
        return Response(serializer.data)

    if request.method=='PUT':
        #data=JSONParser().parse(request)
        serializer=ArticleSerializers(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    elif request.method=="DELETE":
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
