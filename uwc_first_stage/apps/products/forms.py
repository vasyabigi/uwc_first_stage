from django import forms
from django.utils.translation import ugettext_lazy as _
from products.models import Parameter, Product


class ProductImageInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        """Only one main image is possible."""
        count = [item.get('is_main_image', False) for item in self.cleaned_data].count(True)
        if count > 1:
            raise forms.ValidationError(_("Only one main image!"))


class ParameterFilteringForm(forms.Form):
    parameters = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxInput(),
        queryset=Parameter.objects.none()
    )

    def __init__(self, category, *args, **kwargs):
        super(ParameterFilteringForm, self).__init__(*args, **kwargs)
        self.fields['parameters'].queryset = Parameter.objects.filter_by_category(category)

    def get_products(self):
        return Product.objects.filter_by_parameters(self.cleaned_data['parameters'])
