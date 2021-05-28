from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import CustomizeVocabulary, CustomizeStudentList, CustomizeQuestionAndAnswer


@admin.register(CustomizeStudentList)
class CustomizeStudentListAdmin(ImportExportModelAdmin):
 list_display = ('classid', 'studentid', 'studentname', 'studentgroup')


@admin.register(CustomizeVocabulary)
class CustomizeCocabularyAdmin(ImportExportModelAdmin):
 list_display = ('package', 'word', 'partofspeech', 'meaning')
# Register your models here.

@admin.register(CustomizeQuestionAndAnswer)
class CustomizeQuestionAndAnswerAdmin(ImportExportModelAdmin):
 list_display = ('package', 'questionnum', 'question', 'answer', 'option1', 'option2', 'option3', 'option4')