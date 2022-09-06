from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from notifications.models import Notification
from blog.models import BlogDetailPage
from visitor_record.utils import count_visits

def my_notifications(request):
    obj = BlogDetailPage.objects.all()[0]
    data = count_visits(request, obj)

    context = {}
    context['client_ip'] = data['client_ip']
    context['location'] = data['location']
    context['total_hits'] = data['total_hits']
    context['total_visitors'] =data['total_vistors']
    context['cookie'] = data['cookie']
    response = render(request, 'my_notifications/my_notifications.html', context)
    response.set_cookie(context['cookie'], 'true', max_age=300)
    return response
    
def my_notification(request, my_notification_pk):
    my_notification = get_object_or_404(Notification, pk=my_notification_pk)
    my_notification.unread = False
    my_notification.save()
    return redirect(my_notification.data['url'])

def delete_my_read_notifications(request):
    notifications = request.user.notifications.read()
    notifications.delete()
    return redirect(reverse('my_notifications'))