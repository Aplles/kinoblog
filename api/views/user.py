from rest_framework.response import Response
from rest_framework.views import APIView
from api.service.user.login import UserLoginService
from api.service.user.create import UserCreateService
from api.serializers.user.show import UserShowSerializer


class UserLoginView(APIView):
    def post(self, request):
        """ Авторизация пользователя """
        outcome = UserLoginService.execute(request.POST)
        return Response(
            {
                "auth_token": outcome.result
            }
        )


class UserCreateView(APIView):
    def post(self, request):
        """ Создание пользователя """
        outcome = UserCreateService.execute(request.POST)
        return Response(
            UserShowSerializer(outcome.result).data
        )

