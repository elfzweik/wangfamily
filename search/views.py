from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse
from django.db.models import Q
from wagtail.core.models import Page
from wagtail.search.models import Query

from blog.models import BlogDetailPage
from visitor_record.utils import count_visits

def search(request):
    search_query = request.GET.get('query', None).strip()
    page_num = request.GET.get('page', 1)
    
    # Search 分词： 按空格 & | ~
    condition = None
    for word in search_query.split(' '):
        if condition is None:
            condition = Q(custom_title__icontains=word) | Q(intro__icontains=word) | Q(content__icontains=word)
        else:
            condition = condition | Q(custom_title__icontains=word) | Q(intro__icontains=word) | Q(content__icontains=word)

    search_results = []
    if condition is not None:
        # 筛选：搜索
        search_results = BlogDetailPage.objects.live().filter(condition).order_by('-first_published_at')
        '''if search_query:
        #search_results = BlogDetailPage.objects.live().search(search_query, operator='or')
        search_results = BlogDetailPage.objects.live().filter(
                Q(custom_title_icontains = search_query) |
                Q(intro_icontains = search_query) | 
                Q(content_icontains = search_query) |
                Q(tags_icontains = search_query) 
            )
        '''
        query = Query.get(search_query)
        print(search_results)
        # Record hit
        query.add_hit()
    else:
        search_results = BlogDetailPage.objects.none()

    # Pagination
    paginator = Paginator(search_results, 12)
    try:
        search_results = paginator.page(page_num)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

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
    
    data = count_visits(request, BlogDetailPage.objects.all()[0])

    context = {}
    context['client_ip'] = data['client_ip']
    context['location'] = data['location']
    context['total_hits'] = data['total_hits']
    context['total_visitors'] =data['total_vistors']
    context['cookie'] = data['cookie']

    context['search_query'] = search_query
    context['search_results'] = search_results
    context['page_range'] = page_range
    response = TemplateResponse(request, 'search/search_result.html', context)
    response.set_cookie(context['cookie'], 'true', max_age=300)
    return response
