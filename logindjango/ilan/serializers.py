from rest_framework import serializers
from .models import Fakulte, Bolum, Kriter, Ilan
from datetime import datetime
import logging

class FakulteSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='ad')
    
    class Meta:
        model = Fakulte
        fields = ['id', 'name']

class BolumSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='ad')
    faculty = serializers.PrimaryKeyRelatedField(source='fakulte', queryset=Fakulte.objects.all())

    class Meta:
        model = Bolum
        fields = ['id', 'name', 'faculty']

class KriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kriter
        fields = '__all__'

class IlanSerializer(serializers.ModelSerializer):
    bolum = BolumSerializer(read_only=True)
    kriterler = KriterSerializer(many=True, read_only=True)

    class Meta:
        model = Ilan
        fields = '__all__'

class IlanListSerializer(serializers.ModelSerializer):
    bolum_adi = serializers.CharField(source='bolum.ad', read_only=True)
    # fakulte_adi artık null olabilir, bu yüzden allow_null=True ekliyoruz.
    fakulte_adi = serializers.CharField(source='bolum.fakulte.ad', read_only=True, allow_null=True)
    kriterler_count = serializers.IntegerField(source='kriterler.count', read_only=True)

    class Meta:
        model = Ilan
        fields = [
            'id', 'bolum', 'bolum_adi', 'fakulte_adi', 'baslik',
            'son_basvuru_tarihi', 'status', 'kriterler_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
        
    def to_representation(self, instance):
        """
        Özel alan dönüşümü için, frontend-backend uyumluluğu
        """
        ret = super().to_representation(instance)
        # Frontend uyumluluğu için ek alanlar
        ret['title'] = ret['baslik']
        ret['department'] = ret['bolum_adi']
        ret['faculty'] = ret['fakulte_adi']
        ret['deadline'] = ret['son_basvuru_tarihi']
        
        # Status değerini frontend formatına dönüştür
        status_map = {
            'AKTIF': 'active',
            'KAPALI': 'closed',
            'TASLAK': 'draft'
        }
        # Eğer frontend değeri isteniyorsa ekle
        if ret['status'] in status_map:
            ret['status_frontend'] = status_map[ret['status']]
        
        return ret

class IlanDetailSerializer(serializers.ModelSerializer):
    bolum = BolumSerializer(read_only=True)
    kriterler = KriterSerializer(many=True, read_only=True)

    class Meta:
        model = Ilan
        fields = [
            'id', 'bolum', 'baslik', 'aciklama', 'son_basvuru_tarihi',
            'status', 'kriterler', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class IlanCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ilan
        fields = [
            'id', 'bolum', 'baslik', 'aciklama', 'son_basvuru_tarihi',
            'status', 'kriterler' # Note: kriterler might need separate handling for create/update
        ]

logger = logging.getLogger(__name__)

class FrontendIlanCreateSerializer(serializers.Serializer):
    # Frontend'den gelen veriler için alanlar
    title = serializers.CharField(required=True)
    bolum = serializers.PrimaryKeyRelatedField(queryset=Bolum.objects.all(), required=True) # Frontend sends 'department' ID, maps to this 'bolum' field
    description = serializers.CharField(required=True)
    # requirements field removed as it's unused and frontend sends required_documents separately
    # Frontend sends 'end_date', maps to this 'deadline' field
    deadline = serializers.DateField(required=True)
    # Frontend sends 'status' ('active'/'inactive'), maps to this field after validation
    status = serializers.CharField(required=False, default='TASLAK')

    # Kriterler ve Gerekli Belgeler frontend'den gelebilir ancak bu serializer'da doğrudan işlenmiyor.
    # Bunları write_only=True olarak işaretleyip create/update içinde özel işlem yapabiliriz
    # veya şimdilik create/update içinde yok sayabiliriz.
    # required_documents = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)
    # criteria = serializers.ListField(child=serializers.DictField(), required=False, write_only=True)

    def validate_status(self, value):
        """Frontend'den gelen status değerini ('active', 'inactive') backend formatına ('AKTIF', 'TASLAK', 'KAPALI') çevirir."""
        status_map = {
            'active': 'AKTIF',
            'inactive': 'TASLAK', # Frontend 'inactive' genellikle 'Taslak' anlamına gelir
            'draft': 'TASLAK',    # Explicit draft status
            'closed': 'KAPALI'    # Explicit closed status
        }
        normalized_value = str(value).lower() # Gelen değeri string'e çevirip küçük harf yap
        backend_status = status_map.get(normalized_value)
        if backend_status:
            return backend_status
        # Eğer bilinen bir değer değilse veya boşsa, varsayılan olarak TASLAK döndür veya hata fırlat
        logger.warning(f"Geçersiz status değeri alındı: '{value}'. 'TASLAK' olarak ayarlanıyor.")
        return 'TASLAK' # Veya raise serializers.ValidationError("Geçersiz durum değeri.")

    def validate_deadline(self, value):
        """Tarihin geçmiş bir tarih olmadığından emin ol."""
        # Not: Bu validasyon frontend tarafında da yapılabilir.
        # if value < datetime.now().date():
        #     raise serializers.ValidationError("Son başvuru tarihi geçmiş bir tarih olamaz.")
        return value

    def create(self, validated_data):
        """Frontend'den gelen verilerle yeni Ilan oluşturur."""
        logger.info(f"İlan oluşturma isteği alındı. Doğrulanmış veriler: {validated_data}")

        # Frontend'den gelebilecek ancak bu serializer'da doğrudan işlenmeyen alanları ayıkla
        criteria_data = validated_data.pop('criteria', None)
        required_documents_data = validated_data.pop('required_documents', None)
        if criteria_data:
            logger.warning("Gelen 'criteria' verisi bu endpoint tarafından işlenmiyor.")
        if required_documents_data:
            logger.warning("Gelen 'required_documents' verisi bu endpoint tarafından işlenmiyor.")

        # Frontend alan adlarını model alan adlarına eşle
        ilan_data = {
            'baslik': validated_data.get('title'),
            'bolum': validated_data.get('bolum'),
            'aciklama': validated_data.get('description'),
            'son_basvuru_tarihi': validated_data.get('deadline'),
            'status': validated_data.get('status', 'TASLAK') # status validate edildi
        }
        # None değerleri kaldır (opsiyonel alanlar için)
        ilan_data = {k: v for k, v in ilan_data.items() if v is not None}

        try:
            ilan = Ilan.objects.create(**ilan_data)
            logger.info(f"İlan başarıyla oluşturuldu: ID={ilan.id}, Başlık={ilan.baslik}")

            # TODO: Kriterler ve Gerekli Belgeler için ayrı işlem gerekebilir.
            # Örneğin, bu verilerle Kriter nesneleri oluşturup ilana bağlamak.

            return ilan
        except Exception as e:
            logger.error(f"İlan oluşturma sırasında veritabanı hatası: {str(e)}", exc_info=True)
            raise serializers.ValidationError(f"İlan oluşturulurken bir sunucu hatası oluştu: {e}")

    def update(self, instance, validated_data):
        """Mevcut Ilan'ı frontend'den gelen verilerle günceller."""
        logger.info(f"İlan güncelleme isteği alındı. ID: {instance.id}, Doğrulanmış veriler: {validated_data}")

        # Frontend'den gelebilecek ancak bu serializer'da doğrudan işlenmeyen alanları ayıkla
        criteria_data = validated_data.pop('criteria', None)
        required_documents_data = validated_data.pop('required_documents', None)
        if criteria_data:
            logger.warning("Gelen 'criteria' verisi bu endpoint tarafından işlenmiyor.")
        if required_documents_data:
            logger.warning("Gelen 'required_documents' verisi bu endpoint tarafından işlenmiyor.")

        # Alanları güncelle (frontend adlarından model adlarına eşleyerek)
        instance.baslik = validated_data.get('title', instance.baslik)
        instance.bolum = validated_data.get('bolum', instance.bolum)
        instance.aciklama = validated_data.get('description', instance.aciklama)
        instance.son_basvuru_tarihi = validated_data.get('deadline', instance.son_basvuru_tarihi)
        instance.status = validated_data.get('status', instance.status) # status validate edildi

        # TODO: Kriterler ve Gerekli Belgeler için ayrı güncelleme/ilişkilendirme mantığı gerekebilir.

        try:
            instance.save()
            logger.info(f"İlan başarıyla güncellendi: ID={instance.id}")
            return instance
        except Exception as e:
            logger.error(f"İlan güncelleme sırasında veritabanı hatası: {str(e)}", exc_info=True)
            raise serializers.ValidationError(f"İlan güncellenirken bir sunucu hatası oluştu: {e}")
