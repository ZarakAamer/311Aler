from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer
from .serializers import PropertySerializer, PropertyCreateSerializer
from .serializers import ContactSerializer, PriceSerializer, UserDetailsSerializers, ProfileForUserDataSerializer, ComplaintsSerializers, VoilationsSerializer
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from main.models import Profile
from rest_framework.decorators import api_view
from django.shortcuts import render, get_object_or_404
from main.models import User, Property, Price, Complaints, Voilation

# Generate Token Manually


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = get_tokens_for_user(user)
        return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)


# class UserLoginView(APIView):
#     renderer_classes = [UserRenderer]

#     def post(self, request, format=None):
#         serializer = UserLoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         email = serializer.validated_data.get('email')
#         password = serializer.validated_data.get('password')
#         user = authenticate(email=email, password=password)
#         if user is not None:
#             if Profile.objects.filter(user=user).first().is_verified:
#                 token = get_tokens_for_user(user)
#                 user_id = user.id
#                 user_for_data = User.objects.get(id=user_id)
#                 user_data = UserDetailsSerializers(user_for_data, many=False)

#                 return Response({'msg': 'Login Success', 'data': user_data.data, 'token': token}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'msg': 'Account is not verified'}, status=status.HTTP_404_NOT_FOUND)
#         else:
#             return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        user = authenticate(request, **request.data)
        if user is None:
            return Response({'error': 'Invalid login credentials'}, status=400)
        # Create access and refresh tokens for the user
        if Profile.objects.filter(user=user).first().is_verified:
            token = get_tokens_for_user(user)
            # Get the user's orders
            user_id = user.id
            user_for_data = User.objects.get(id=user_id)
            user_profile = Profile.objects.filter(user=user_for_data).first()
            user_property = Property.objects.filter(
                user=user_for_data)

            user_data = UserDetailsSerializers(user_for_data, many=False)
            user_properties = PropertySerializer(user_property, many=True)

            user_profile = ProfileForUserDataSerializer(
                user_profile, many=False)
            return Response({'msg': 'Login Success', 'user': user_data.data, 'user_profile': user_profile.data, 'Properties': user_properties.data,  'token': token}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Email is not verified'}, status=400)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_200_OK)


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(
            data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_200_OK)


class VerifyRegisteration(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, auth_token):

        try:

            profile_obj = Profile.objects.get(auth_token=auth_token)

            if profile_obj:
                if profile_obj.is_verified:
                    return Response({'msg': 'Account is already verified'}, status=status.HTTP_200_OK)

                profile_obj.is_verified = True
                profile_obj.save()
                return Response({'msg': 'Account verified successfully'}, status=status.HTTP_200_OK)

            else:
                return Response({'msg': 'Invalid Url !!!'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({'msg': 'Varification fialed or already varified !!!'}, status=status.HTTP_400_BAD_REQUEST)


class ComplaintsView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        complaints = Complaints.objects.filter(user=user)
        serializer = ComplaintsSerializers(
            complaints, many=True)
        return Response({'msg': serializer.data}, status=status.HTTP_200_OK)


class VoilationsView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        voilations = Voilation.objects.filter(user=user)
        serializer = VoilationsSerializer(voilations, many=True)
        return Response({'msg': serializer.data}, status=status.HTTP_200_OK)


class PropertyListView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        properties = Property.objects.filter(user=user)
        serializer = PropertySerializer(properties, many=True)
        return Response({'msg': serializer.data}, status=status.HTTP_200_OK)


class PropertyView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PropertyCreateSerializer(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'msg': 'Property added  Successful'}, status=status.HTTP_201_CREATED)


class PropertyDeleteView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def delete(self, request, property_id):
        serializer = PropertySerializer()
        try:
            Property.objects.get(id=property_id).delete()
            return Response({'msg': 'Property Deleted'}, status=status.HTTP_404_NOT_FOUND)

        except:
            return Response({'msg': 'unexpected Error Occured'}, status=status.HTTP_201_CREATED)


class PriceView(APIView):
    renderer_classes = [UserRenderer]

    def get(self, request, format=None):
        prices = Price.objects.all()
        serializer = PriceSerializer(prices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContactView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Message Sent Successful'}, status=status.HTTP_201_CREATED)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def putsss(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # user = get_object_or_404(User, user=request.user)
        # print(user)
        profile = Profile.objects.filter(user=self.request.user).first()
        print(self.request.user)
        profile.can_add = serializer.data['can_add']
        profile.is_pro = serializer.data['is_pro']
        profile. pro_expiry_date = serializer.data['pro_expiry_date']
        profile.save()

        return Response({'msg': 'profile Updated Successful'}, status=status.HTTP_201_CREATED)
