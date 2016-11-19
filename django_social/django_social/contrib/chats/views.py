from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.formats import date_format
from django.contrib.auth.decorators import login_required

from .models import Room, Message
from .forms import ChatForm



@login_required
def index(request):
    rooms = Room.objects.all()
    return render(request, 'chats/index.html', {'rooms': rooms})


@login_required
def load_form(request, room_id):
    room, created = Room.objects.get_or_create(pk=room_id)
    form = ChatForm()
    last_message_id = 0
    first_message_id = 0
    if not created:
        messages = room.messages().order_by('-id')[:20]
        if messages:
            last_message_id = messages.first().pk
            first_message_id = messages[messages.count()-1].pk
        messages = reversed(messages)
    else:
        messages = None
    return render(request, 'chats/form.html', {'form': form,
                                               'room_id': int(room_id),
                                               'messages': messages,
                                               'last_message_id': last_message_id,
                                               'first_message_id': first_message_id,})


@login_required
def send_message(request, room_id):
    if request.is_ajax():
        message = request.POST.get('message')
        room, created = Room.objects.get_or_create(pk=room_id)
        room.add_message('m', request.user, message)
    return HttpResponse('')


def sync_messages(request, room_id):
    if request.is_ajax():
        last_message_id = request.POST.get('last_message_id')
        new_messages = Message.objects.filter(room_id=room_id, pk__gt=last_message_id)
        last_message = new_messages.last()
        if last_message:
            last_message_id = last_message.pk
        messages = [{'date': x.date.strftime('%d.%m.%Y %H:%M:%S'),
                     'message': x.message,
                     'type': x.type} for x in new_messages if x]
    return JsonResponse({'new_messages': messages,
                         'last_message_id': last_message_id})


def get_previous(request, room_id):
    if request.is_ajax():
        first_message_id = request.POST.get('first_message_id')
        offset = 2
        # Last 20 messages
        previous_messages = Message.objects.filter(room_id=room_id,
                                                   pk__lt=first_message_id).order_by('-id')[:offset]
        if previous_messages:
            first_message_id = previous_messages[offset-1].pk

        messages = [{'date': x.date.strftime('%d.%m.%Y %H:%M:%S'),
                     'message': x.message,
                     'type': x.type} for x in previous_messages if x]
    return JsonResponse({'previous_messages': messages,
                         'first_message_id': first_message_id})
