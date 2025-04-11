from datetime import datetime

from .models import Recipient, Message, Sending

from django import forms


class RecipientForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    name = forms.CharField(
        label="ФИО", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    comment = forms.CharField(
        label="Комментарий", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Recipient
        fields = ("email", "name", "comment")


class MessageForm(forms.ModelForm):
    subject = forms.CharField(
        label="Тема письма", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    content = forms.CharField(
        label="Тело письма", widget=forms.Textarea(attrs={"class": "form-control"})
    )

    class Meta:
        model = Message
        fields = ("subject", "content")


class SendingForm(forms.ModelForm):
    first_sending = forms.DateTimeField(
        label="Дата первой рассылки",
        input_formats={"%H:%M %d-%m-%Y"},
        widget=forms.DateTimeInput(
            format="%H:%M %d-%m-%Y",
            attrs={"class": "form-control", "type": "datetime-local"},
        ),
    )
    stop_sending = forms.DateTimeField(
        label="Дата остановки рассылки",
        input_formats={"%H:%M %d-%m-%Y"},
        widget=forms.DateTimeInput(
            format="%H:%M %d-%m-%Y",
            attrs={"class": "form-control", "type": "datetime-local"},
        ),
    )

    message = forms.ModelChoiceField(
        label="Письмо",
        queryset=Message.objects.all(),
        # widget=forms.Select(attrs={'class': "form-select"}),
        widget=forms.Select(attrs={"class": "form-select", "style": "width: 200px"}),
    )

    recipients = forms.ModelMultipleChoiceField(
        label="Получатели рассылки",
        queryset=Recipient.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Sending
        fields = ("first_sending", "stop_sending", "recipients", "message")

    def clean_status(self):
        status = self.cleaned_data["status"]
        end_mailing = self.cleaned_data.get("end_mailing")
        if end_mailing and end_mailing < datetime.now():
            status = "Остановлена"
        return status
