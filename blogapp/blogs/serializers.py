from rest_framework import serializers
from .models import Blogs,Tags


class BlogSerializer(serializers.ModelSerializer):

    tags = serializers.ListField(child=serializers.CharField(max_length=20),write_only=True)

    def create(self, validated_data):
        tags_data = validated_data.pop('tags',[])
        blog = Blogs.objects.create(**validated_data,tags=tags_data)

        # for tag in tags_data:
        #     Tags.objects.create(tag=tag, blog=blog)
    class Meta:
        model = Blogs
        fields = ('title','content', 'isDraft')