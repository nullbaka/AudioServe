from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.views import View

import json

from .models import Song, Podcast, Audiobook


INVALID_REQUEST_MESSAGE = "Invalid request."


class CreateView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(INVALID_REQUEST_MESSAGE, status=400)

    def post(self, request, *args, **kwargs):
        audioType = kwargs['audioType'].lower()
        if audioType == 'song' and self.save_song_to_db(request):
            return HttpResponse("Song successfully created.")
        elif audioType == 'podcast' and self.save_podcast_to_db(request):
            return HttpResponse("Podcast successfully created.")
        elif audioType == 'audiobook' and self.save_audiobook_to_db(request):
            return HttpResponse("Audiobook successfully created.")
        else:
            return HttpResponse(INVALID_REQUEST_MESSAGE, status=400)

    def save_song_to_db(self, request):
        keys = [key for key in request.POST.keys()]
        fields = ['name', 'duration']
        if set(keys) != set(fields):
            return False
        name = request.POST.get('name')
        duration = request.POST.get('duration')
        item = Song(name=name, duration=duration)
        try:
            item.full_clean()
            item.save()
        except ValidationError:
            return False
        return True

    def save_podcast_to_db(self, request):
        keys = [key for key in request.POST.keys()]
        fields = ['name', 'host', 'participants', 'duration']
        if set(keys) != set(fields):
            return False
        name = request.POST.get('name')
        duration = request.POST.get('duration')
        host = request.POST.get('host')
        participants = request.POST.get('participants')
        participants = participants.split(',')
        participants = [p.strip() for p in participants]
        participants = json.dumps(participants)
        item = Podcast(name=name, duration=duration, host=host, participants=participants)
        try:
            item.full_clean()
            item.save()
        except ValidationError:
            return False
        return True

    def save_audiobook_to_db(self, request):
        keys = [key for key in request.POST.keys()]
        fields = ['title', 'author', 'narrator', 'duration']
        if set(keys) != set(fields):
            return False
        title = request.POST.get('title')
        author = request.POST.get('author')
        narrator = request.POST.get('narrator')
        duration = request.POST.get('duration')
        item = Audiobook(title=title, author=author, narrator=narrator, duration=duration)
        try:
            item.full_clean()
            item.save()
        except ValidationError:
            return False
        return True


class UpdateView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(INVALID_REQUEST_MESSAGE, status=400)

    def post(self, request, *args, **kwargs):
        audioType = kwargs['audioType'].lower()
        audioFileID = kwargs['audioFileID']
        if audioType == 'song' and self.update_song(audioFileID, request):
            return HttpResponse("Song successfully updated.")
        elif audioType == 'podcast' and self.update_podcast(audioFileID, request):
            return HttpResponse("Podcast successfully updated.")
        elif audioType == 'audiobook' and self.update_audiobook(audioFileID, request):
            return HttpResponse("Audiobook successfully updated.")
        return HttpResponse(INVALID_REQUEST_MESSAGE, status=400)

    def update_song(self, audioFileID, request):
        keys = [key for key in request.POST.keys()]
        fields = ['name', 'duration']
        if not all(x in fields for x in keys):
            return False
        try:
            item = Song.objects.get(id=audioFileID)
        except Song.DoesNotExist:
            return False
        name = request.POST.get('name')
        duration = request.POST.get('duration')
        if name:
            item.name = name
        if duration:
            item.duration = duration
        try:
            item.full_clean()
        except ValidationError:
            return False
        item.save()
        return True

    def update_podcast(self, audioFileID, request):
        keys = [key for key in request.POST.keys()]
        fields = ['name', 'host', 'participants', 'duration']
        if not all(x in fields for x in keys):
            return False
        try:
            item = Podcast.objects.get(id=audioFileID)
        except Podcast.DoesNotExist:
            return False
        name = request.POST.get('name')
        host = request.POST.get('host')
        participants = request.POST.get('participants')
        if participants:
            participants = participants.split(',')
            participants = [p.strip() for p in participants]
            participants = json.dumps(participants)
        duration = request.POST.get('duration')
        if name:
            item.name = name
        if host:
            item.host = host
        if participants:
            item.participants = participants
        if duration:
            item.duration = duration
        try:
            item.full_clean()
        except ValidationError:
            return False
        item.save()
        return True

    def update_audiobook(self, audioFileID, request):
        keys = [key for key in request.POST.keys()]
        fields = ['title', 'author', 'narrator', 'duration']
        if not all(x in fields for x in keys):
            return False
        try:
            item = Audiobook.objects.get(id=audioFileID)
        except Audiobook.DoesNotExist:
            return False
        title = request.POST.get('title')
        author = request.POST.get('author')
        narrator = request.POST.get('narrator')
        duration = request.POST.get('duration')
        if title:
            item.title = title
        if author:
            item.author = author
        if narrator:
            item.narrator = narrator
        if duration:
            item.duration = duration
        try:
            item.full_clean()
        except ValidationError:
            return False
        item.save()
        return True


