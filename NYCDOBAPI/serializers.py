from rest_framework import serializers
from main.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util
from main.models import Price
from main.models import Profile
from main.models import Contact
from main.models import Complaints
from main.models import Voilation
from main.models import Property
import uuid


class UserRegistrationSerializer(serializers.ModelSerializer):
    # We are writing this becoz we need confirm password field in our Registratin Request
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'first_name', 'last_name', 'phone',
                  'company_name', 'address', 'city',  'state',  'zip',  'fax',  'cell', 'our_source']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # Validating Password and Confirm Password while Registration
    def validate(self, attrs):
        password = attrs.get('password')

        if not password:
            raise serializers.ValidationError("Password is necessary")
        return attrs

    def create(self, validate_data):
        user = User.objects.create_user(**validate_data)
        fname = user.first_name
        email = user.email
        auth_token = str(uuid.uuid4())
        profile_obj = Profile.objects.create(user=user, auth_token=auth_token)
        profile_obj.save()
        Util.send_mail_after_registration(
            email=email, auth_token=auth_token, fname=fname)

        return user


class ComplaintsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Complaints
        fields = '__all__'


class VoilationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Voilation
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'


class PropertyCreateSerializer(serializers.ModelSerializer):
    property_name = serializers.CharField(max_length=100)
    job_name = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)
    zip = serializers.CharField(max_length=100)
    borough = serializers.CharField(max_length=200)
    block = serializers.CharField(max_length=100)
    lott = serializers.CharField(max_length=100)
    street = serializers.CharField(max_length=100)
    house = serializers.CharField(max_length=100)
    bin_number = serializers.CharField(max_length=200)

    def create(self, validated_data):
        user = self.context.get('user')
        property_name = validated_data['property_name']
        job_name = validated_data['job_name']
        address = validated_data['address']
        state = validated_data['state']
        zip = validated_data['zip']
        borough = validated_data['borough']
        block = validated_data['block']
        lott = validated_data['lott']
        street = validated_data['street']
        house = validated_data['house']
        bin_number = validated_data['bin_number']

        # product = Product.objects.get(id=int(product_id))

        property = Property.objects.create(user=user,  property_name=property_name, job_name=job_name, address=address,
                                           state=state, zip=zip, borough=borough, block=block, lott=lott, street=street, house=house, bin_number=bin_number)

        return property

    class Meta:
        model = Property
        fields = [
            'property_name',
            'job_name',
            'address',
            'state',
            'zip',
            'borough',
            'block',
            'lott',
            'street',
            'house',
            'bin_number'


        ]


class ProfileForUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class UserDetailsSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name']


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    userdata = UserDetailsSerializers(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password',  'userdata']


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return attrs


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)
            link = 'http://localhost:8000/api/version-001/reset-password/'+uid+'/'+token
            print('Password Reset Link', link)
            # Send EMail
            body = 'Click Following Link to Reset Your Password '+link
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('You are not a Registered User')


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError(
                    "Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError(
                    'Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not Valid or Expired')


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['can_add', 'is_pro', 'pro_expiry_date']
