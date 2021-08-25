from django.db import models
from django.utils import timezone

class Pay(models.Model):
    id = models.AutoField(primary_key=True)
    item_spend = models.CharField(null=False, max_length=50)
    money = models.FloatField(null=False)
    year = models.IntegerField(null=False)
    month = models.IntegerField(null=False)
    day = models.IntegerField(null=False)
    isPri = models.BooleanField(null=False)
    data_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        temp = "id is : " + str(self.id) + "--item is : " + str(self.item_spend)
        return temp

# 學生名單 and 點名
class studentcheck(models.Model):
    id = models.AutoField(primary_key=True)
    cId = models.CharField(max_length=10, null=False)  # 學號
    cName = models.CharField(max_length=10, null=False)  # 姓名
    cGroup = models.IntegerField(null=True)  # 組別
    FirstweekCheck = models.CharField(max_length=10, null=False)  # 第一週簽到
    SecondweekCheck = models.CharField(max_length=10, null=False)  # 第二週簽到
    ThirdweekCheck = models.CharField(max_length=10, null=False)  # 第三週簽到
    ForthweekCheck = models.CharField(max_length=10, null=False)  # 第四週簽到
    point = models.IntegerField(null=True)  # 加分紀錄
    picked = models.IntegerField(null=True)  # 抽點紀錄
    vp1point = models.IntegerField(null=True)  # vocabulary preview 分數
    foc1point = models.IntegerField(null=True)  # focus on content 分數
    vr1point = models.IntegerField(null=True)  # vocabulary review 分數
    vp2point = models.IntegerField(null=True)  # vocabulary preview 分數
    foc2point = models.IntegerField(null=True)  # focus on content 分數
    vr2point = models.IntegerField(null=True)  # vocabulary review 分數
    ctchoosebeforediscuss = models.IntegerField(null=False, default=0)  # Critical Thinking 選擇正方或反方 1:正方 0:尚未選擇 -1:反方 (討論前)
    ctchooseafterdiscuss = models.IntegerField(null=False, default=0)  # Critical Thinking 選擇正方或反方 1:正方 0:尚未選擇 -1:反方 (討論後)

    def __str__(self):
        return self.cName

# Before You Read 題目、選項、答案
class BeforeYouRead(models.Model):
    id = models.AutoField(primary_key=True)
    unit = models.CharField(max_length=2, null=False)  # 第幾課
    number = models.IntegerField(null=False)  # 第幾題
    question = models.CharField(max_length=255, null=False)  # 問題
    option1 = models.CharField(max_length=100, null=False)  # 選項一
    option2 = models.CharField(max_length=100, null=False)  # 選項二
    option3 = models.CharField(max_length=100, null=False)  # 選項三
    option4 = models.CharField(max_length=100, null=False)  # 選項四
    option5 = models.CharField(max_length=100, null=False)  # 選項五
    numof1 = models.IntegerField(null=True)  # 選擇一的人數
    numof2 = models.IntegerField(null=True)  # 選擇二的人數
    numof3 = models.IntegerField(null=True)  # 選擇三的人數
    numof4 = models.IntegerField(null=True)  # 選擇四的人數
    numof5 = models.IntegerField(null=True)  # 選擇五的人數

    def __str__(self):
        return self.question

# Unit 10 Before You Read GOOGLE 表單回應
class U10BeforeYouReadAns(models.Model):
    id = models.AutoField(primary_key=True)
    unit = models.CharField(max_length=2)  # 第幾課
    cId = models.CharField(max_length=10, null=False, default='NULL')  # 學號
    q1answer = models.CharField(max_length=255, null=False)  # 第一題答案
    q2answer = models.CharField(max_length=255, null=False)  # 第二題答案
    q3answer = models.CharField(max_length=255, null=False)  # 第三題答案
    q4answer = models.CharField(max_length=255, null=False)  # 第四題答案
    q5answer = models.CharField(max_length=255, null=False)  # 第五題答案
    timezone = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.totalchoose

