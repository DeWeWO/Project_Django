from django import forms
from .models import Product
from django.forms import ClearableFileInput, FileField
from django.core.validators import validate_image_file_extension
from ckeditor.widgets import CKEditorWidget
from ckeditor.fields import RichTextFormField

class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(FileField):
    default_validators = [validate_image_file_extension]
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)
        
    def clean(self, data, initial = None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ProductForm(forms.ModelForm):
    images = MultipleFileField()
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'ckeditor form-control'}))
    
    class Meta:
        model = Product
        fields = ["title", "description", "price", "stock_status", "quantity", "category", "discount"]