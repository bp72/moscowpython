from __future__ import annotations

from django.test import TestCase
from django.urls import reverse

from apps.meetup.models import Event, Photo, Speaker, Talk


def create_events():
    act = Event.objects.create(number=1, name='Active', status=Event.STATUS.active)
    drf = Event.objects.create(number=2, name='Draft', status=Event.STATUS.draft)
    pln = Event.objects.create(number=3, name='Planning', status=Event.STATUS.planning)
    arc = Event.objects.create(number=4, name='Archived', status=Event.STATUS.archived)
    return act, drf, pln, arc


class IndexSystem(TestCase):
    """Integration tests for index page"""

    def test_main_event(self):
        self.main_event = Event.objects.create(pk=1, number=2, name='Upcoming Meetup', status=Event.STATUS.active)
        self.passed_event = Event.objects.create(pk=2, number=1, name='Passed Meetup', status=Event.STATUS.archived)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.context['main_event'], self.main_event)

    def test_no_active_event(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.context['main_event'], None)

    def test_planning_event(self):
        Event.objects.create(number=2, name='Archived', status=Event.STATUS.archived)
        pln = Event.objects.create(number=3, name='Planning', status=Event.STATUS.planning)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.context['main_event'], pln)

    def test_archived_events(self):
        act, drf, pln, arc = create_events()
        response = self.client.get(reverse('index'))
        self.assertQuerySetEqual(response.context['events'], [arc])


class EventList(TestCase):
    """Integration tests for events list page"""

    def test_event_list(self):
        act, drf, pln, arc = create_events()
        response = self.client.get(reverse('events'))
        self.assertQuerySetEqual(response.context['events'], [event for event in [act, pln, arc]])


class EventsPage(TestCase):
    """Integration tests for event detail page"""

    def setUp(self):
        self.act, self.drf, self.pln, self.arc = create_events()

    def test_active_event_page(self):
        response = self.client.get(reverse('event', args=[1]))
        self.assertEqual(response.context['event'], self.act)

    def test_draft_event_page(self):
        response = self.client.get(reverse('event', args=[2]))
        self.assertEqual(response.status_code, 404)


class TalkPage(TestCase):
    """Integration tests for event detail page"""

    def setUp(self):
        event = Event.objects.create(number=1, name='Active', status=Event.STATUS.active)
        speaker = Speaker.objects.create(name='Speaker', slug='slug')
        self.talk = Talk.objects.create(
            name='Talk', slug='slug', event=event, speaker=speaker, status=Talk.STATUS.active
        )

    def test_talk_page_active(self):
        response = self.client.get(reverse('talk', args=[1, 'slug']))
        self.assertEqual(response.context['talk'], self.talk)

    def test_talk_page_inactive(self):
        self.talk.status = Talk.STATUS.draft
        self.talk.save()
        response = self.client.get(reverse('talk', args=[1, 'slug']))
        self.assertEqual(response.status_code, 404)

    def test_talk_page_order(self):
        pass


class SpeakerList(TestCase):
    """Integration tests for speaker list page"""

    def test_speakers(self):
        speaker1 = Speaker.objects.create(name='Speaker1', slug='slug1')
        speaker2 = Speaker.objects.create(name='Speaker2', slug='slug2')
        response = self.client.get(reverse('speakers'))
        self.assertQuerySetEqual(response.context['speakers'], [speaker1, speaker2])


class SpeakerDetail(TestCase):
    """Integration tests for speaker detail page"""

    def test_speaker(self):
        speaker = Speaker.objects.create(name='Speaker1', slug='slug')
        response = self.client.get(reverse('speaker', args=['slug']))
        self.assertEqual(response.context['speaker'], speaker)


class AboutPage(TestCase):
    """Integration tests for speaker list page"""

    def test_page(self):
        photo1 = Photo.objects.create(image='_', caption='1')
        photo2 = Photo.objects.create(image='^', caption='2')
        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'about.html')
        self.assertQuerySetEqual(response.context['photos'], [photo2, photo1])


class LivePage(TestCase):
    """Integration tests for live page"""

    def test_page(self):
        response = self.client.get(reverse('live'))
        self.assertTemplateUsed(response, 'live.html')
        self.assertEqual(response.context['event'], None)
