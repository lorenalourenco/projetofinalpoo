from django import forms

class RepositoryForm(forms.Form):
    repo_url = forms.URLField(label="URL do Repositório", widget=forms.URLInput(attrs={'placeholder': 'Digite a URL do repositório'}))
