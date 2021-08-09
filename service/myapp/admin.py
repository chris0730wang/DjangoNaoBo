from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import CustomizeVocabulary, CustomizeStudentList, CustomizeQuiz, CustomizeClassInfo, CustomizeDiscussion, CustomizeExerciseInfo, CustomizeReading


@admin.register(CustomizeStudentList)
class CustomizeStudentListAdmin(ImportExportModelAdmin):
 list_display = ('classid', 'studentid', 'studentname', 'studentgroup')

@admin.register(CustomizeVocabulary)
class CustomizeVocabularyAdmin(ImportExportModelAdmin):
 list_display = ('package', 'word', 'partofspeech', 'meaning')

@admin.register(CustomizeQuiz)
class CustomizeQuizAdmin(ImportExportModelAdmin):
 list_display = ('package', 'questionnum', 'question', 'answer', 'option1', 'option2', 'option3', 'option4')

@admin.register(CustomizeClassInfo)
class CustomizeClassInfoAdmin(ImportExportModelAdmin):
 list_display = ('classname', 'stepbystep', 'stepbystepdetail')

@admin.register(CustomizeDiscussion)
class CustomizeDiscussionAdmin(ImportExportModelAdmin):
 list_display = ('issuename', 'issue', 'sampleanswer', 'time')

@admin.register(CustomizeExerciseInfo)
class CustomizeExerciseAdmin(ImportExportModelAdmin):
 list_display = ('exercisename', 'category', 'musicdirectory')

@admin.register(CustomizeReading)
class CustomizeExerciseAdmin(ImportExportModelAdmin):
 list_display = ('lesson', 'part', 'readinginaudio', 'readingexplanationaudio')