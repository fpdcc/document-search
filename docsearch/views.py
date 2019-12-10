from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from docsearch import models, base_views


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'docsearch/index.html'


class Search(LoginRequiredMixin, TemplateView):
    template_name = 'docsearch/search.html'


class BookDetail(base_views.BaseDetailView):
    model = models.Book
    template_name = 'docsearch/book/detail.html'
    update_url = 'book-update'


class BookCreate(base_views.BaseCreateView):
    model = models.Book
    template_name = 'docsearch/book/form.html'
    fields = '__all__'
    cancel_url = 'home'  # TODO: Change this to Search


class BookUpdate(base_views.BaseUpdateView):
    model = models.Book
    template_name = 'docsearch/book/form.html'
    fields = '__all__'
    cancel_url = 'book'
    delete_url = 'book-delete'


class BookDelete(base_views.BaseDeleteView):
    model = models.Book
    template_name = 'docsearch/book/confirm_delete.html'
    cancel_url = 'book'
    success_url = reverse_lazy('book-create')  # TODO: Change to search