# Vocabulary Preview 題目、選項、答案
class VocabularyPreview(models.Model):
    id = models.AutoField(primary_key=True)
    unit = models.IntegerField(null=False)  # 第幾課
    reading = models.IntegerField(null=False)  # 第幾章(1/2)
    questionnum = models.IntegerField(null=False)  # 題號
    question = models.CharField(max_length=100, null=False)  # 單字
    option1 = models.CharField(max_length=100, null=False)  # 選項一
    numof1 = models.IntegerField(null=True)  # 選擇一的人數
    option2 = models.CharField(max_length=100, null=False)  # 選項二
    numof2 = models.IntegerField(null=True)  # 選擇二的人數
    option3 = models.CharField(max_length=100, null=False)  # 選項三
    numof3 = models.IntegerField(null=True)  # 選擇三的人數
    option4 = models.CharField(max_length=100, null=True)  # 選項四
    numof4 = models.IntegerField(null=True)  # 選擇四的人數
    correctans = models.CharField(max_length=100, null=False)  # 正確答案
    falsepercent = models.IntegerField(null=True)  # 錯誤率


    def __str__(self):
        learnword = "Unit " + str(self.unit) + "lesson"
        return learnword

# Unit 10 Reading 1 GOOGLE 表單回應
class U10R1VocabularyPreviewAns(models.Model):
    id = models.AutoField(primary_key=True)
    unit = models.IntegerField(null=False)  # 第幾課
    reading = models.IntegerField(null=False)  # 第幾章(1/2)
    cId = models.CharField(max_length=10, null=False)  # 學號
    q1answer = models.CharField(max_length=100, null=False)  # 第一題
    q2answer = models.CharField(max_length=100, null=False)  # 第二題
    q3answer = models.CharField(max_length=100, null=False)  # 第三題
    q4answer = models.CharField(max_length=100, null=False)  # 第四題
    q5answer = models.CharField(max_length=100, null=False)  # 第五題
    q6answer = models.CharField(max_length=100, null=False)  # 第六題
    q7answer = models.CharField(max_length=100, null=False)  # 第七題
    q8answer = models.CharField(max_length=100, null=False)  # 第八題
    point = models.FloatField(null=False)  # 分數
    timezone = models.CharField(max_length=100, null=False)


    def __str__(self):
        return self.cId

# Unit 10 Reading 2 GOOGLE 表單回應
class U10R2VocabularyPreviewAns(models.Model):
    id = models.AutoField(primary_key=True)
    unit = models.IntegerField(null=False)  # 第幾課
    reading = models.IntegerField(null=False)  # 第幾章(1/2)
    cId = models.CharField(max_length=10, null=False)  # 學號
    q1answer = models.CharField(max_length=100, null=False)  # 第一題
    q2answer = models.CharField(max_length=100, null=False)  # 第二題
    q3answer = models.CharField(max_length=100, null=False)  # 第三題
    q4answer = models.CharField(max_length=100, null=False)  # 第四題
    q5answer = models.CharField(max_length=100, null=False)  # 第五題
    q6answer = models.CharField(max_length=100, null=False)  # 第六題
    q7answer = models.CharField(max_length=100, null=False)  # 第七題
    q8answer = models.CharField(max_length=100, null=False)  # 第八題
    point = models.FloatField(null=False)  # 分數
    timezone = models.CharField(max_length=100, null=False)


    def __str__(self):
        return self.cId

# Focus on Content 題目、選項、答案
class FocusOnContent(models.Model):
    id = models.AutoField(primary_key=True)
    unit = models.IntegerField(null=False)  # 第幾課
    reading = models.IntegerField(null=False, default=None)  # 第幾章(1/2)
    questionnum = models.IntegerField(null=False)  # 題號
    question = models.CharField(max_length=255, null=False)  # 問題
    option1 = models.CharField(max_length=100, null=False)  # 選項一
    option2 = models.CharField(max_length=100, null=True)  # 選項二
    option3 = models.CharField(max_length=100, null=True)  # 選項三
    option4 = models.CharField(max_length=100, null=True)  # 選項四
    option5 = models.CharField(max_length=100, default=None, null=True)  # 選項五
    correctans = models.CharField(max_length=255, default=None, null=False)  # 正確答案
    numof1 = models.IntegerField(null=True)  # 選擇一的人數
    numof2 = models.IntegerField(null=True)  # 選擇二的人數
    numof3 = models.IntegerField(null=True)  # 選擇三的人數
    numof4 = models.IntegerField(null=True)  # 選擇四的人數
    numof5 = models.IntegerField(null=True)  # 選擇五的人數
    falsepercent = models.IntegerField(null=True)  # 錯誤率


    def __str__(self):
        return self.question

# Unit 10 Reading 1 Focus on Content GOOGLE 表單回應
class U10R1FocusonContentAns(models.Model):
    id = models.AutoField(primary_key=True)
    cId = models.CharField(max_length=10, null=False)
    q1answer = models.CharField(max_length=255, null=False)
    q2answer = models.CharField(max_length=255, null=False)
    q3answer = models.CharField(max_length=255, null=False)
    q4answer = models.CharField(max_length=255, null=False)
    q5answer = models.CharField(max_length=255, null=False)
    q6answer = models.CharField(max_length=255, null=False)
    q7answer = models.CharField(max_length=255, null=False)
    point = models.IntegerField(null=True)
    timezone = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.cId

