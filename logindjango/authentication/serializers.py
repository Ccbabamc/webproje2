from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

class TCAuthTokenSerializer(serializers.Serializer):
    tc_kimlik_no = serializers.CharField(
        label=_("TC Kimlik No"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        tc_kimlik_no = attrs.get('tc_kimlik_no')
        password = attrs.get('password')

        if tc_kimlik_no and password:
            user = authenticate(request=self.context.get('request'),
                              username=tc_kimlik_no,
                              password=password)

            if not user:
                msg = _('Giriş bilgileri hatalı.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('TC Kimlik No ve şifre gereklidir.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs 