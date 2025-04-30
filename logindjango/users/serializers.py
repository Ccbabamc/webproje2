from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Aday, Admin, Yonetici, JuriUyesi

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'tc_kimlik_no', 'username', 'email', 'first_name', 'last_name', 
                  'role', 'faculty', 'department', 'phone', 'is_active', 'is_staff', 
                  'date_joined', 'last_login', 'profile_image']
        # Make is_staff readable but not directly writable through this serializer
        read_only_fields = ['id', 'date_joined', 'last_login', 'is_active'] 
        extra_kwargs = {
            'password': {'write_only': True},
            'is_staff': {'read_only': True} # Explicitly mark as read-only here
        }
    
    def get_profile_image(self, obj):
        # Kullanıcının Aday profili varsa, profil fotoğrafını döndür
        if hasattr(obj, 'aday_profile') and obj.aday_profile.profile_image:
            # Ensure context and request exist
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.aday_profile.profile_image.url)
        return None

class UserUpdateSerializer(serializers.ModelSerializer):
    # Allow role to be updated
    role = serializers.ChoiceField(choices=User.Role.choices, required=False) 

    class Meta:
        model = User
        # is_staff is handled by the model's save method based on role
        fields = ['id', 'tc_kimlik_no', 'username', 'email', 'first_name', 'last_name', 
                  'role', 'faculty', 'department', 'phone', 'password'] 
        read_only_fields = ['id', 'tc_kimlik_no', 'username']  # These cannot be updated
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }
    
    def validate(self, data):
        # TC Kimlik No ve kullanıcı adının değiştirilmediğinden emin oluyoruz
        if 'tc_kimlik_no' in data:
            data.pop('tc_kimlik_no')
        if 'username' in data:
            data.pop('username')
        return data
    
    def update(self, instance, validated_data):
        # Eğer şifre varsa, şifreyi güncelle
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
            
        # Diğer alanları güncelle (role dahil)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Model's save method will handle is_staff based on the new role
        instance.save() 
        return instance

# Rewriting the entire class to ensure clean formatting
class UserCreateSerializer(serializers.ModelSerializer):
    # Allow role selection during creation
    role = serializers.ChoiceField(choices=User.Role.choices, required=True) 

    class Meta:
        model = User
        fields = [
            'id', 'tc_kimlik_no', 'username', 'email', 'password', 'first_name', 
            'last_name', 'role', 'faculty', 'department', 'phone'
            # is_staff is not included here, will be set by model's save() based on role
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': False, 'allow_blank': True} # Allow blank username input
        }

    def validate(self, data):
        # No need for explicit sync logic here anymore, model handles it.
        # Add validation for required fields if necessary (though handled by DRF)
        if not data.get('tc_kimlik_no'):
             raise serializers.ValidationError({"tc_kimlik_no": "TC Kimlik No zorunludur."})
        # Add other validations as needed
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        # Ensure username is not in the data passed to User constructor
        # Let the model's save() method handle setting it from tc_kimlik_no
        validated_data.pop('username', None) 
        
        user = User(**validated_data)
        user.set_password(password)
        
        # Model's save() method will handle setting is_staff based on role
        user.save() 
        return user

# --- Role Specific Serializers ---
# These might need review if they create User instances directly

class AdaySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) # Make user read-only if managed separately

    class Meta:
        model = Aday
        fields = ('id', 'user', 'cv', 'diploma', 'profile_image', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at', 'user') # User should be linked, not created here

class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Admin
        fields = ('id', 'user', 'department', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at', 'user')

class YoneticiSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Yonetici
        fields = ('id', 'user', 'faculty', 'department', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at', 'user')

class JuriUyesiSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = JuriUyesi
        fields = ('id', 'user', 'faculty', 'department', 'expertise', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at', 'user')
