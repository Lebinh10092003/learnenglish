from django.db import models
from django.contrib.auth.models import User


class Vocabulary(models.Model):
    word = models.TextField()
    meaning = models.JSONField()  # Lưu trữ dạng JSON
    description = models.TextField()  # Sử dụng TextField thay vì CharField
    detail_description = models.JSONField()  # Lưu trữ dạng JSON
    phonetic = models.TextField()
    example = models.JSONField()  # Lưu trữ dạng JSON
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.word


class Topic(models.Model):
    vn_name = models.TextField()
    name = models.TextField()
    description = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class VocabularyTopic(models.Model):
    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.vocabulary.word} - {self.topic.name}'
    
# Bảng để lưu mối quan hệ User và Vocabulary
class UserVocabulary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE)
    LEARNED_CHOICES = [
        ('Not Learned', 'Chưa học'),
        ('Learning', 'Đang học'),
        ('Learned', 'Đã học'),
    ]
    is_learned = models.CharField(max_length=20, choices=LEARNED_CHOICES, default='Not Learned')  
    learned_at = models.DateTimeField(null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.vocabulary.word}'
