from django.db import models


class Grade(models.Model):
    name = models.CharField(max_length=50)  
    description = models.TextField(blank=True, null=True)  # Optional: Description about the grade

    def __str__(self):
        return self.name



class Subject(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='subjects') 
    name = models.CharField(max_length=100) 
    description = models.TextField(blank=True, null=True)  

    def __str__(self):
        return f"{self.name} ({self.grade.name})"  
    
class Chapter(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='chapters')

    def __str__(self):
        return f"{self.name} ({self.subject.name})"

class shortQuestion(models.Model):

    
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='shortquestions')  
    question_text = models.TextField()

    def __str__(self):
        return f" {self.question_text[:50]}..." 

class LongQuestion(models.Model):

    
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='longquestions')  
    question_text = models.TextField()

    def __str__(self):
        return f" {self.question_text[:50]}..." 



class MCQ(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='mcqs')
    question = models.CharField(max_length=500)
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_option = models.CharField(max_length=1) 

    def __str__(self) -> str:
        return self.question