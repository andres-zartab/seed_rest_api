from rest_framework import serializers

from plants.models import Plant


#NOTE:serializers convert to JSON and validate date passed
class PlantSerializer(serializers.ModelSerializer):
    url         = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Plant
        fields = [
            'url',
            'pk',
            'seed',
            'name',
            'about',
            'category',
            'slug',
            #'picture',
            'active',
            'timestamp',
            'updated',
        ]
        #NOTE: The name I give here to the fields is the name that the JSON ends up having
        #read_only_fields = ['user']

    def get_url(self, object):
        request = self.context.get('request')
        return object.get_api_url(request=request)
    

    # def validate_gps_lat(self, value):
    #     if value < 4:
    #         raise serializers.ValidationError('This latitude is out of bounds')
    #     return value
