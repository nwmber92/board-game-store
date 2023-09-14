from django import forms

ITEM_MAX_COUNT = [(i, str(i)) for i in range(1, 6)]


class CartAddItemForm(forms.Form):
    count_item = forms.TypedChoiceField(choices=ITEM_MAX_COUNT, coerce=int, label='шт.')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    def __init__(self, cart_item_count=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['count_item'].initial = cart_item_count
        self.fields['count_item'].widget.attrs.update({'class': 'form-select d-inline'})
