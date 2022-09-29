from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import Admin, Superuser
from .serializers import (UserSelfSerializer, UserSerializer,
                          UserSignUpSerializer)
from .services import check_token, generate_token

User = get_user_model()


@api_view(['POST'])
def sign_up(request):
    serializer = UserSerializer(data=request.data)
    email = request.data.get('email')
    user = User.objects.filter(email=email)

    if user.exists():
        user = user.get(email=email)
        generate_token(user)
        return Response(
            {'message': 'Пользователь с такой электронной почтой уже '
                        'существует. Код подтверждения отправлен повторно. '
             },
            status=status.HTTP_400_BAD_REQUEST
        )

    else:
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        user, created = User.objects.get_or_create(username=username,
                                                   email=email)
        generate_token(user)
        token = generate_token(user)
        send_mail(
            'Yamdb confirmation code',
            f'{token}',
            settings.AUTH_EMAIL,
            [f'{email}']
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def retrieve_token(request):
    serializer = UserSignUpSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = get_object_or_404(User, username=request.data.get('username'))
        if check_token(user, request.data.get('confirmation_code')):
            access = AccessToken.for_user(user)
            return Response(
                {
                    'token': str(access)
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'confirmation_code': 'Confirmation code is invalid'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    return 'Something wrong'


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [Admin | Superuser]
    lookup_field = 'username'
    pagination_class = PageNumberPagination

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = request.user
        serializer_class = UserSelfSerializer

        if request.method == 'GET':
            serializer = serializer_class(user)
            return Response(serializer.data)

        serializer = serializer_class(user, partial=True, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)
