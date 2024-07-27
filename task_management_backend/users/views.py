
from rest_framework.views import APIView
from .serializers import Userserializer
from rest_framework.response import Response
from .models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from datetime import datetime, timezone



# Create your views here.

class RegisterView(APIView):
  def post(self, request):
    serializer = Userserializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)



class LoginView(APIView):
  def post(self, request):
    email = request.data['email']
    password = request.data['password']

    user = User.objects.filter(email=email).first()

    if user is None:
      raise AuthenticationFailed('user not found')
    
    if not user.check_password(password):
      raise AuthenticationFailed('incorrect password')
    
    payload = {
      'id': (user.id),
      'exp': datetime.now(timezone.utc).timestamp() + 60 * 60,
      'iat': datetime.now(timezone.utc).timestamp()

    }

    token = jwt.encode(payload, 'secret', algorithm='HS256')

    response = Response()
    
    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {
      'jwt': token
    }

    return response


class UserView(APIView):
  def get(self, request):
    token = request.COOKIES.get('jwt')

    if not token:
      raise AuthenticationFailed('UnAuthenticated (no-token)')  
    
    try:
       payload = jwt.decode(token, 'secret', algorithms=['HS256'])

    except jwt.ExpiredSignatureError:
       raise AuthenticationFailed('UnAuthenticated(token expired)')


    user = User.objects.filter(id=payload['id']).first()
    serializer = Userserializer(user)

    return Response(serializer.data)



class LogoutView(APIView):
  def post(self, request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
      'message': 'success'
    }
    return response
  