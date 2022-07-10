from typing import Any, Dict, List
from django.views.generic import ListView, FormView, View
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _


class BaseContextMixin:
    def get_context_data(self, **kwargs):
        if hasattr(super(), 'get_context_data'):
            context = super().get_context_data(**kwargs)
        else:
            context = {}
        context['user'] = self.request.user
        return context


class BaseView(View):
    page_title = None
    page_subtitle = None
    page_subtitle_field = None
    page_subtitle_prefix = '#'
    go_back_button = True

    def get_page_title(self):
        if self.page_title:
            return self.page_title
        if self.model:
            return self.model._meta.verbose_name_plural
        queryset = self.get_queryset()
        if queryset:
            return queryset.model._meta.verbose_name_plural
    
    def get_page_subtitle(self):
        return self.page_subtitle or ''

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.get_page_title()
        context['page_subtitle'] = self.get_page_subtitle()
        context['go_back_button'] = self.go_back_button
        return context

            

class GenericFormView(BaseContextMixin, BaseView, FormView):
    
    success_message = ""

    def get_page_subtitle(self):
        assert not self.page_subtitle or not self.page_subtitle_field, _(
            'Use either "page_subtitle" or "page_subtitle_field", not both')
        if self.page_subtitle:
            return self.page_subtitle
        if not self.page_subtitle_field:
            self.page_subtitle_field = 'pk'
        attr = getattr(self.get_object(), self.page_subtitle_field)
        return f'{self.page_subtitle_prefix}{attr}'

    def get_page_title(self):
        if self.page_title:
            return self.page_title
        if self.model:
            return self.model._meta.verbose_name
        queryset = self.get_queryset()
        if queryset:
            return queryset.model._meta.verbose_name
    
    def get_success_message(self, cleaned_data):
        return self.success_message

    def get_form_classes(self):
        return self.form_classes if hasattr(self, 'form_classes') else [self.form_class]

    def get_forms(self, form_classes=None):
        if form_classes is None:
            form_classes = self.get_form_classes()
        return [form_class(**self.get_forms_kwargs()) for form_class in form_classes]

    def get_forms_kwargs(self):
        kwargs = {}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        if 'forms' not in kwargs:
            kwargs['forms'] = self.get_forms()
        context = super().get_context_data(**kwargs)
        return context

    def forms_valid(self, forms):
        for form in forms:
            form.save()
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        forms = self.get_forms()
        if all([form.is_valid() for form in forms]):
            return self.forms_valid(forms)
        else:
            return self.forms_invalid(forms)
            
            
            
class GenericModelFormView(GenericFormView):
    def get_forms_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs


class GenericModelListView(BaseContextMixin,BaseView, ListView):
    template_name = 'generic_model_list.html'
    fields = None
    datetime_fields = []

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        self.model = self.get_queryset().model
        context['model'] = self.model
        context['items'] = self.get_queryset()
        context['fields'] = self.fields
        context['headers'] = self.get_table_headers()
        context['field_labels'] = self.field_labels
        context['datetime_fields'] = self.datetime_fields
        return context

    def get_table_headers(self) -> List[str]:
        headers = []
        for item in self.fields:
            headers.append(self.get_field_label(item))
        return headers

    def get_field_label(self, key: str) -> str:
        if key in self.field_labels:
            return self.field_labels[key]
        if '__' not in key:
            return self.model._meta.get_field(key).verbose_name
        model = self.model
        keys = key.split('__')
        for key in keys:
            model = model._meta.get_field(key).related_model or model
        return model._meta.get_field(key).verbose_name

