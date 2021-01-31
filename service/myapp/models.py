from django.db import models


class Pay(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
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


class studentcheck(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    cId = models.CharField(max_length=10, null=False)  # 學號
    cName = models.CharField(max_length=10, null=False)  # 姓名
    cGroup = models.IntegerField(null=True)  # 組別
    FirstweekCheck = models.CharField(max_length=10, null=False)  # 第一週簽到
    SecondweekCheck = models.CharField(max_length=10, null=False)  # 第二週簽到
    ThirdweekCheck = models.CharField(max_length=10, null=False)  # 第三週簽到
    ForthweekCheck = models.CharField(max_length=10, null=False)  # 第四週簽到
    point = models.IntegerField(null=True)  # 加分紀錄
    picked = models.IntegerField(null=True)  # 抽點紀錄

    def __str__(self):
        return self.cName

class BeforeYouRead(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
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

class U5BeforeYouReadAns(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    unit = models.CharField(max_length=2)  # 第幾課
    cId = models.CharField(max_length=10, null=False, default='NULL')  # 學號
    q1answer = models.CharField(max_length=255, null=False)  # 第一題答案
    q2answer = models.CharField(max_length=255, null=False)  # 第二題答案
    q3answer = models.CharField(max_length=255, null=False)  # 第三題答案
    q4answer = models.CharField(max_length=255, null=False)  # 第四題答案
    q5answer = models.CharField(max_length=255, null=False)  # 第五題答案

    def __str__(self):
        return self.totalchoose

class U7BeforeYouReadAns(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    unit = models.CharField(max_length=2)  # 第幾課
    cId = models.CharField(max_length=10, null=False, default='NULL')  # 學號
    q1answer = models.CharField(max_length=255, null=False)  # 第一題答案
    q2answer = models.CharField(max_length=255, null=False)  # 第二題答案
    q3answer = models.CharField(max_length=255, null=False)  # 第三題答案
    q4answer = models.CharField(max_length=255, null=False)  # 第四題答案
    q5answer = models.CharField(max_length=255, null=False)  # 第五題答案

    def __str__(self):
        return self.totalchoose

class VocabularyPreview(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
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

class VocabularyPreviewAns(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
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


    def __str__(self):
        return self.totalchoose

class FocusOnContent(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    unit = models.IntegerField(null=False)  # 第幾課
    lesson = models.IntegerField(null=False, default=None)  # 第幾章(1/2)
    questionnum = models.CharField(max_length=100, default=None, null=False)  # 題號
    question = models.CharField(max_length=100, null=False)  # 問題
    option1 = models.CharField(max_length=100, null=False)  # 選項一
    option2 = models.CharField(max_length=100, null=False)  # 選項二
    option3 = models.CharField(max_length=100, null=False)  # 選項三
    option4 = models.CharField(max_length=100, null=False)  # 選項四

    def __str__(self):
        return self.question

class FocusOnContentAns(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    unit = models.IntegerField(null=False)  # 第幾課
    lesson = models.IntegerField(null=False)  # 第幾章(1/2)
    questionnum = models.CharField(max_length=100, default=None, null=False)  # 題號
    correctoption = models.CharField(max_length=100, null=False)  # 正確選項
    chooseoption1 = models.IntegerField(null=False)  # 選擇選項一的人數
    chooseoption2 = models.IntegerField(null=False)  # 選擇選項二的人數
    chooseoption3 = models.IntegerField(null=False)  # 選擇選項三的人數
    chooseoption4 = models.IntegerField(null=False)  # 選擇選項四的人數
    totalchoose = models.IntegerField(null=False)  # 總共答題人數

    def __str__(self):
        return self.questionnum

class VocabularyReview(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    unit = models.IntegerField(null=False)  # 第幾課
    lesson = models.IntegerField(null=False)  # 第幾章(1/2)
    questionnum = models.CharField(max_length=100, null=False)  # 題號
    question = models.CharField(max_length=100, null=False)  # 單字
    option1 = models.CharField(max_length=100, null=False)  # 選項一
    option2 = models.CharField(max_length=100, null=False)  # 選項二
    option3 = models.CharField(max_length=100, null=False)  # 選項三
    option4 = models.CharField(max_length=100, null=False)  # 選項四
    correctans = models.CharField(max_length=100, null=False)  # 正確答案

    def __str__(self):
        learnword = "Unit " + str(self.unit) + "lesson"
        return learnword

class VocabularyReviewAns(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    unit = models.IntegerField(null=False)  # 第幾課
    lesson = models.IntegerField(null=False)  # 第幾章(1/2)
    questionnum = models.CharField(max_length=100, null=False)  # 題號
    correctoption = models.CharField(max_length=100, null=False)  # 正確選項
    chooseoption1 = models.IntegerField(null=False)  # 選擇選項一的人數
    chooseoption2 = models.IntegerField(null=False)  # 選擇選項二的人數
    chooseoption3 = models.IntegerField(null=False)  # 選擇選項三的人數
    chooseoption4 = models.IntegerField(null=False)  # 選擇選項四的人數
    totalchoose = models.IntegerField(null=False)  # 總共答題人數

    def __str__(self):
        learnword = "Unit " + str(self.unit) + "lesson"
        return learnword


# Create your models here.
