import requests, jwt

from rest_framework.views import APIView
from django.http  import JsonResponse
from django.conf  import settings
from users.models import User

class KakaoLogInView(APIView):
    def post(self, request):
        try: 
            kakao_access_token  = request.headers.get('Authorization')
            kakao_user_api      = 'https://kapi.kakao.com/v2/user/me' 
            kakao_user_response = requests.get(kakao_user_api, headers={'Authorization' : f'Bearer {kakao_access_token}'}).json()   
            kakao_id            = kakao_user_response['id']
            nickname            = kakao_user_response['kakao_account']['profile']['nickname']
            email               = kakao_user_response['kakao_account']['email']

            if not User.objects.filter(kakao_id = kakao_id).exists():
                user = User.objects.create(
                    kakao_id  = kakao_id,
                    nickname  = nickname,
                    email     = email
                )
            else:
                user = User.objects.get(kakao_id = kakao_id)
            
            user, is_created = User.objects.get_or_create(
                kakao_id = kakao_id,
                defaults = {
                    nickname : nickname,
                    email    : email
                }
            )

            access_token = jwt.encode({'id':user.id}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
            return JsonResponse({'message':'SUCCESS', 'access_token': access_token, 'nickname': nickname}, status=200)
        except KeyError:
                return JsonResponse({'message':'KEY_ERROR'}, status = 400)
