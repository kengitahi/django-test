from django.db import models


# Create your models here.
class Details(models.Model):
    name = models.CharField(max_length=255)
    imdb_rating = models.CharField("IMDB Rating", default="1.0")
    kinopoisk_rating = models.CharField("Kinopoisk Rating", default="1.0")
    image = models.CharField()
    description = models.TextField()

    class Meta:
        abstract = True


class Movie(Details):
    release_year = models.CharField()
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
        return f"{self.name}"


class Season(models.Model):
    number = models.IntegerField("The Season Number")
    show = models.ForeignKey(Show, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.show.name}, Season: {self.number}"


class Episode(models.Model):
    number = models.IntegerField("The Episode Number")
    name = models.CharField(max_length=255)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.season.show.name}, Season: {self.season.number}, Eposide: {self.number}"
