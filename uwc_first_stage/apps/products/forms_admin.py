from django import forms
from django.utils.translation import ugettext_lazy as _
from products.models import ProductParameter, Parameter, ParameterValue
from ajax_select import make_ajax_field

class ProductParameterForm(forms.ModelForm):

    parameter = make_ajax_field(Parameter,'name','parameters',help_text=None)
    value = forms.ModelChoiceField(label=_('Value'), queryset=ParameterValue.objects.all(), cache_choices=True)

    class Meta:
        model = ProductParameter

    def __init__(self, *args, **kwargs):
        super(ProductParameterForm, self).__init__(*args, **kwargs)