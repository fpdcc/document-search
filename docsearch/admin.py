from django.contrib import admin

from docsearch import models

admin.site.site_header = 'Forest Preserve of Cook County Document Search Admin'
admin.site.site_title = 'Document Search'


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ControlMonumentMap)
class ControlMonumentMapAdmin(admin.ModelAdmin):
    pass


@admin.register(models.SurplusParcel)
class SurplusParcelAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Dossier)
class DossierAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Easement)
class EasementAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FlatDrawing)
class FlatDrawingAdmin(admin.ModelAdmin):
    pass


@admin.register(models.IndexCard)
class IndexCardAdmin(admin.ModelAdmin):
    pass


@admin.register(models.License)
class LicenseAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    pass


@admin.register(models.RightOfWay)
class RightOfWayAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Survey)
class SurveyAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Title)
class TitleAdmin(admin.ModelAdmin):
    pass