class ReadView(View):
    def get(self, request, *args, **kwargs):
        audioType = kwargs['audioType'].lower()
        try:
            audioFileID = kwargs['audioFileID']
        except KeyError:
            audioFileID = None
        if audioType == 'song':
            result = self.read_song(audioFileID)
            if result:
                return JsonResponse(result, safe=False)
        elif audioType == 'podcast':
            result = self.read_podcast(audioFileID)
            if result:
                return JsonResponse(result, safe=False)
        elif audioType == 'audiobook':
            result = self.read_audiobook(audioFileID)
            if result:
                return JsonResponse(result, safe=False)
        return HttpResponse(INVALID_REQUEST_MESSAGE, status=400)

    def read_song(self, audioFileID):
        if not audioFileID:
            songs_ = Song.objects.all()
            songs = []
            for song in songs_:
                temp = {}
                temp['id'] = song.id
                temp['name'] = song.name
                temp['duration'] = song.duration
                songs.append(temp)
            return songs
        else:
            try:
                song = Song.objects.get(id=audioFileID)
            except Song.DoesNotExist:
                return False
            song = {
                'id': song.id,
                'name': song.name,
                'duration': song.duration
            }
            return song

    def read_podcast(self, audioFileID):
        if not audioFileID:
            podcasts_ = Podcast.objects.all()
            podcasts = []
            for podcast in podcasts_:
                temp = {}
                temp['id'] = podcast.id
                temp['name'] = podcast.name
                temp['duration'] = podcast.duration
                temp['host'] = podcast.host
                temp['participants'] = json.loads(podcast.participants)
                podcasts.append(temp)
            return podcasts
        else:
            try:
                podcast = Podcast.objects.get(id=audioFileID)
            except Podcast.DoesNotExist:
                return False
            podcast = {
                'id': podcast.id,
                'name': podcast.name,
                'duration': podcast.duration,
                'host': podcast.host,
                'participants': json.loads(podcast.participants)
            }
            return podcast

    def read_audiobook(self, audioFileID):
        if not audioFileID:
            audiobooks_ = Audiobook.objects.all()
            audiobooks = []
            for audiobook in audiobooks_:
                temp = {}
                temp['id'] = audiobook.id
                temp['title'] = audiobook.title
                temp['duration'] = audiobook.duration
                temp['author'] = audiobook.author
                temp['narrator'] = audiobook.narrator
                audiobooks.append(temp)
            return audiobooks
        else:
            try:
                audiobook = Audiobook.objects.get(id=audioFileID)
            except Audiobook.DoesNotExist:
                return False
            audiobook = {
                'id': audiobook.id,
                'title': audiobook.title,
                'duration': audiobook.duration,
                'author': audiobook.author,
                'narrator': audiobook.narrator
            }
            return audiobook

    def post(self, request, *args, **kwargs):
        return HttpResponse(INVALID_REQUEST_MESSAGE, status=400)


class DeleteView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(INVALID_REQUEST_MESSAGE, status=400)

    def post(self, request, *args, **kwargs):
        audioType = kwargs['audioType'].lower()
        audioFileID = kwargs['audioFileID']
        if audioType == 'song':
            try:
                song = Song.objects.get(id=audioFileID)
            except Song.DoesNotExist:
                return HttpResponse(INVALID_REQUEST_MESSAGE, status=400)
            song.delete()
            return HttpResponse("Song deleted.")
        elif audioType == 'podcast':
            try:
                podcast = Podcast.objects.get(id=audioFileID)
            except Podcast.DoesNotExist:
                return HttpResponse(INVALID_REQUEST_MESSAGE, status=400)
            podcast.delete()
            return HttpResponse("Podcast deleted.")
        elif audioType == 'audiobook':
            try:
                audiobook = Audiobook.objects.get(id=audioFileID)
            except Audiobook.DoesNotExist:
                return HttpResponse(INVALID_REQUEST_MESSAGE, status=400)
            audiobook.delete()
            return HttpResponse("Audiobook deleted.")
        else:
            return HttpResponse(INVALID_REQUEST_MESSAGE, status=400)


def handle4xx(request, exception):
    return HttpResponse(INVALID_REQUEST_MESSAGE, status=400)


def handle500(request):
    return HttpResponse("Internal server error.", status=500)
