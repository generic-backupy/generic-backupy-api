from rest_framework import serializers

from ..models.secret import Secret


class SecretRetrieveSerializer(serializers.ModelSerializer):
    secret = serializers.SerializerMethodField('get_secret')

    def get_secret(self, current_object: Secret):
        return "******"

    class Meta:
        model = Secret
        fields = ('id', 'name', 'description', 'secret')


class SecretSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secret
        fields = ('id', 'name', 'description', 'secret')


class SecretGbModuleSerializer(SecretSerializer):
    pass


class SecretPostSerializer(SecretSerializer):
    pass


class SecretBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secret
        fields = ('id', 'name')


class SecretListSerializer(SecretBaseSerializer):

    pass


class SecretGetShortSerializer(SecretBaseSerializer):
    pass


class SecretOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secret
        fields = ('id',)
