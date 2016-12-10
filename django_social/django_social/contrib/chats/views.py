from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import ugettext as _
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
    return render(request, 'chats/chat.html', {'form': form,
                                               'room_id': int(room_id),
                                               'messages': messages,
                                               'last_message_id': last_message_id,
                                               'first_message_id': first_message_id,})


@login_required
def send_message(request, room_id):
    if request.is_ajax():
        try:
            room = Room.objects.get(pk=room_id)
        except Room.DoesNotExist:
            return JsonResponse({'error': _('Room does not exist')})

        form = ChatForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.room = room
            form.user = request.user
            form.save()
            return JsonResponse({'success': _('Success')})
        else:
            return JsonResponse({'error': form.errors})
    return JsonResponse({'error': _('Unknown request type')})


@login_required
def load_messages(request, room_id):
    if request.is_ajax() and request.method == "POST":
        try:
            room = Room.objects.get(pk=room_id)
        except Room.DoesNotExist:
            return JsonResponse({'error': _('Room does not exist')}, status=500)

        direction = request.POST.get('direction')
        start_id = request.POST.get('start_id')
        number = request.POST.get('number')

        if not any([direction, start_id, number]):
            return JsonResponse({'error': 'No POST data'}, status=500)

        number = int(number)
        if direction == 'backward':
            list_of_messages = Message.objects.filter(room=room, pk__lt=start_id).order_by('-pk')
        else:
            list_of_messages = Message.objects.filter(room=room, pk__gt=start_id).order_by('pk')

        if list_of_messages.count() == 0:
            if direction == 'backward':
                return JsonResponse({'messages': [], 'new_data': 0}, safe=False)
            else:
                return JsonResponse({'messages': [], 'new_data': start_id}, safe=False)
        elif list_of_messages.count() > number:
            list_of_messages = list_of_messages[:number]
            new_data = list_of_messages[number-1].pk
        else:
            new_data = list_of_messages[list_of_messages.count()-1].pk

        messages = [{'type': x.type,
                     'message': x.message,
                     'author': x.author.username,
                     'date': x.date.strftime('%d.%m.%Y %H:%M:%S'),
                     'file_name': x.get_file_name(),
                     'file_url': x.get_file_url()} for x in list_of_messages if x]

        return JsonResponse({'messages': messages, 'new_data': new_data}, safe=False)
    return JsonResponse({'error': _('Unknown request type')}, status=500)
