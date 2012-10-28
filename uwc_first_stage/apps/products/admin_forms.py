from django import forms
from django.forms import TypedChoiceField
from django.forms.models import BaseInlineFormSet
from django.utils.translation import ugettext_lazy as _
from products.models import Category, CategoryParameter, Parameter


class CategoryParameterFormset(BaseInlineFormSet):
    def get_queryset(self):
        q = super(CategoryParameterFormset, self).get_queryset()

        return q.select_related('parameter', 'category', 'category__parent')

class ProductParameterForm(forms.ModelForm):
    """
        Form for CategoryParameterInline admin inline
    """
    TypedChoiceField
    parameter = forms.ModelChoiceField(
        queryset=Parameter.objects.all(),
        label=_('parameter')
    )

    class Meta:
        model = CategoryParameter

    def __init__(self, *args, **kwargs):
        super(CategoryParameterForm, self).__init__(*args, **kwargs)
        ids = []

        if self.instance.category and self.instance.category.id:
            ids.append(self.instance.id)
            if self.instance.category.parent:
                ids.append(self.instance.category.parent.id)

        # Override queryset of parameters. Shows only instance and parent parameters
        if ids:
            self.fields['parameter'].queryset = Parameter.objects.filter(related_categories__category__in=ids)

