from rest_framework import serializers

from seed_app.models import Seed

class SeedSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Seed
        fields = [
            'uri',
            'id',
            'user',
            'title',
            'content',
            'timestamp',
        ]
        read_only_fields = ['id', 'user'] 
    
    def get_uri(self, obj):
        request = self.context.get('request')
        return obj.get_api_uri(request=request)

    def validate_title(self, value):
        qs = Seed.objects.filter(title__exact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('This title malready exists')
        return value
