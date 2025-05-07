from django import forms
from django.core.exceptions import ValidationError

from shop.models import Order


class SearchForm(forms.Form):
    q = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Поиск"}
        )
    )


class OrderModelForm(forms.ModelForm):
    """Выпадающий список"""
    DELIVERY_CHOISES = (
        (0, "Выберите пожалуйста"),
        (1, "Доставка"),
        (2, "Самовывоз"),
    )
    delivery = forms.TypedChoiceField(label="Доставка", choices=DELIVERY_CHOISES, coerce=int)

    class Meta:
        model = Order
        """Исключаем ненужные поля"""
        exclude = ["discount", "status", "need_delivery"]
        """Меняем placeholder для поля в соответствии с вёрсткой"""
        labels = {"addres": "Полный адрес (Страна, город, улица, дом, квартира)"}
        widgets = {
            "addres": forms.Textarea(
                attrs={"rows": 6, "cols": 80, "placeholder": "При самовывозе можно оставить это поле пустым"}
            ),
            "notice": forms.Textarea(
                attrs={"rows": 6, "cols": 80}
            ),
        }

    def clean_delivery(self):
        """Валидация поля доставка"""
        # data = self.cleaned_data['delivery']
        cleaned_data = super().clean()
        data = cleaned_data.get('delivery')
        print(f"data = {data}")
        if data == 0:
            raise ValidationError("Необходимо выбрать способ доставки")
        # elif data == 1 or data == 2:
        #     return data
        # raise ValidationError("Неизвестная ошибка")
        return data

    def clean(self):
        """Валидация формы"""
        # print(self.delivery)
        cleaned_data = super().clean()
        delivery = cleaned_data.get('delivery')
        # delivery = self.cleaned_data['delivery']
        address = cleaned_data.get('address')
        # address = self.cleaned_data['address']
        if delivery == 1 and address == "":
            raise ValidationError("Необходимо выбрать адрес доставки")
        return self.cleaned_data

