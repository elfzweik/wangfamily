from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from wagtail.core.models import Page
from wagtail.search.models import Query

from .models import BlogDetailPage
from visitor_record.utils import count_visits

# Create your views here.

def category_view(request):
    category = request.GET.get('category','')

    blogpages = BlogDetailPage.objects.live().filter(categories__name=category).order_by('-first_published_at')

    paginator = Paginator(blogpages, 12)
    page_num = request.GET.get('page', 1)
    
    try:
        blogpage = paginator.get_page(page_num)
    except PageNotAnInteger:
        blogpage = paginator.get_page(1)
        page_num=1
    except EmptyPage:
        blogpage = paginator.get_page(paginator.num_pages)
        page_num = paginator.num_pages
    page_range = list(range(max(int(page_num)-2, 1), int(page_num))) + \
        list(range(int(page_num), min(int(page_num)+2, paginator.num_pages)+1))
    if page_range[0]-1 > 1:
        page_range.insert(0,'...')
        page_range.insert(0,1)
    elif page_range[0]-1 == 1:
        page_range.insert(0,1)

    if paginator.num_pages - page_range[-1] > 1:
        page_range.append('...')
        page_range.append(paginator.num_pages)
    elif paginator.num_pages - page_range[-1] == 1:
        page_range.append(paginator.num_pages)


    # Update template context
    data = count_visits(request, BlogDetailPage.objects.all()[0])

    context = {}
    context['posts'] = blogpage
    context['page_range'] = page_range
    context['caption'] = "Pages in Category \"" + category +"\""
    context['category'] = category

    context['client_ip'] = data['client_ip']
    context['location'] = data['location']
    context['total_hits'] = data['total_hits']
    context['total_visitors'] =data['total_vistors']
    context['cookie'] = data['cookie']
    response = render(request, 'blog/blog_cat_listing_page.html', context)
    response.set_cookie(context['cookie'], 'true', max_age=300)
    return response