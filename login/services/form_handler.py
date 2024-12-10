from login.forms import RepositoryForm

class RepositoryFormHandler:
    def __init__(self, request):
        self.request = request
        self.form = RepositoryForm(request.POST)

    def is_valid(self):
        return self.form.is_valid()

    def get_repo_url(self):
        return self.form.cleaned_data['repo_url']
