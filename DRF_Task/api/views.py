from django.shortcuts import render
from api.models import Book
from api.serializers import BookSerializer
from rest_framework.response import Response
from rest_framework import viewsets,renderers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from api.utils import get_data
from django.views.generic import TemplateView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from .serializers import BookSerializer,UserRegistrationSerializer,LoginSerializer,UserProfileSerializer
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class BookViewSet(viewsets.ViewSet):
    # queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    # filterset_class = BookFilter
    filter_fields = ( 
        'title', 
        'publisher', 
    )
    
    def create(self,request):
        print(request.user.is_author)
        if request.user.is_author:
            data=request.data
            data['author']=request.user.id
            serializer = BookSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'data is created'},status=status.HTTP_201_CREATED)
            return  Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg':'You must login from author account to post book details'})
    
    def list(self, request):
        queryset = Book.objects.all()
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self,request,pk):
        id=pk
        obj=Book.objects.get(id=id)
        serializer=BookSerializer(obj)
        return Response(serializer.data)     
    

    def update(self,request,pk):
        id=pk
        # book_author=Book.objects.filter(id=id).values('name')
        obj=Book.objects.get(pk=id)
        if (request.user.is_author) and (obj.author.name==request.user.name): 
            serializer=BookSerializer(obj,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'data is completely updated'})
        return Response({'msg':'You must login from author account to edit book details'})
    
    def partial_update(self,request,pk):
        id=pk
        obj=Book.objects.get(pk=id)
        if (request.user.is_author) and (obj.author.name==request.user.name):
            serializer=BookSerializer(obj,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'data is partially updated'})
        return Response({'msg':'You must login from author account to edit book details'})
    
    def delete(self,request,pk,format=None):
        id=pk
        obj=Book.objects.get(pk=id)
        if request.user.is_author and (obj.author.name==request.user.name):
            obj.delete()
            return Response({'msg':'data deleted'})
        return Response({'msg':'You must login from author account to delete this book'})

class HomeView(TemplateView):
    model = Book
    template_name = 'api/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = get_data()
        return context
    

class RegisterUser(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({'token':token,'msg':'sign up successful'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        # serializer=UserSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # return Response(serializer.data)
    
class Login(APIView):
    def post(self,request,format=None):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'token':token,'msg':'Login successful'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not valid']}},status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated]
    def get (self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    