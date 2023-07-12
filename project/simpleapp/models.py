from django.db import models
from django.contrib.auth.models import User
import re
from django.urls import reverse


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name.title()


class Post(models.Model):

    #author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(to='Category',on_delete=models.CASCADE, related_name='postlist')
    dateCreation = models.DateTimeField(auto_now = True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128, unique=True)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def censor_text(self, text):
        bad_words = ['хуй', 'пизда', 'пидор','пидорас',]  # список запрещенных слов
        pattern = re.compile(r'\b(%s)\b' % '|'.join(map(re.escape, bad_words)), flags=re.IGNORECASE)
        censored_text = pattern.sub('*', text)
        return censored_text

    def save(self, *args, **kwargs):
        self.title = self.censor_text(self.title)
        self.text = self.censor_text(self.text)
        print(f"Censored title: {self.title}")  # отладочная информация
        print(f"Censored text: {self.text}")  # отладочная информация
        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.title.title()}: {self.text[:20]}, {self.category}, {self.dateCreation}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])



class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
