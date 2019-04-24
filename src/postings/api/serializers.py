from rest_framework import serializers

from postings.models import BlogPost

#NOTE:serializers convert to JSON and validate date passed
class BlogPostSerializer(serializers.ModelSerializer):
    url         = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = BlogPost
        fields = [
            'url',
            'pk',
            'user',
            'title',
            'content',
            'timestamp',
        ]
        #NOTE: The name I give here to the fields is the name that the JSON ends up having
        read_only_fields = ['user']

    def get_url(self, object):
        request = self.context.get('request')
        return object.get_api_url(request=request)

    def validate_title(self, value):
        qs = BlogPost.objects.filter(title__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('This title has already been used')
        return value