# Unit 10 Reading 2 Focus on Content GOOGLE 表單回應
class U10R2FocusonContentAns(models.Model):
    id = models.AutoField(primary_key=True)
    cId = models.CharField(max_length=10, null=False)
    q1answer = models.CharField(max_length=255, null=False)
    q2answer = models.CharField(max_length=255, null=False)
    q3answer = models.CharField(max_length=255, null=False)
    q4answer = models.CharField(max_length=255, null=False)
    q5answer = models.CharField(max_length=255, null=False)
    q6answer = models.CharField(max_length=255, null=False)
    q7answer = models.CharField(max_length=255, null=False)
    q8answer = models.CharField(max_length=255, null=False)
    q9answer = models.CharField(max_length=255, null=False)
    q10answer = models.CharField(max_length=255, null=False)
    point = models.IntegerField(null=True)
    timezone = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.cId

# Vocabulary Review 題目、選項、答案
class VocabularyReview(models.Model):
    id = models.AutoField(primary_key=True)
    unit = models.IntegerField(null=False)  # 第幾課
    reading = models.IntegerField(null=False)  # 第幾章(1/2)
    questionnum = models.IntegerField(null=False)  # 題號
    question = models.CharField(max_length=255, null=False)  # 單字
    option1 = models.CharField(max_length=100, null=False)  # 選項一
    numof1 = models.IntegerField(null=True)  # 選擇一的人數
    option2 = models.CharField(max_length=100, null=False)  # 選項二
    numof2 = models.IntegerField(null=True)  # 選擇二的人數
    option3 = models.CharField(max_length=100, null=False)  # 選項三
    numof3 = models.IntegerField(null=True)  # 選擇三的人數
    option4 = models.CharField(max_length=100, null=True)  # 選項四
    numof4 = models.IntegerField(null=True)  # 選擇四的人數
    correctans = models.CharField(max_length=100, null=False)  # 正確答案
    falsepercent = models.IntegerField(null=True)  # 錯誤率


    def __str__(self):
        learnword = "Unit " + str(self.unit) + "lesson"
        return learnword

# Unit 10 Reading 1 Vocabulary Review GOOGLE 表單回應
class U10R1VocabularyReviewAns(models.Model):
    id = models.AutoField(primary_key=True)
    unit = models.IntegerField(null=False)  # 第幾課
    reading = models.IntegerField(null=False)  # 第幾章(1/2)
    cId = models.CharField(max_length=10, null=False)  # 學號
    q1answer = models.CharField(max_length=100, null=False)  # 第一題
    q2answer = models.CharField(max_length=100, null=False)  # 第二題
    q3answer = models.CharField(max_length=100, null=False)  # 第三題
    q4answer = models.CharField(max_length=100, null=False)  # 第四題
    q5answer = models.CharField(max_length=100, null=False)  # 第五題
    q6answer = models.CharField(max_length=100, null=False)  # 第六題
    q7answer = models.CharField(max_length=100, null=False)  # 第七題
    q8answer = models.CharField(max_length=100, null=False)  # 第八題
    point = models.FloatField(null=False)  # 分數
    timezone = models.CharField(max_length=100, null=False)


    def __str__(self):
        return self.cId

# Unit 10 Reading 2 Vocabulary Review GOOGLE 表單回應
class U10R2VocabularyReviewAns(models.Model):
    id = models.AutoField(primary_key=True)
    unit = models.IntegerField(null=False)  # 第幾課
    reading = models.IntegerField(null=False)  # 第幾章(1/2)
    cId = models.CharField(max_length=10, null=False)  # 學號
    q1answer = models.CharField(max_length=100, null=False)  # 第一題
    q2answer = models.CharField(max_length=100, null=False)  # 第二題
    q3answer = models.CharField(max_length=100, null=False)  # 第三題
    q4answer = models.CharField(max_length=100, null=False)  # 第四題
    q5answer = models.CharField(max_length=100, null=False)  # 第五題
    q6answer = models.CharField(max_length=100, null=False)  # 第六題
    q7answer = models.CharField(max_length=100, null=False)  # 第七題
    q8answer = models.CharField(max_length=100, null=False)  # 第八題
    point = models.FloatField(null=False)  # 分數
    timezone = models.CharField(max_length=100, null=False)


    def __str__(self):
        return self.cId

