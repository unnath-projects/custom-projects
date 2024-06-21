from django import forms


class TextInputForm(forms.Form):
    user_text = forms.CharField(
        label='Enter SIG',
        max_length=300,
        widget=forms.Textarea(attrs={'placeholder': 'Type your text here...'})
    )




