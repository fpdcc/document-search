from haystack import indexes, fields

from docsearch import models


class IntegerMultiValueField(fields.MultiValueField):
    field_type = 'integer'


class BookIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    township = indexes.CharField(model_attr='township', faceted=True)
    section = indexes.CharField(model_attr='section', null=True, faceted=True)
    range = indexes.CharField(model_attr='range', faceted=True)

    def get_model(self):
        return models.Book


class ControlMonumentMapIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    township = indexes.CharField(model_attr='township', null=True, faceted=True)
    range = indexes.CharField(model_attr='range', null=True, faceted=True)
    section_arr = IntegerMultiValueField(model_attr='section', null=True, faceted=True)
    part_of_section = indexes.CharField(model_attr='part_of_section', null=True, faceted=True)

    def get_model(self):
        return models.ControlMonumentMap


class SurplusParcelIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    surplus_parcel = indexes.CharField(model_attr='surplus_parcel', null=True, faceted=True)
    description = indexes.CharField(model_attr='description', null=True)

    def get_model(self):
        return models.SurplusParcel


class DeepTunnelIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    description = indexes.CharField(model_attr='description')

    def get_model(self):
        return models.DeepTunnel


class DossierIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    file_number = indexes.CharField(model_attr='file_number', faceted=True)
    document_number = indexes.CharField(model_attr='document_number', faceted=True)

    def get_model(self):
        return models.Dossier


class EasementIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    easement_number = indexes.CharField(model_attr='easement_number', null=True, faceted=True)
    description = indexes.CharField(model_attr='description', null=True)

    def get_model(self):
        return models.Easement


class FlatDrawingIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    section = indexes.IntegerField(model_attr='section', null=True, faceted=True)
    map_number = indexes.CharField(model_attr='map_number', null=True, faceted=True)
    location = indexes.CharField(model_attr='location', null=True, faceted=True)
    description = indexes.CharField(model_attr='description', null=True, faceted=True)
    job_number = indexes.CharField(model_attr='job_number', null=True, faceted=True)
    number_of_sheets = indexes.CharField(model_attr='number_of_sheets', null=True, faceted=True)
    date = indexes.CharField(model_attr='date', null=True, faceted=True)
    cross_ref_area = indexes.IntegerField(model_attr='cross_ref_area', null=True, faceted=True)
    cross_ref_section = indexes.IntegerField(model_attr='cross_ref_section', null=True, faceted=True)
    cross_ref_map_number = indexes.CharField(model_attr='cross_ref_map_number', null=True, faceted=True)
    hash = indexes.CharField(model_attr='hash', null=True, faceted=True)

    def get_model(self):
        return models.FlatDrawing


class IndexCardIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    monument_number = indexes.CharField(model_attr='monument_number', null=True, faceted=True)
    township = indexes.CharField(model_attr='township', faceted=True)
    section = indexes.CharField(model_attr='section', null=True, faceted=True)
    corner = indexes.CharField(model_attr='corner', null=True, faceted=True)

    def get_model(self):
        return models.IndexCard


class LicenseIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    license_number = indexes.CharField(model_attr='license_number', null=True, faceted=True)
    description = indexes.CharField(model_attr='description', null=True)

    def get_model(self):
        return models.License


class ProjectFileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    area = indexes.IntegerField(model_attr='area', null=True, faceted=True)
    section = indexes.IntegerField(model_attr='section', null=True, faceted=True)
    job_number = indexes.CharField(model_attr='job_number', null=True, faceted=True)
    job_name = indexes.CharField(model_attr='job_name', null=True, faceted=True)
    description = indexes.CharField(model_attr='description', null=True)
    cabinet_number = indexes.CharField(model_attr='cabinet_number', null=True, faceted=True)
    drawer_number = indexes.CharField(model_attr='drawer_number', null=True, faceted=True)

    def get_model(self):
        return models.ProjectFile


class RightOfWayIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    folder_tab = indexes.CharField(model_attr='folder_tab', faceted=True)

    def get_model(self):
        return models.RightOfWay


class SurveyIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    township_arr = IntegerMultiValueField(model_attr='township', null=True, faceted=True)
    range_arr = IntegerMultiValueField(model_attr='range', null=True, faceted=True)
    section_arr = IntegerMultiValueField(model_attr='section', null=True, faceted=True)
    map_number = indexes.CharField(model_attr='map_number', null=True, faceted=True)
    location = indexes.CharField(model_attr='location', null=True, faceted=True)
    description = indexes.CharField(model_attr='description', null=True)
    job_number = indexes.CharField(model_attr='job_number', null=True, faceted=True)
    number_of_sheets = indexes.CharField(model_attr='number_of_sheets', null=True, faceted=True)
    date = indexes.CharField(model_attr='date', null=True, faceted=True)
    cross_ref_area = indexes.IntegerField(model_attr='cross_ref_area', null=True, faceted=True)
    cross_ref_section = indexes.IntegerField(model_attr='cross_ref_section', null=True, faceted=True)
    cross_ref_map_number = indexes.CharField(model_attr='cross_ref_map_number', null=True, faceted=True)
    hash = indexes.CharField(model_attr='hash', null=True, faceted=True)

    def get_model(self):
        return models.Survey


class TitleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    control_number = indexes.CharField(model_attr='control_number', faceted=True)

    def get_model(self):
        return models.Title