# Vocabulary Detail 單字詳解
class VocabularyDetail(models.Model):
    id = models.AutoField(primary_key=True)
    unit = models.IntegerField(null=False)  # 第幾課
    reading = models.IntegerField(null=False)  # 第幾章(1/2)
    num = models.IntegerField(null=False)  # 第幾個單字
    vocabulary = models.CharField(max_length=100, null=False)  # 單字
    partsofspeech = models.CharField(max_length=100, null=False)  # 詞性
    explain = models.CharField(max_length=100, null=False)  # 英文單字解釋

    def __str__(self):
        return self.vocabulary + "/" + self.partsofspeech + "/" + self.explain

# 存取NAO的IP Address
class SetNaoIP(models.Model):
    id = models.AutoField(primary_key=True)
    IPAddress = models.CharField(max_length=100, null=False)
    timezone = models.DateTimeField(default=timezone.now())
    test = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.IPAddress


# 修改後系統

# 存取課程開始時間
class SetStartTime(models.Model):
    id = models.AutoField(primary_key=True)
    starttime = models.DateTimeField(max_length=100, null=False)
    timezone = models.DateTimeField(default=timezone.now())

# 授課教師匯入學生名單
class CustomizeStudentList(models.Model):
    id = models.AutoField(primary_key=True)
    classid = models.CharField(max_length=20, null=False)
    studentid = models.CharField(max_length=20, null=False)
    studentname = models.CharField(max_length=20, null=False)
    studentgroup = models.IntegerField(null=True)
    studentcheck = models.CharField(max_length=20, default="尚未簽到")
    studentpoint = models.IntegerField(default=0)

# 授課教師自定義單字
class CustomizeVocabulary(models.Model):
    id = models.AutoField(primary_key=True)
    package = models.CharField(max_length=100, null=True)
    word = models.CharField(max_length=100, null=False)
    partofspeech = models.CharField(max_length=20, null=True)
    meaning = models.CharField(max_length=100, null=True)

# 授課教師匯入測驗題目正確答案
class CustomizeQuiz(models.Model):
    id = models.AutoField(primary_key=True)
    package = models.CharField(max_length=100, null=False)
    questionnum = models.IntegerField(null=False)
    question = models.CharField(max_length=100, null=False)
    answer = models.CharField(max_length=100, null=False)
    option1 = models.CharField(max_length=100, null=False)
    option2 = models.CharField(max_length=100, null=False)
    option3 = models.CharField(max_length=100, null=True)
    option4 = models.CharField(max_length=100, null=True)

# 授課教師設計課程
class CustomizeClassInfo(models.Model):
    id = models.AutoField(primary_key=True)
    classname = models.CharField(max_length=100, null=False)
    stepbystep = models.CharField(max_length=100, null=True)
    stepbystepdetail = models.CharField(max_length=100, null=False)
    stepbysteptoshow = models.CharField(max_length=255, null=False, default="")
    attention = models.CharField(max_length=255, null=True)
    timezone = models.DateTimeField(default=timezone.now())

# 授課教師匯入閱讀課程
class CustomizeReading(models.Model):
    id = models.AutoField(primary_key=True)
    lesson = models.CharField(max_length=100, null=False)
    part = models.IntegerField(null=False)
    readingintext = models.CharField(max_length=255, null=True)
    readinginaudio = models.CharField(max_length=100, null=True)
    readingexplanationaudio = models.CharField(max_length=100, null=True)

# 課堂活動(帶動唱)
class CustomizeExerciseInfo(models.Model):
    id = models.AutoField(primary_key=True)
    exercisename = models.CharField(max_length=100, null=False)
    category = models.CharField(max_length=100, null=False)
    musicdirectory = models.CharField(max_length=255, null=True)

# 小組討論
class CustomizeDiscussion(models.Model):
    id = models.AutoField(primary_key=True)
    issuename = models.CharField(max_length=100, null=False, default="")
    issue = models.CharField(max_length=100, null=False)
    sampleanswer = models.CharField(max_length=255, null=True)
    time = models.IntegerField(null=False)

# class CustomizeClassInfo(models.Model):
#     id = models.AutoField(primary_key=True)
#     class_id = models.CharField(max_length=100, null=False)
#     module_sequence = models.CharField(max_length=100, null=True)
#     module_data = models.CharField(max_length=100, null=False)
#     module_list = models.CharField(max_length=255, null=False, default="")
#     attention = models.CharField(max_length=255, null=True)
#     creation_time = models.DateTimeField(default=timezone.now())
