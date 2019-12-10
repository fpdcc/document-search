from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView


class BaseUrlMixin:
    def get_url(self, attr, obj=None):
        if not hasattr(self, attr):
            raise AttributeError(
                f'{attr} is required on this class'
            )
        name = getattr(self, attr)
        if obj is not None:
            args = (obj.pk,)
        else:
            args = ()
        return reverse(name, args=args)


class CancelUrlMixin(BaseUrlMixin):
    def get_cancel_url(self, obj=None):
        return self.get_url('cancel_url', obj)


class DeleteUrlMixin(BaseUrlMixin):
    def get_delete_url(self, obj=None):
        return self.get_url('delete_url', obj)


class UpdateUrlMixin(BaseUrlMixin):
    def get_update_url(self, obj=None):
        return self.get_url('update_url', obj)


class BaseCreateView(LoginRequiredMixin, CancelUrlMixin, CreateView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['cancel_url'] = self.get_cancel_url()
        return context


class BaseUpdateView(LoginRequiredMixin, CancelUrlMixin, DeleteUrlMixin, UpdateView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['cancel_url'] = self.get_cancel_url(obj=context['object'])
        context['delete_url'] = self.get_delete_url(obj=context['object'])
        return context


class BaseDetailView(LoginRequiredMixin, UpdateUrlMixin, DetailView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['update_url'] = self.get_update_url(obj=context['object'])
        return context


class BaseDeleteView(LoginRequiredMixin, CancelUrlMixin, DeleteView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['cancel_url'] = self.get_cancel_url(obj=context['object'])
        return context
