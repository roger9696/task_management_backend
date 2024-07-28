
from rest_framework.views import APIView
from .serializers import Userserializer, TaskSerializer
from rest_framework.response import Response
from .models import User, Task
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from datetime import datetime, timezone
from rest_framework import generics



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
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(' ')[1]  # Extract the token
            try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
                user = User.objects.filter(id=payload['id']).first()
                serializer = Userserializer(user)
                return Response(serializer.data)
            except jwt.ExpiredSignatureError:
                return Response({'error': 'Token has expired'})
        return Response({'error': 'Token is missing or invalid'})



# class UserView(APIView):
#   def get(self, request):
#     token = request.headers.get('Authorization')

#     print(token)

#     if not token:
#       raise AuthenticationFailed('UnAuthenticated (no-token)')  
    
#     try:
#        payload = jwt.decode(token, 'secret', algorithms=['HS256'])

#     except jwt.ExpiredSignatureError:
#        raise AuthenticationFailed('UnAuthenticated(token expired)')


#     user = User.objects.filter(id=payload['id']).first()
#     serializer = Userserializer(user)

#     return Response(serializer.data)



class LogoutView(APIView):
  def post(self, request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
      'message': 'success'
    }
    return response
  



class TaskCreatView(generics.ListCreateAPIView):
   queryset = Task.objects.all()
   serializer_class = TaskSerializer


class TaskRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
   queryset = Task.objects.all()
   serializer_class = TaskSerializer
   lookup_field = 'pk'