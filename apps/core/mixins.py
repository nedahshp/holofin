from django.contrib import messages
from django.urls import reverse


class CustomListTemplateMixin:
    fields = []
    page_title = ''
    page_subtitle = ''
    header_buttons = []
    action_buttons = []
    filter_class = None
    template_name = 'generic_model_list.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = self.get_queryset()
        context["fields"] = self.fields
        context["page_title"] = self.page_title
        context["page_subtitle"] = self.page_subtitle
        context["header_buttons"] = self.header_buttons
        context["action_buttons"] = self.action_buttons
        context["view"] = self
        if self.filter_class:
            context["filter_class"] = self.filter_class(self.request.GET)
        return context

    def get_page_title(self):
        return self.page_title
    
    def get_page_subtitle(self):
        return self.page_subtitle



class CustomFormTemplateMixin:
    page_title = ''
    page_subtitle = ''
    cancel_url = ''
    success_message = ''
    template_name = 'generic_model_multiform.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.get_page_title()
        context["page_subtitle"] = self.get_page_subtitle()
        context["cancel_url"] = self.get_cancel_url()
        context['forms'] = [self.get_form(), ]
        return context

    def form_valid(self, form):
        self.show_success_message()
        return super().form_valid(form)

    def get_page_title(self):
        return self.page_title
    
    def get_page_subtitle(self):
        return self.page_subtitle

    def get_cancel_url(self):
        return self.cancel_url

    def get_success_message(self):
        return self.success_message

    def show_success_message(self):
        message = self.get_success_message()
        if message:
            messages.success(self.request, message)
    

class CustomDeleteMixin:
    success_message = ''
    success_url = ''
    pk_url_kwarg = 'pk'
    model = None

    
    def get(self, request, *args, **kwargs):
        if not self.model:
            raise NotImplementedError("Model is not defined")
        return self.delete()

    def delete(self):
        obj = self.get_object()
        obj.delete()
        messages.success(self.request, self.get_success_message())
        return reverse(self.get_success_url())

    def get_object(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        obj = self.model.objects.get(pk=pk)
        return obj
        

    def get_success_message(self):
        return self.success_message

    def get_success_url(self):
        return self.success_url

