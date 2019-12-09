from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from docsearch import models, base_views


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'docsearch/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['doctypes'] = models.get_searchable_models()
        return context


class Search(LoginRequiredMixin, TemplateView):
    template_name = 'docsearch/search.html'


class BookDetail(base_views.BaseDetailView):
    model = models.Book
    update_url = 'book-update'


class BookCreate(base_views.BaseCreateView):
    model = models.Book
    fields = '__all__'
    cancel_url = 'home'  # TODO: Change this to Search


class BookUpdate(base_views.BaseUpdateView):
    model = models.Book
    fields = '__all__'
    cancel_url = 'book'
    delete_url = 'book-delete'


class BookDelete(base_views.BaseDeleteView):
    model = models.Book
    cancel_url = 'book'
    success_url = reverse_lazy('book-create')  # TODO: Change to search
