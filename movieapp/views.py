from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, JsonResponse
import json
import models

@csrf_exempt
def index(request):
    return HttpResponse("Hello! You're at the movieapp index.")

@csrf_exempt
def add_movie(request):
    if request.method == 'POST':
        movie_dict = json.loads(request.body)
        required_fields = ["name", "actors", "directors", "release_year", "imdb_rating", "genre"]
        for rf in required_fields:
            if rf not in movie_dict:
                return JsonResponse({"message": "Missing field(name/actors/directors/release_year/imdb_rating) in "
                                                "the request body!"})
        actors = models.Actor.objects.filter(id__in=movie_dict["actors"])
        directors = models.Director.objects.filter(id__in=movie_dict["directors"])
        genre = models.Genre.objects.filter(id=movie_dict["genre"]).first()
        if not actors or not directors or not genre:
            return JsonResponse({"message":"One or more entries in actors/directors/genre is/are invalid    "})
        m = models.Movie.objects.create(name=movie_dict["name"], release_year=movie_dict["release_year"],
                                        imdb_rating=movie_dict["imdb_rating"], genre_id=genre.id)
        for a in actors:
            m.actors.add(a)
        for d in directors:
            m.directors.add(d)
        created_movie = {"id":m.id, "name":m.name, "release_year":m.release_year}
        return JsonResponse(created_movie)
    else:
        message = "Not a POST request. Can't create movie."
    message_dict = {"message":message}
    return JsonResponse(message_dict)


@csrf_exempt
def search_movie(request):
    if request.method == 'GET':
        movie_name = request.GET.get('name')
        actor_name = request.GET.get('actor')
        director_name = request.GET.get('director')
        m = models.Movie.objects.filter()
        if movie_name:
            m = models.Movie.objects.filter(name__contains=movie_name)
        if actor_name:
            actor_query = models.Actor.objects.filter(name=actor_name)
            if not actor_query.exists():
                message = "Actor with name: %s doesn't exist!" % actor_name
                return JsonResponse({"message":message})
            else:
                m = m.filter(actors__name=actor_name)
        if director_name:
            director_query = models.Director.objects.filter(name=director_name)
            if not director_query.exists():
                message = "Director with name: %s doesn't exist!" %director_name
                return JsonResponse({"message":message})
            else:
                m = m.filter(directors__name=director_name)
        movies = [mv.asDict() for mv in m]

        return JsonResponse({"movies": movies})
    else:
        message = "Not a GET request. Can't search for movies."
    message_dict = {"message":message}
    return JsonResponse(message_dict)


@csrf_exempt
def get_top_rated(request):
    if request.method == 'GET':
        genre_name = request.GET.get('genre')
        limit = request.GET.get('limit')
        m = models.Movie.objects.filter()
        if genre_name:
            genre_query = models.Genre.objects.filter(name=genre_name)
            if not genre_query.exists():
                message = "Genre with name: %s doesn't exist!" % genre_name
                return JsonResponse({"message":message})
            else:
                m = m.filter(genre__name=genre_name)
        m = m.order_by('-imdb_rating')
        if limit:
            m = m[:limit]
        movies = [mv.asDict() for mv in m]
        return JsonResponse({"movies": movies})
    else:
        message = "Not a GET request. Can't get top rated movies."
    message_dict = {"message": message}
    return JsonResponse(message_dict)


@csrf_exempt
def add_actor(request):
    if request.method == 'POST':
        actor_dict = json.loads(request.body)
        if "name" in actor_dict:
            actor_query = models.Actor.objects.filter(name=actor_dict["name"])
            if actor_query.exists():
                message = "Actor with name: %s already exists!"
            else:
                actor = models.Actor.objects.create(name=actor_dict["name"])
                message = "Created Actor!"
        else:
            message = "Missing field: name in the request body"
    else:
        message = "Not a POST request. Can't create actor."
    message_dict = {"message":message}
    return JsonResponse(message_dict)


@csrf_exempt
def add_director(request):
    if request.method == 'POST':
        director_dict = json.loads(request.body)
        if "name" in director_dict:
            actor_query = models.Director.objects.filter(name=director_dict["name"])
            if actor_query.exists():
                message = "Director with name: %s already exists!"
            else:
                d = models.Director.objects.create(name=director_dict["name"])
                message = "Created Director!"
        else:
            message = "Missing field: name in the request body"
    else:
        message = "Not a POST request. Can't create director."
    message_dict = {"message":message}
    return JsonResponse(message_dict)


@csrf_exempt
def add_genre(request):
    if request.method == 'POST':
        genre_dict = json.loads(request.body)
        if "name" in genre_dict:
            genre_query = models.Genre.objects.filter(name=genre_dict["name"])
            if genre_query.exists():
                message = "genre with name: %s already exists!"
            else:
                d = models.Genre.objects.create(name=genre_dict["name"])
                message = "Created genre!"
        else:
            message = "Missing field: name in the request body"
    else:
        message = "Not a POST request. Can't create genre."
    message_dict = {"message":message}
    return JsonResponse(message_dict)
