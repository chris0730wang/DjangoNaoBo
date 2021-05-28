from import_export import resources
from .models import CustomizeVocabulary, CustomizeStudentList, CustomizeQuestionAndAnswer

class CustomizeVocabularyResource(resources.ModelResource):
    class Meta:
        model = CustomizeVocabulary

class CustomizeStudentListResource(resources.ModelResource):
    class Meta:
        model = CustomizeStudentList

class CustomizeQuestionAndAnswerResource(resources.ModelResource):
    class Meta:
        model = CustomizeQuestionAndAnswer