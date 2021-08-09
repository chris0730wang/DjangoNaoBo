from import_export import resources
from .models import CustomizeVocabulary, CustomizeStudentList, CustomizeQuestionAndAnswer, CustomizeClassInfo, CustomizeDiscussion, CustomizeExerciseInfo, CustomizeReading

class CustomizeVocabularyResource(resources.ModelResource):
    class Meta:
        model = CustomizeVocabulary

class CustomizeStudentListResource(resources.ModelResource):
    class Meta:
        model = CustomizeStudentList

class CustomizeQuestionAndAnswerResource(resources.ModelResource):
    class Meta:
        model = CustomizeQuestionAndAnswer

class CustomizeClassInfoResource(resources.ModelResource):
    class Meta:
        model = CustomizeClassInfo

class CustomizeDiscussionResource(resources.ModelResource):
    class Meta:
        model = CustomizeDiscussion

class CustomizeExerciseResource(resources.ModelResource):
    class Meta:
        model = CustomizeExerciseInfo

class CustomizeReadingResource(resources.ModelResource):
    class Meta:
        model = CustomizeReading