from core.serializers import BaseUserRegistrationSerializer
from rest_framework import serializers
from core.models import User, UserRole
from .models import Inspector, Admin, Worker, Client


# INSPECTOR REGISTRATION
class InspectorRegistrationSerializer(BaseUserRegistrationSerializer):
    qualification = serializers.CharField(write_only=True)
    years_of_experience = serializers.IntegerField(write_only=True)

    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = BaseUserRegistrationSerializer.Meta.fields + ['qualification', 'years_of_experience']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data.pop('password2')
        
        inspector_data = {
            'years_of_experience': validated_data.pop('years_of_experience', 0),
        }

        # Set qualification on User
        validated_data['qualification'] = validated_data.pop('qualification', '')

        user = User.objects.create_user(
            **validated_data,
            role='inspector',
            created_by=request.user if request and request.user.is_authenticated else None,
        )

        inspector = Inspector.objects.create(
            inspector=user,
            **inspector_data
        )

        # Return both user and inspector
        return {'user': user, 'inspector': inspector}

    def validate(self, attrs):
        attrs['role'] = 'inspector'  # Ensure role is always set to inspector
        return attrs
    
# ADMIN REGISTRATION
class AdminRegistrationSerializer(BaseUserRegistrationSerializer):
    office_location = serializers.CharField(write_only=True)
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = BaseUserRegistrationSerializer.Meta.fields + ['office_location']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data.pop('password2')

        # Extract admin fields
        admin_data = {
            'office_location': validated_data.pop('office_location'),
        }

        # validated_data['role'] = 'admin'  # Ensure role is always set to admin
        def validate(self, attrs):
            attrs = super().validate(attrs)
            attrs['role'] = 'admin'  # Role set here
            return attrs
        
        user = User.objects.create_user(
            **validated_data,
            # role='admin',
            created_by = request.user if request and request.user.is_authenticated else None,
        )

        admin = Admin.objects.create(
            admin=user,
            **admin_data
        )

        # Return both user and inspector
        return {'user': user, 'admin': admin}
    
    
    
    # def to_representation(self, instance):
    #     if isinstance(instance, dict):  # Handle the {'user': user, 'admin': admin} case
    #         return AdminReadSerializer(instance['admin']).data
    #     return super().to_representation(instance)
   

# WORKER REGISTRATION
class WorkerRegistrationSerializer(BaseUserRegistrationSerializer):
    department = serializers.ChoiceField(
        choices=Worker.DEPARTMENT_CHOICES,
        write_only=True
    )
    shift_type = serializers.ChoiceField(
        choices=Worker.SHIFT_CHOICES,
        write_only=True
    )
    shift_time = serializers.TimeField(
        write_only=True,
        required=False,
        allow_null=True
    )
    next_shift_start = serializers.DateTimeField(
        write_only=True,
        required=False,
        allow_null=True
    )
    hire_date = serializers.DateField(
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = BaseUserRegistrationSerializer.Meta.fields + [
            'department',
            'shift_type',
            'shift_time',
            'next_shift_start',
            'hire_date'
        ]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs['role'] = UserRole.WORKER  # Use enum for consistency
        return attrs
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data.pop('password2', None)  # Safer pop with default
        
        # Extract all worker-specific fields at once
        worker_fields = [
            'department', 'shift_time', 'shift_type',
            'next_shift_start', 'hire_date'
        ]
        worker_data = {
            field: validated_data.pop(field, None)
            for field in worker_fields
        }

        user = User.objects.create_user(
            **validated_data,  # role is included from validate()
            created_by=request.user if request and request.user.is_authenticated else None,
        )

        worker = Worker.objects.create(
            worker=user,
            **worker_data
        )

        return {'user': user, 'worker': worker}
   


# CLIENT REGISTRATION
class ClientRegistrationSerializer(BaseUserRegistrationSerializer):
    age = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    company_name = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = BaseUserRegistrationSerializer.Meta.fields + [
            'age', 'company_name',
        ]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs['role'] = UserRole.CLIENT
        return attrs
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data.pop('password2', None)
        
        client_data = {
            'age': validated_data.pop('age', ''),
            'company_name': validated_data.pop('company_name', ''),
        }

        user = User.objects.create_user(
            **validated_data,  # role is included from validate()
            created_by=request.user if request and request.user.is_authenticated else None,
        )

        client = Client.objects.create(
            client=user,
            **client_data
        )

        return {'user': user, 'client': client}
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'role', 'profile_picture', 'bio', 'phone_number', 'is_verified', 'rating', 'is_active', 'created_by', 'date_joined', 'is_staff']
    
    def validate_role(self, value):
        if value not in [role.value for role in UserRole]:
            raise serializers.ValidationError("Invalid user role")
        return value
    
    def get_full_name(self, obj):
        return obj.get_full_name()


