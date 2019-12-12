from django import forms

class ContactForm(forms.Form):
    usuario = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder':'Escribe tu nombre'}))
    mensaje = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={'rows': 2, 'cols': 35, 'placeholder':'Escribe aqui'})
        #widget=forms.TextInput(attrs={'size': 20})#,
        #help_text='Escribe aqui'
    )

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        usuario = cleaned_data.get('usuario')
        mensaje = cleaned_data.get('mensaje')
        if not usuario or not mensaje:
            raise forms.ValidationError('Los campos usuario y/o mensaje no pueden estar vacios')