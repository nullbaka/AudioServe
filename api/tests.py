from django.test import TestCase, Client
from django.core.exceptions import ValidationError

import json

from .models import Podcast, Song, Audiobook


class PodcastModelsTest(TestCase):
    def test_participants_custom_validation(self):
        participants = ['a']*11
        participants = json.dumps(participants)
        item = Podcast(name='podcast', duration=1200, host='host', participants=participants)
        with self.assertRaises(ValidationError):
            item.full_clean()
        participants = json.dumps(['a', 'b'*101, 'c',])
        item = Podcast(name='podcast', duration=1200, host='host', participants=participants)
        with self.assertRaises(ValidationError):
            item.full_clean()
        participants = ['a'*100]*9 + ['a'*101]
        participants = json.dumps(participants)
        item = Podcast(name='podcast', duration=1200, host='host', participants=participants)
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_participants_max_value(self):
        participants = ['a'*100]*10
        participants = json.dumps(participants)
        item = Podcast(name='podcast', duration=1200, host='host', participants=participants)
        try:
            item.full_clean()
        except:
            raise Exception("Unexpected exception occurred.")


class SongViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        Song.objects.create(name='song1', duration=100)
        Song.objects.create(name='song2', duration=200)

    def test_create_view(self):
        song_data = {'name': 'song3'}
        response = self.client.post('/create/song/', song_data)
        self.assertEquals(response.status_code, 400)

        song_data['wrongparam'] = 'wrongparam'
        response = self.client.post('/create/song/', song_data)
        self.assertEquals(response.status_code, 400)

        song_data = {'name': 'song3', 'duration': 400}
        response = self.client.post('/create/song/', song_data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Song.objects.count(), 3)

    def test_update_view(self):
        update_data = {'wrongparam': 'wrongparam'}
        response = self.client.post('/update/song/1/', update_data)
        self.assertEquals(response.status_code, 400)

        update_data = {'duration': 300}
        response = self.client.post('/update/song/1/', update_data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Song.objects.get(id=1).duration, 300)

    def test_read_view(self):
        response = self.client.get('/read/song/2/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Song.objects.get(id=2).name, 'song2')

        response = self.client.get('/read/song/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.json()), 2)

    def test_delete_view(self):
        response = self.client.post('/delete/song/2/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Song.objects.count(), 1)


class PodcastViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.participants1 = ['participant1', 'participant2', 'participant3', 'participant4']
        self.participants1 = json.dumps(self.participants1)
        self.podcast = Podcast.objects.create(name='podcast1', duration=500, host='host1', participants=self.participants1)
        self.participants2 = ['participant1', 'participant2', 'participant3', 'participant4']
        self.participants2 = json.dumps(self.participants2)
        self.podcast = Podcast.objects.create(name='podcast2', duration=500, host='host2', participants=self.participants2)

    def test_create_view(self):
        podcast_data = {
            'name': 'podcast3',
            'duration': 600,
            'host': 'host3',
        }
        response = self.client.post('/create/podcast/', podcast_data)
        self.assertEquals(response.status_code, 400)
        
        podcast_data['participants'] = "participant1, participant2, participant3, participant4"
        response = self.client.post('/create/podcast/', podcast_data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Podcast.objects.count(), 3)
        self.assertEquals(len(json.loads(Podcast.objects.get(id=3).participants)), 4)

        podcast_data['wrongparam'] = 'wrongparam'
        response = self.client.post('/create/podcast/', podcast_data)
        self.assertEquals(response.status_code, 400)

    def test_update_view(self):
        update_data = {'wrongparam': 'wrongparam'}
        response = self.client.post('/update/podcast/2/', update_data)
        self.assertEquals(response.status_code, 400)

        update_data = {'name': 'new podcast'}
        response = self.client.post('/update/podcast/2/', update_data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Podcast.objects.get(id=2).name, 'new podcast')

    def test_read_view(self):
        response = self.client.get('/read/podcast/2/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Podcast.objects.get(id=2).name, 'podcast2')

        response = self.client.get('/read/podcast/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.json()), 2)

    def test_delete_view(self):
        response = self.client.post('/delete/podcast/2/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Podcast.objects.count(), 1)


class AudiobookViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.audiobook1 = Audiobook.objects.create(title='audiobook1', duration=1000, author='author1', narrator='narrator1')
        self.audiobook2 = Audiobook.objects.create(title='audiobook2', duration=2000, author='author2', narrator='narrator2')

    def test_create_view(self):
        audiobook_data = {'title': 'audiobook3'}
        response = self.client.post('/create/audiobook/', audiobook_data)
        self.assertEquals(response.status_code, 400)

        audiobook_data['wrongparam'] = 'wrongparam'
        response = self.client.post('/create/audiobook/', audiobook_data)
        self.assertEquals(response.status_code, 400)

        audiobook_data = {'title': 'audiobook3', 'duration': 3000, 'author': 'author3', 'narrator': 'narrator3'}
        response = self.client.post('/create/audiobook/', audiobook_data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Audiobook.objects.count(), 3)

    def test_update_view(self):
        update_data = {'wrongparam': 'wrongparam'}
        response = self.client.post('/update/audiobook/1/', update_data)
        self.assertEquals(response.status_code, 400)

        update_data = {'duration': 3000}
        response = self.client.post('/update/audiobook/1/', update_data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Audiobook.objects.get(id=1).duration, 3000)

    def test_read_view(self):
        response = self.client.get('/read/audiobook/2/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Audiobook.objects.get(id=2).title, 'audiobook2')

        response = self.client.get('/read/audiobook/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.json()), 2)

    def test_delete_view(self):
        response = self.client.post('/delete/audiobook/2/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Audiobook.objects.count(), 1)


class HttpErrorTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_status_400(self):
        response = self.client.get('/abc')
        self.assertEquals(response.status_code, 400)
        response = self.client.post('/create/s/')
        self.assertEquals(response.status_code, 400)
        response = self.client.get('/read/abc/')
        self.assertEquals(response.status_code, 400)
        response = self.client.post('/update/song/abc/')
        self.assertEquals(response.status_code, 400)
        response = self.client.get('/create/song/')
        self.assertEquals(response.status_code, 400)
