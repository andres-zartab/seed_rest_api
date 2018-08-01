from jsonschema import validate as json_validate
from jsonschema.exceptions import ValidationError as json_ValidationError

from rest_framework import serializers

from seeds.models import Seed


#NOTE:serializers convert to JSON and validate date passed
class SeedSerializer(serializers.ModelSerializer):
    url         = serializers.SerializerMethodField(read_only=True)
    location    = serializers.JSONField()
    class Meta:
        model = Seed
        fields = [
            'url',
            'pk',
            'user',
            'name',
            'slug',
            'location',
            'picture',
            'active',
            'timestamp',
            'updated',
            'post',
        ]
        #NOTE: The name I give here to the fields is the name that the JSON ends up having
        read_only_fields = ['user']


    def get_url(self, object):
        request = self.context.get('request')
        return object.get_api_url(request=request)

    def validate_location(self, value):
        schema = {
            "type" : "object",
            "properties": {
                "latitude" : {"type" : "number"},
                "name" : {"type": "number"}
            },
            "required" : ["latitude", "longitude"] 
        }
        try:
            json_validate(value, schema)
        except json_ValidationError:
            raise serializers.ValidationError('This is not a valid JSON for geolocation')
        
        #Test for validate JSON
        if value['latitude'] > 4:
            raise serializers.ValidationError('This latitude is out of bounds')
        return value
