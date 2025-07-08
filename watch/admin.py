from django.contrib import admin

from .models import Episode, Movie, Season, Show


class MovieAdmin(admin.ModelAdmin):
    list_display = ("name", "release_year", "imdb_rating", "kinopoisk_rating")
    search_fields = ("name", "release_year")


class ShowAdmin(admin.ModelAdmin):
    list_display = ("name", "release_date", "imdb_rating", "kinopoisk_rating")
    search_fields = ("name", "release_date")


class SeasonAdmin(admin.ModelAdmin):
    ordering = ["number"]
    list_display = ["number", "show"]
    search_fields = ["show__name"]


class EpisodeAdmin(admin.ModelAdmin):
    ordering = ["number"]
    list_display = ["number", "name", "season__show"]


admin.site.register(Movie, MovieAdmin)
admin.site.register(Show, ShowAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Episode, EpisodeAdmin)
