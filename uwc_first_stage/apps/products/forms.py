from django import forms
from django.utils.translation import ugettext_lazy as _


class ProductImageInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        """Only one main image is possible."""
        count = [item.get('is_main_image', False) for item in self.cleaned_data].count(True)
        if count > 1:
            raise forms.ValidationError(_("Only one main image!"))
