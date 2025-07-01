from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Customuser
from datetime import date

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    age = serializers.SerializerMethodField()
    foto_url = serializers.SerializerMethodField()

    class Meta:
        model = Customuser
        fields = [
            'id', 'fullname', 'username', 'email', 'password', 'is_admin', 'divisi', 'jabatan',
            'foto', 'foto_url', 'no_hp', 'alamat', 'office_branch', 'gender', 'ttl', 'age'
        ]
        extra_kwargs = {
            'username': {'validators': []},
            'email': {'required': True},
        }

    def get_age(self, obj):
        if obj.ttl:
            today = date.today()
            return today.year - obj.ttl.year - ((today.month, today.day) < (obj.ttl.month, obj.ttl.day))
        return None

    def get_foto_url(self, obj):
        request = self.context.get('request')
        if obj.foto and hasattr(obj.foto, 'url'):
            return request.build_absolute_uri(obj.foto.url) if request else obj.foto.url
        return ''

    def validate_username(self, value):
        user = self.instance
        if Customuser.objects.filter(username=value).exclude(id=user.id if user else None).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        user = self.instance
        if Customuser.objects.filter(email=value).exclude(id=user.id if user else None).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        is_admin = validated_data.get('is_admin', False)
        user = Customuser.objects.create_user(
            fullname=validated_data['fullname'],
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            divisi=validated_data.get('divisi', ''),
            jabatan=validated_data.get('jabatan', ''),
            foto=validated_data.get('foto', None),
            no_hp=validated_data.get('no_hp', ''),
            alamat=validated_data.get('alamat', ''),
            office_branch=validated_data.get('office_branch', ''),
            gender=validated_data.get('gender', ''),
            ttl=validated_data.get('ttl', None),
        )
        user.is_admin = is_admin
        if is_admin:
            user.is_staff = True
        user.save()
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
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if user:
            return {
                "user_id": user.id,
                "username": user.username,
                "is_admin": user.is_admin,
            }
        raise serializers.ValidationError("Invalid Credentials")

class UserListSerializer(serializers.ModelSerializer):
    foto_url = serializers.SerializerMethodField()

    class Meta:
        model = Customuser
        fields = [
            'id', 'fullname', 'username', 'email', 'is_admin', 'no_hp', 'jabatan', 'foto_url',
            # tambahkan field lain jika perlu
        ]

    def get_foto_url(self, obj):
        request = self.context.get('request')
        if obj.foto and hasattr(obj.foto, 'url'):
            return request.build_absolute_uri(obj.foto.url) if request else obj.foto.url
        return ''
