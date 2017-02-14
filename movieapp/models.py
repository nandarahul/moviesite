from __future__ import unicode_literals

from django.db import models


class Actor(models.Model):
    name = models.CharField(max_length=50)


class Director(models.Model):
    name = models.CharField(max_length=50)


class Genre(models.Model):
    name = models.CharField(max_length=50)


class Movie(models.Model):
    name = models.CharField(max_length=50)
    actors = models.ManyToManyField(Actor)
    directors = models.ManyToManyField(Director)
    genre = models.ForeignKey(Genre)
    release_year = models.IntegerField()
    imdb_rating = models.FloatField()

    def asDict(self):
        return {"name": self.name, "release_year": self.release_year, "imdb_rating": self.imdb_rating,
                "genre": self.genre.name,
                "actors": [{"id": a.id, "name": a.name} for a in self.actors.all()],
                "directors": [{"id": d.id, "name": d.name} for d in self.directors.all()]
               }



