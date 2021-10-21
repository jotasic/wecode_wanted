from django.conf                import settings
from django.contrib.auth        import get_user_model
from rest_framework.serializers import ModelSerializer


class RegisterUserSerializer(ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = '__all__'
        read_only_fields = ('is_staff', 'date_of_join', 'last_login', 'is_admin', 'id')
        extra_kwargs = {'password' : {'write_only' : True}}

    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)