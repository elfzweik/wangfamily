from django.db import models
from django.shortcuts import render
from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel

from visitor_record.utils import count_visits

class HomePage(Page):
    template = "home/home_page.html"

    banner_title = models.CharField (max_length=100, blank=False, null=True)
    banner_subtitle = RichTextField ()

    content = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel("banner_title"),
        FieldPanel("banner_subtitle"),
        InlinePanel('gallery_images', label="Gallery images"),
        FieldPanel("content")
    ]

    def get_context (self, request, *args, **kwargs):
        data = count_visits(request, self)
        context=super().get_context(request, *args, **kwargs)
        context['requestMETA'] = data['requestMETA']
        context['client_ip'] = data['client_ip']
        context['location'] = data['location']
        context['total_hits'] = data['total_hits']
        context['total_visitors'] =data['total_vistors']
        context['cookie'] = data['cookie']
        return context

    def serve(self, request):
        context = self.get_context(request)
        template = self.get_template(request)
        
        response = render(request, template, context)
        response.set_cookie(context['cookie'], 'true', max_age=3000)
        return response

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"

class BannerGalleryImage(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', blank=False, on_delete=models.CASCADE, related_name='+'
    )
    

    panels = [
        ImageChooserPanel('image'),
    ]