# READ SERIALIZERS 
class InspectorReadSerializer(serializers.ModelSerializer):
    inspector = UserSerializer()
    class Meta:
        model = Inspector
        fields = ['inspector', 'years_of_experience']

# class InspectorReadSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(source='inspector.email')
#     first_name = serializers.CharField(source='inspector.first_name')
#     last_name = serializers.CharField(source='inspector.last_name')
#     qualification = serializers.CharField(source='inspector.qualification')
    
#     class Meta:
#         model = Inspector
#         fields = ['id', 'email', 'first_name', 'last_name', 
#                  'qualification', 'years_of_experience']

class AdminReadSerializer(serializers.ModelSerializer):
    admin = UserSerializer()
    class Meta:
        model = Admin
        fields = ['admin', 'office_location',]

class WorkerReadSerializer(serializers.ModelSerializer):
    worker = UserSerializer()
    class Meta:
        model = Worker
        fields = ['worker', 'department', 'shift_time']

class ClientReadSerializer(serializers.ModelSerializer):
    client = UserSerializer()
    class Meta:
        model = Client
        fields = ['client', 'age', 'company_name']

# class ClientReadSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(source='client.email')
#     first_name = serializers.CharField(source='client.first_name')
#     last_name = serializers.CharField(source='client.last_name')
#     phone_number = serializers.CharField(source='client.phone_number')
#     profile_picture = serializers.ImageField(source='client.profile_picture')
#     is_active = serializers.BooleanField(source='client.is_active')

#     class Meta:
#         model = Client
#         fields = [
#             'id',
#             'email',
#             'first_name',
#             'last_name',
#             'phone_number',
#             'profile_picture',
#             'is_active',
#             'company_name',
#             'industry',
#             'company_size'
#         ]
#         read_only_fields = fields



# UPDATE
class InspectorUpdateSerializer(serializers.ModelSerializer):
    # User fields
    email = serializers.EmailField(source='inspector.email')
    first_name = serializers.CharField(source='inspector.first_name')
    last_name = serializers.CharField(source='inspector.last_name')
    phone_number = serializers.CharField(source='inspector.phone_number', required=False, allow_null=True)
    profile_picture = serializers.ImageField(source='inspector.profile_picture', required=False, allow_null=True)
    bio = serializers.CharField(source='inspector.bio', required=False, allow_null=True)
    qualification = serializers.ChoiceField(
        source='inspector.qualification',
        choices=User.QUALIFICATION_CHOICES,
        required=False,
        allow_null=True
    )
    certifications = serializers.CharField(source='inspector.certifications', required=False, allow_null=True)

    # Inspector field
    years_of_experience = serializers.IntegerField()

    class Meta:
        model = Inspector
        fields = [
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'profile_picture',
            'bio',
            'qualification',
            'certifications',
            'years_of_experience'
        ]

    def validate_email(self, value):
        """
        Ensure email is unique except for current user
        """
        user = self.instance.inspector
        if User.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def update(self, instance, validated_data):
        # Extract user data
        inspector_data = {
            'years_of_experience': validated_data.pop('years_of_experience', None)
        }
        
        user_data = validated_data.pop('inspector', {})
        
        # Update User model
        user = instance.inspector
        for attr, value in user_data.items():
            if value is not None:  # Only update provided fields
                setattr(user, attr, value)
        user.save()

        # Update Inspector model
        for attr, value in inspector_data.items():
            if value is not None:
                setattr(instance, attr, value)
        instance.save()

        return instance

