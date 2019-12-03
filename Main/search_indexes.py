from haystack import indexes

from .models import Note


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # title = indexes.CharField(model_attr='title')
    # summary = indexes.CharField(model_attr='summary')
    # subject_name = indexes.CharField(model_attr='subject__name')


    def get_model(self):  # 重载get_model方法，必须要有！
        return Note


    def index_queryset(self, using=None):
        return self.get_model().objects.all()

