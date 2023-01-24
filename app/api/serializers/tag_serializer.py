from rest_framework import serializers

from ..models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = ('created_with_user_agent',)


class TagPostSerializer(TagSerializer):
    pass


class TagRetrieveSerializer(TagSerializer):
    pass


class TagListSerializer(serializers.ModelSerializer):
    editable = serializers.SerializerMethodField('is_editable')

    def is_editable(self, current_object: Tag):
        request = self.context.get('request', None)
        if request:
            return request.user is not None and request.user == current_object.created_by
        return False

    class Meta:
        model = Tag
        fields = ('id', 'name', 'editable')


class TagGetShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class TagOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id',)
        