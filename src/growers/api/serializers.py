from rest_framework import serializers

from django.contrib.auth.models import User


#NOTE:serializers convert to JSON and validate date passed
class GrowerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'username',
            'pk',
        ]
        