from api.models import Book, Favourite, Cart
from django.contrib.auth import authenticate
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    BookAuthorDetail,
    BookSerializer,
    FavouriteSerializer,
    LoginSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
    CartSerializer,
)

# Create your views here.


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class BookViewSet(viewsets.ViewSet):
    serializer_class = BookSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        if request.user.is_author:
            data = request.data.copy()
            data["author"] = request.user.id
            serializer = BookSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"msg": "data is created"}, status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"msg": "You must login from author account to post book details"},
            status=status.HTTP_200_OK,
        )

    def list(self, request):
        print(request.query_params.get("title"))
        queryset = Book.objects.all()
        if request.query_params.get("title"):
            queryset = Book.objects.filter(title=request.query_params.get("title"))
        elif request.query_params.get("author"):
            queryset = Book.objects.filter(
                author__name=request.query_params.get("author")
            )

        serializer = BookAuthorDetail(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        id = pk
        obj = Book.objects.get(id=id)
        serializer = BookAuthorDetail(obj)
        return Response(serializer.data)

    def update(self, request, pk):
        id = pk
        obj = Book.objects.get(pk=id)
        if (request.user.is_author) and (obj.author.name == request.user.name):
            serializer = BookSerializer(obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"msg": "data is completely updated"})
        return Response(
            {"msg": "You must login from author account to edit book details"}
        )

    def partial_update(self, request, pk):
        id = pk
        obj = Book.objects.get(pk=id)
        if (request.user.is_author) and (obj.author.name == request.user.name):
            serializer = BookSerializer(obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"msg": "data is partially updated"})
        return Response(
            {"msg": "You must login from author account to edit book details"}
        )

    def delete(self, request, pk, format=None):
        id = pk
        obj = Book.objects.get(pk=id)
        if request.user.is_author and (obj.author.name == request.user.name):
            obj.delete()
            return Response({"msg": "data deleted"})
        return Response(
            {"msg": "You must login from author account to delete this book"}
        )

    @action(
        detail=True,
        methods=["post", "get"],
        permission_classes=[IsAuthenticated],
        authentication_classes=[JWTAuthentication],
    )
    def add_to_favourite(self, request, pk):
        id = pk
        if request.method == "POST":
            book = Book.objects.get(pk=id)
            user = request.user
            favourite, created = Favourite.objects.get_or_create(user=user, book=book)
            if created:
                return Response(
                    {"status": "book added to favourites"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"status": "book already in favourites"}, status=status.HTTP_200_OK
                )
        elif request.method == "GET":
            user = request.user
            favourites = Favourite.objects.filter(user=user)
            serializer = FavouriteSerializer(favourites, many=True)
            return Response(serializer.data)

    @action(
        detail=True,
        methods=["post", "get"],
        permission_classes=[IsAuthenticated],
        authentication_classes=[JWTAuthentication],
    )
    def add_to_cart(self, request, pk):
        id = pk
        if request.method == "POST":
            book = Book.objects.get(pk=id)
            user = request.user
            cart_item, created = Cart.objects.get_or_create(user=user, book=book)
            if created:
                return Response(
                    {"status": "book added to favourites"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"status": "book already in favourites"}, status=status.HTTP_200_OK
                )
        elif request.method == "GET":
            user = request.user
            cart_items = Cart.objects.filter(user=user)
            serializer = CartSerializer(cart_items, many=True)
            return Response(serializer.data)


class RegisterUser(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response(
                {"token": token, "msg": "sign up successful"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response(
                    {"token": token, "msg": "Login successful"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "errors": {
                            "non_field_errors": ["Email or Password is not valid"]
                        }
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
