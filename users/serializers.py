from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Customuser
from datetime import date

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    # age = serializers.SerializerMethodField()
    foto_url = serializers.SerializerMethodField()

    class Meta:
        model = Customuser
        fields = [
            'id', 'nama_lengkap', 'email', 'password', 'is_admin', 'jabatan',
            'foto', 'foto_url', 'no_hp', 'kantor_cabang', 'gender'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'nama_lengkap': {'required': True},
        }

    # def get_age(self, obj):
    #     if obj.ttl:
    #         today = date.today()
    #         return today.year - obj.ttl.year - ((today.month, today.day) < (obj.ttl.month, obj.ttl.day))
    #     return None

    def get_foto_url(self, obj):
        request = self.context.get('request')
        if obj.foto and hasattr(obj.foto, 'url'):
            return request.build_absolute_uri(obj.foto.url) if request else obj.foto.url
        return ''


    def validate_email(self, value):
        user = self.instance
        if Customuser.objects.filter(email=value).exclude(id=user.id if user else None).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        email = validated_data.get('email')
        user = Customuser.objects.create_user(
            username=email,  # username diisi otomatis dengan email
            email=email,
            password=validated_data['password'],
            nama_lengkap=validated_data.get('nama_lengkap', ''),
            is_admin=validated_data.get('is_admin', False),
            jabatan=validated_data.get('jabatan', ''),
            foto=validated_data.get('foto', None),
            no_hp=validated_data.get('no_hp', ''),
            kantor_cabang=validated_data.get('kantor_cabang', ''),
            gender=validated_data.get('gender', ''),
        )
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data["email"], password=data["password"])
        if user:
            return {
                "user_id": user.id,
                "email": user.email,
                "is_admin": user.is_admin,
            }
        raise serializers.ValidationError("Invalid Credentials")

class UserListSerializer(serializers.ModelSerializer):
    foto_url = serializers.SerializerMethodField()

    class Meta:
        model = Customuser
        fields = [
            'id', 'nama_lengkap', 'email', 'is_admin', 'no_hp', 'jabatan', 'foto_url',
        ]

    def get_foto_url(self, obj):
        request = self.context.get('request')
        if obj.foto and hasattr(obj.foto, 'url'):
            return request.build_absolute_uri(obj.foto.url) if request else obj.foto.url
        return ''
