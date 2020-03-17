from rest_framework import serializers
from .models import User

class MailChimpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email_id',)