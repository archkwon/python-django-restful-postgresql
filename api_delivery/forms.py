from django import forms
from api_delivery.models import DeliveryFileModel

class DeliveryFileForm(forms.ModelForm):
    file_seq = forms.CharField(required=False)
    master_seq = forms.CharField(required=True)
    image_file = forms.FileField(required=False)
    image_file_url = forms.CharField(required=False)

    class Meta:
        model = DeliveryFileModel
        fields = ('file_seq','master_seq','image_file','image_file_url',)
