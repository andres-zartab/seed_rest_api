from rest_framework import serializers

from seeds.models import Seed


#NOTE:serializers convert to JSON and validate date passed
class SeedSerializer(serializers.ModelSerializer):
    url         = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Seed
        fields = [
            'url',
            'pk',
            'user',
            'name',
            'slug',
            'gps_lat',
            'gps_lon',
            #'picture',
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

    def validate_gps_lat(self, value):
        if value < 4:
            raise serializers.ValidationError('This latitude is out of bounds')
        return value

    def validate_gps_lon(self, value):
        if value > -50:
            raise serializers.ValidationError('This longitutde is out of bounds')
        return value