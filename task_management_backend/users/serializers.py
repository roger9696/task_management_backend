from rest_framework import serializers
from .models import User, Task

class Userserializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'first_name', 'last_name', 'email', 'password','is_superuser']
    extra_kwargs = {
      'password': {'write_only': True}
    }

  def create(self, validated_data):
    password = validated_data.pop('password', None)
    instance = self.Meta.model(**validated_data)
    if password is not None:
      instance.set_password(password)
    instance.save()
    return instance
  
class TaskSerializer(serializers.ModelSerializer):
  class Meta:
    model = Task
    fields = '__all__'