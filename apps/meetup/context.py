from __future__ import annotations

from django.urls import reverse_lazy

from .models import Event, Executive

ANNOUNCEMENT_THRESHOLD = 14


def menu(request):
    menu_items = (
        {'title': 'События', 'url': 'events'},
        {'title': 'Видео', 'url': 'https://www.youtube.com/moscowdjangoru'},
        {'title': 'Группа Facebook', 'url': 'https://www.facebook.com/groups/MoscowDjango/'},
        {'title': 'Люди', 'url': 'speakers'},
        {'title': 'О проекте', 'url': 'about'},
    )

    for item in menu_items:
        if item['url'] is not None:
            if item['url'].startswith('http'):
                item['external'] = True
            else:
                item['external'] = False
                item['url'] = reverse_lazy(item['url'])

    return {'menu_items': menu_items}


def all_events_processor(request):
    show_announcement = False
    try:
        latest_event = Event.visible.all().latest()
        days_to_next_event = latest_event.days_delta()
        if days_to_next_event is not None and days_to_next_event <= ANNOUNCEMENT_THRESHOLD:
            show_announcement = True
    except Event.DoesNotExist:
        latest_event = None
        days_to_next_event = None
    return {
        'all_events': Event.visible.all(),
        'show_announcement': show_announcement,
        'streaming_url': latest_event.streaming_url if latest_event else None,
        'days_to_next_event': days_to_next_event,
        'next_event_time': latest_event.date if latest_event else None,
    }


def executives(request):
    return {"executives": Executive.objects.all()}
