from django import forms

# from pagedown.widgets import PagedownWidget

from core.models import Item, ImageUploads


class ItemForm(forms.ModelForm):
    #     content = forms.CharField(widget=PagedownWidget(show_preview=False))
    #     publish = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Item
        fields = [
            "title",
            "sku",
            "upc",
            "price",
            "discount_price",
            "category",
            "label",
            "slug",
            "description",
            "image",
            "stock_quantity",
        ]


class ImageUploads(forms.ModelForm):
    #     content = forms.CharField(widget=PagedownWidget(show_preview=False))
    #     publish = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = ImageUploads
        fields = [
            "image",
        ]
