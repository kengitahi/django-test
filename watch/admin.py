from django.contrib import admin

from .models import Movie, Show


# Register your models here.
class MovieAdmin(admin.ModelAdmin):
    list_display = ("name", "release_year", "imdb_rating")
    search_fields = ("name", "release_year")


class ShowAdmin(admin.ModelAdmin):
    list_display = ("name", "release_date", "imdb_rating")
    search_fields = ("name", "release_date")


admin.site.register(Movie, MovieAdmin)
admin.site.register(Show, ShowAdmin)
