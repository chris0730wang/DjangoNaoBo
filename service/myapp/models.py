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

    def __str__(self):
        return self.cName

class BeforeYouRead(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    unit = models.CharField(max_length=2, null=False)  # 第幾課
    number = models.IntegerField(null=False)  # 第幾題
    question = models.CharField(max_length=100, null=False)  # 問題
    option1 = models.CharField(max_length=100, null=False)  # 選項一
    numofchoose1 = models.IntegerField(null=False)  # 選擇選項一的人數
    option2 = models.CharField(max_length=100, null=False)  # 選項二
    numofchoose2 = models.IntegerField(null=False)  # 選擇選項二的人數
    option3 = models.CharField(max_length=100, null=False)  # 選項三
    numofchoose3 = models.IntegerField(null=False)  # 選擇選項三的人數
    option4 = models.CharField(max_length=100, null=False)  # 選項四
    numofchoose4 = models.IntegerField(null=False)  # 選擇選項四的人數
    option5 = models.CharField(max_length=100, null=False)  # 選項五
    numofchoose5 = models.IntegerField(null=False)  # 選擇選項五的人數
    totalchoose = models.IntegerField(null=False)  # 總共進行選擇的人數

    def __str__(self):
        return self.question

class BeforeYouReadAns(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    unit = models.CharField(max_length=2)  # 第幾課
    number = models.IntegerField(null=False)  # 第幾題
    numofchoose1 = models.IntegerField(null=False)  # 選擇選項一的人數
    numofchoose2 = models.IntegerField(null=False)  # 選擇選項二的人數
    numofchoose3 = models.IntegerField(null=False)  # 選擇選項三的人數
    numofchoose4 = models.IntegerField(null=False)  # 選擇選項四的人數
    numofchoose5 = models.IntegerField(null=False)  # 選擇選項五的人數
    totalchoose = models.IntegerField(null=False)  # 總共進行選擇的人數

    def __str__(self):
        return self.totalchoose

class VocabularyPreview(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    unit = models.IntegerField(null=False)  # 第幾課
    lesson = models.IntegerField(null=False)  # 第幾章(1/2)
    questionnum = models.CharField(max_length=100, null=False)  # 題號
    question = models.CharField(max_length=100, null=False)  # 單字
    option1 = models.CharField(max_length=100, null=False)  # 選項一
    option2 = models.CharField(max_length=100, null=False)  # 選項二
    option3 = models.CharField(max_length=100, null=False)  # 選項三
    option4 = models.CharField(max_length=100, null=False)  # 選項四


    def __str__(self):
        learnword = "Unit " + str(self.unit) + "lesson"
        return learnword

class VocabularyPreviewAns(models.Model):
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
