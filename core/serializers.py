from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password


class UserWriteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["id",
            "email","first_name","last_name","role","profile_picture","bio",
            "phone_number","location","address","city","state","country","company",
            "created_by","date_joined","is_active","is_staff","password",   "full_name", 
        ]
        read_only_fields = ["id", "date_joined", "is_staff", "created_by"]

    def get_full_name(self, obj):
        return obj.get_full_name()

    def create(self, validated_data):
        password = validated_data.pop("password")
        # Use manager to handle password hashing
        return User.objects.create_user(password=password, **validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)  # still needed here for updates
        instance.save()
        return instance

class UserReadSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            "id", "email", "first_name", "last_name", "role",
            "profile_picture", "bio", "phone_number", "location",
            "address", "city", "state", "country", "company",
            "created_by", "created_by_name", "date_joined", "is_active", "is_staff",
            "full_name"
        ]

    def get_full_name(self, obj):
        return obj.get_full_name()
    
    def get_created_by_name(self, obj):
        if obj.created_by: 
            return obj.created_by.get_full_name()
        return None


# class BaseUserRegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only = True, style={'input_type': 'password'})
#     password2 = serializers.CharField(write_only = True, style={'input_type': 'password'})

#     class Meta:
#         model = User 
#         fields =  ['email', 'first_name', 'last_name', 'password', 'password2', 'phone_number']


#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({'password': 'Passwords must match'})
#         return attrs
    
#     def validate_email(self, value):
#         if User.objects.filter(email=value).exists():
#             raise serializers.ValidationError('This email already exist')
#         return value
    





# class UserLoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')

#         user = authenticate(email=email, password=password)
#         if not user:
#             raise serializers.ValidationError(
#                 {"error": "Invalid email or password. Please try again."},  # Custom message
#                  # Optional: custom error code
#             )
#         refresh = RefreshToken.for_user(user)

#         return {
#             'user': {
#                 'id': user.id,
#                 'first_name': user.first_name,
#                 'last_name': user.last_name,
#                 'email': user.email,
#                 'role': user.role,
#             },
#             'access': str(refresh.access_token),
#             'refresh': str(refresh),
#         }


class UserUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False, max_length=50)
    last_name = serializers.CharField(required=False, max_length=50)
    email = serializers.EmailField(read_only=True)  
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    bio = serializers.CharField(required=False, allow_blank=True, max_length=300)
    phone_number = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )
    location = serializers.CharField(required=False, allow_blank=True, max_length=100)
    address = serializers.CharField(required=False, allow_blank=True, max_length=200)
    city = serializers.CharField(required=False, allow_blank=True, max_length=50)
    state = serializers.CharField(required=False, allow_blank=True, max_length=50)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "profile_picture",
            "bio",
            "phone_number",
            "location",
            "address",
            "city",
            "state",
        ]

    # Custom validation for names
    def validate_first_name(self, value):
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError("First name cannot contain numbers.")
        return value

    def validate_last_name(self, value):
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError("Last name cannot contain numbers.")
        return value

    # Example: If both city and state are given, require consistency
    def validate(self, data):
        city = data.get("city")
        state = data.get("state")
        if city and not state:
            raise serializers.ValidationError({"state": "State is required if city is provided."})
        return data


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(
        write_only=True, 
        required=True,
        validators=[validate_password],
        style={"input_type": "password"}
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")
        return value

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user


# --- Custom Token Serializer to include user info ---
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Include user info in response
        data.update({
            "user": {
                "id": self.user.id,
                "email": self.user.email,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "role": self.user.role,
            }
        })
        return data