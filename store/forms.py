from django import forms
from django.forms import inlineformset_factory

from .models import Product, Category, Tag, Order, OrderPosition


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'})
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields['categories'].widget = forms.Select(
            choices=[(category.id, category.name) for category in Category.objects.all()])

        self.fields['tags'].widget = forms.CheckboxSelectMultiple(choices=[(tag.id, tag.name) for tag in Tag.objects.all()])


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'})
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'
        widgets = {
            'name':forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address', 'customer_phone', 'customer_name']
        widgets = {
            'delivery_address': forms.Textarea(attrs={'class': 'form-control'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class OrderPositionForm(forms.ModelForm):
    class Meta:
        model = OrderPosition
        fields = ['product', 'quantity', 'discount']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
        }


OrderPositionFormSet = inlineformset_factory(
    Order,
    OrderPosition,
    fields=['product', 'quantity', 'discount'],
    extra=1,
    can_delete=True)
