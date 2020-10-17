from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView


class BaseAPIView(LoginRequiredMixin, APIView):
    pass
