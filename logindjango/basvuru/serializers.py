from rest_framework import serializers
from .models import Basvuru, Belge, Tablo5, Puan
from users.serializers import UserSerializer
from ilan.serializers import IlanSerializer, KriterSerializer

class BelgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Belge
        fields = '__all__'
        read_only_fields = ['id', 'upload_date']

class PuanSerializer(serializers.ModelSerializer):
    kriter = KriterSerializer(read_only=True)
    supporting_documents = BelgeSerializer(many=True, read_only=True)

    class Meta:
        model = Puan
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class Tablo5Serializer(serializers.ModelSerializer):
    puanlar = PuanSerializer(many=True, read_only=True)

    class Meta:
        model = Tablo5
        fields = '__all__'
        read_only_fields = ['id', 'creation_date', 'created_at', 'updated_at']

class BasvuruListSerializer(serializers.ModelSerializer):
    aday = UserSerializer(read_only=True)
    ilan = IlanSerializer(read_only=True)

    class Meta:
        model = Basvuru
        fields = [
            'id', 'ilan', 'aday', 'submission_date', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'submission_date', 'created_at', 'updated_at']

class BasvuruDetailSerializer(serializers.ModelSerializer):
    aday = UserSerializer(read_only=True)
    ilan = IlanSerializer(read_only=True)
    belgeler = BelgeSerializer(many=True, read_only=True)
    tablo5 = Tablo5Serializer(read_only=True)

    class Meta:
        model = Basvuru
        fields = [
            'id', 'ilan', 'aday', 'submission_date', 'status',
            'tablo5_file', 'belgeler', 'tablo5', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'submission_date', 'created_at', 'updated_at']

class BasvuruCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basvuru
        fields = ['id', 'ilan', 'status', 'tablo5_file']
        read_only_fields = ['id'] 