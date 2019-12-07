from django.views.generic import TemplateView

from . import models


class FAQ(TemplateView):
    template_name = "core/faq.html"

    def get_context_data(self, *args, **kwargs):
        faqs = models.FAQ.objects.all()
        selected_faq_slug = self.request.GET.get("faq")

        if selected_faq_slug is not None:
            selected_faq = models.FAQ.objects.filter(slug=selected_faq_slug).first()
        else:
            selected_faq = None

        return super().get_context_data(*args, faqs=faqs, selected_faq=selected_faq, **kwargs)
