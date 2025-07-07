from django.db import models


# Create your models here.
class Details(models.Model):
    name = models.CharField(max_length=255)
    imdb_rating = models.FloatField("IMDB Rating", default=1)
    kinopoisk_rating = models.FloatField(default=1)
    image = models.CharField()
    description = models.TextField()

    class Meta:
        abstract = True


class Movie(Details):
    release_year = models.IntegerField()
    sources_list = models.JSONField(
        default=list,
        help_text="List of sources for the movie, e.g. ['source1', 'source2']",
    )

    def __str__(self):
        return f"Movie: {self.name} - {self.release_year} - {self.imdb_rating}"


class Show(Details):
    release_date = models.DateField()
    sources_list = models.JSONField(
        default=list,
        help_text="List of sources for the episode, e.g. ['source1', 'source2']",
    )

    def __str__(self):
        return f"Show: {self.name} - {self.release_date} - {self.imdb_rating}"


class Episode(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
