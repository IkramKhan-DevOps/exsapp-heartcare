import os

from rest_framework import generics, viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.accounts.models import User
from src.api.models import Predication
from . import ai_utils
from .serializers import (
    UserPasswordChangeSerializer, UserSerializer,
    PredicationSerializer
)
from core import settings

""" AUTH USER API' S """


class UserPublicDetailedView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileDetailedView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserPasswordChangeView(generics.UpdateAPIView):
    model = User
    serializer_class = UserPasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


""" PUBLIC API'S """


class PredicationViewSet(APIView):
    queryset = Predication.objects.all()
    serializer_class = PredicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        predication = Predication(user=self.request.user,
                                  age=self.request.data['age'],
                                  gender=self.request.data['gender'],
                                  resting_bp_s=self.request.data['resting_bp_s'],
                                  cholestrol=self.request.data['cholestrol'],
                                  fasting_blood_sugar=self.request.data['fasting_blood_sugar'],
                                  old_peak=self.request.data['old_peak'],
                                  chest_pain_type=self.request.data['chest_pain_type'],
                                  st_slope=self.request.data['st_slope'],
                                  target=0,
                                  exercise_angina=self.request.data['exercise_angina'],
                                  resting_ecg=self.request.data['resting_ecg'],
                                  max_heart_rate=self.request.data['max_heart_rate'])
        inp = (int(predication.age),
               int(predication.resting_bp_s),
               int(predication.cholestrol),
               int(predication.fasting_blood_sugar),
               int(predication.max_heart_rate),
               int(predication.exercise_angina),
               float(predication.old_peak),
               int(predication.gender),
               1 if int(predication.chest_pain_type) == 1 else 0,
               1 if int(predication.chest_pain_type) == 3 else 0,
               1 if int(predication.chest_pain_type) == 2 else 0,
               1 if int(predication.resting_ecg) == 2 else 0,
               1 if int(predication.resting_ecg) == 0 else 0,
               1 if int(predication.st_slope) == 2 else 0,
               1 if int(predication.st_slope) == 3 else 0)
        target = ai_utils.run(inp)
        print('--------------------TARGET------------------------------------')
        print(int(target[0][0]))
        predication.target = int(target[0][0])
        predication.save()
        return Response(data={'Target': predication.target}, status=status.HTTP_201_CREATED)

    def get(self, request, format=None):
        predications = Predication.objects.filter(user=self.request.user)
        data = PredicationSerializer(predications, many=True).data
        return Response(data=data, status=status.HTTP_202_ACCEPTED)
