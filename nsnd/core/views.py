from os.path import join

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from PIL import Image, ImageDraw, ImageFont

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

        return super().get_context_data(
            *args, faqs=faqs, selected_faq=selected_faq, **kwargs
        )


@method_decorator(cache_page(9999, cache="thumbnails"), name="dispatch")
class FAQImage(View):
    def get(self, *args, **kwargs):
        faq = get_object_or_404(
            models.FAQ, slug=self.request.resolver_match.kwargs.get("slug")
        )
        resp = HttpResponse(content_type="image/png")
        text = faq.question

        img = Image.new("RGB", (1200, 630), color=(255, 255, 255))
        logo_img = Image.open(join(settings.BASE_DIR, "thumbnails", "logo.png"))

        font_size = 84 if len(text) < 110 else 50
        font = ImageFont.truetype(
            join(settings.BASE_DIR, "thumbnails", "Poppins-SemiBold.ttf"), font_size
        )

        line = ""
        lines = []
        width_of_line = 0
        number_of_lines = 0
        base_width, base_height = img.size
        font_character_width, font_character_height = (
            font.getsize("M")[0],
            font.getsize("M")[1],
        )
        padding = 32
        padded_width = base_width - padding - (logo_img.size[0] + padding)

        # Break text into multi-lines that fit base_width.
        for token in text.split():
            token = token + " "
            token_width = font.getsize(token)[0]

            if width_of_line + token_width < padded_width:
                line += token
                width_of_line += token_width
            else:
                lines.append(line)
                number_of_lines += 1
                width_of_line = 0
                line = ""
                line += token
                width_of_line += token_width

        if line:
            lines.append(line)
            number_of_lines += 1

        draw = ImageDraw.Draw(img)
        line_y = base_height - padding - sum(font.getsize(line)[1] for line in lines)

        # render each sentence
        for line in lines:
            width, height = font.getsize(line)
            draw.text((padding, line_y), line, font=font, fill=(82, 150, 67))
            line_y += height

        # Paste logo image in top-right corner.
        logo_pos = (base_width - logo_img.size[0] - padding, padding)
        img.paste(logo_img, logo_pos, mask=logo_img)

        img.save(resp, format="png")
        return resp