class AdminUpdateSerializer(serializers.ModelSerializer):
    # User fields
    email = serializers.EmailField(source='admin.email')
    first_name = serializers.CharField(source='admin.first_name')
    last_name = serializers.CharField(source='admin.last_name')
    phone_number = serializers.CharField(source='admin.phone_number', required=False, allow_null=True)
    profile_picture = serializers.ImageField(source='admin.profile_picture', required=False, allow_null=True)
    bio = serializers.CharField(source='admin.bio', required=False, allow_null=True)
    
    # Admin fields
    office_location = serializers.CharField()
    last_access = serializers.DateTimeField(required=False)

    class Meta:
        model = Admin
        fields = [
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'profile_picture',
            'bio',
            'office_location',
            'last_access'
        ]

    def validate_email(self, value):
        """
        Ensure email is unique except for current admin user
        """
        admin = self.instance
        if User.objects.filter(email=value).exclude(pk=admin.admin.pk).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def update(self, instance, validated_data):
        # Extract admin data
        admin_data = {
            'office_location': validated_data.pop('office_location', None),
            'last_access': validated_data.pop('last_access', None)
        }
        
        # Extract user data
        user_data = validated_data.pop('admin', {})
        
        # Update User model
        user = instance.admin
        for attr, value in user_data.items():
            if value is not None:  # Only update provided fields
                setattr(user, attr, value)
        user.save()

        # Update Admin model
        for attr, value in admin_data.items():
            if value is not None:
                setattr(instance, attr, value)
        instance.save()

        return instance


class WorkerUpdateSerializer(serializers.ModelSerializer):
    # User fields
    email = serializers.EmailField(source='worker.email')
    first_name = serializers.CharField(source='worker.first_name')
    last_name = serializers.CharField(source='worker.last_name')
    phone_number = serializers.CharField(source='worker.phone_number', required=False, allow_null=True)
    profile_picture = serializers.ImageField(source='worker.profile_picture', required=False, allow_null=True)
    bio = serializers.CharField(source='worker.bio', required=False, allow_null=True)
    qualification = serializers.ChoiceField(
        source='worker.qualification',
        choices=User.QUALIFICATION_CHOICES,
        required=False,
        allow_null=True
    )
    certifications = serializers.CharField(source='worker.certifications', required=False, allow_null=True)

    # Worker fields
    department = serializers.ChoiceField(choices=Worker.DEPARTMENT_CHOICES)
    shift_type = serializers.ChoiceField(choices=Worker.SHIFT_CHOICES)
    shift_time = serializers.TimeField(required=False, allow_null=True)
    next_shift_start = serializers.DateTimeField(required=False, allow_null=True)
    hire_date = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = Worker
        fields = [
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'profile_picture',
            'bio',
            'qualification',
            'certifications',
            'department',
            'shift_type',
            'shift_time',
            'next_shift_start',
            'hire_date'
        ]

    def validate_email(self, value):
        worker = self.instance
        if User.objects.filter(email=value).exclude(pk=worker.worker.pk).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def update(self, instance, validated_data):
        # Extract worker data
        worker_data = {
            'department': validated_data.pop('department'),
            'shift_type': validated_data.pop('shift_type'),
            'shift_time': validated_data.pop('shift_time', None),
            'next_shift_start': validated_data.pop('next_shift_start', None),
            'hire_date': validated_data.pop('hire_date', None)
        }
        
        # Extract user data
        user_data = validated_data.pop('worker', {})
        
        # Update User model
        user = instance.worker
        for attr, value in user_data.items():
            if value is not None:
                setattr(user, attr, value)
        user.save()

        # Update Worker model
        for attr, value in worker_data.items():
            if value is not None:
                setattr(instance, attr, value)
        instance.save()

        return instance

class ClientUpdateSerializer(serializers.ModelSerializer):
    # User fields
    email = serializers.EmailField(source='client.email')
    first_name = serializers.CharField(source='client.first_name')
    last_name = serializers.CharField(source='client.last_name')
    phone_number = serializers.CharField(source='client.phone_number', required=False, allow_null=True)
    profile_picture = serializers.ImageField(source='client.profile_picture', required=False, allow_null=True)
    bio = serializers.CharField(source='client.bio', required=False, allow_null=True)
    
    # Client fields
    company_name = serializers.CharField(required=False, allow_null=True)
    age = serializers.IntegerField(required=False, allow_null=True)
    class Meta:
        model = Client
        fields = [
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'profile_picture',
            'bio',
            'company_name',
            'age'
        ]

    def validate_email(self, value):
        """
        Ensure email is unique except for current client user
        """
        client = self.instance
        if User.objects.filter(email=value).exclude(pk=client.client.pk).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def update(self, instance, validated_data):
        # Extract client data
        client_data = {
            'company_name': validated_data.pop('company_name', None),
            'age': validated_data.pop('age', None)
        }
        
        # Extract user data
        user_data = validated_data.pop('client', {})
        
        # Update User model
        user = instance.client
        for attr, value in user_data.items():
            if value is not None:  # Only update provided fields
                setattr(user, attr, value)
        user.save()

        # Update Client model
        for attr, value in client_data.items():
            if value is not None:
                setattr(instance, attr, value)
        instance.save()

        return instance