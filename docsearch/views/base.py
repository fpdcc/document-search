from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from docsearch import models


class BaseUrlMixin:
    def get_url(self, attr, obj=None):
        if hasattr(self, attr):
            # If the base attr is set, that means the user has set a simple
            # URL string, so default to that string
            return getattr(self, attr)
        elif hasattr(self, f'{attr}_from_obj'):
            if obj is None:
                raise ValueError(
                    f'Expected an obj kwarg for {attr}_from_obj, got None'
                )
            name = getattr(self, f'{attr}_from_obj')
            return reverse(name, args=(obj.pk,))
        else:
            raise AttributeError(
                f'One of {attr} or {attr}_from_obj must be set on this class'
            )


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

    def form_valid(self, form):
        models.ActionLog.objects.create(
            user=self.request.user,
            content_object=form.instance,
            action=models.ActionLog.Action.CREATE
        )
        return super().form_valid(form)


class BaseUpdateView(LoginRequiredMixin, CancelUrlMixin, DeleteUrlMixin, UpdateView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['cancel_url'] = self.get_cancel_url(obj=context['object'])
        context['delete_url'] = self.get_delete_url(obj=context['object'])
        return context

    def form_valid(self, form):
        models.ActionLog.objects.create(
            user=self.request.user,
            content_object=form.instance,
            action=models.ActionLog.Action.UPDATE
        )
        return super().form_valid(form)


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
