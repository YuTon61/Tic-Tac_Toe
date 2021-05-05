from django.db import models

from accounts.models import Author
from django.contrib.auth.models import User



class Category(models.Model):
    name = models.CharField(max_length = 255, unique = True)



class Post(models.Model):
    article  = "AR"
    news     = "NE"
    CONTENTS = [
        (article, "Article"),
        (news,    "News")
    ]
    
    author     = models.ForeignKey(Author,   on_delete = models.CASCADE)
    categories = models.ManyToManyField(Category, through = 'PostCategory')

    content    = models.CharField(max_length = 2, choices = CONTENTS, default = news)
    datetime   = models.DateTimeField(auto_now_add = True)
    title      = models.CharField(max_length = 255)
    text       = models.TextField()
    rating     = models.IntegerField(default = 0)

    def like(self):
        self.rating += 1
        self.save()
        #
        Author.objects.get(id = self.author.id).update_rating(3)

    def dislike(self):
        self.rating -= 1
        self.save()
        #
        Author.objects.get(id = self.author.id).update_rating(-3)

    def preview(self):
        return self.text[:125] + "..."



class Comment(models.Model):
    user     = models.ForeignKey(User, on_delete = models.CASCADE)
    post     = models.ForeignKey(Post, on_delete = models.CASCADE)

    text     = models.TextField()
    datetime = models.DateTimeField(auto_now_add = True)
    rating   = models.IntegerField(default = 0)

    def like(self):
        self.rating += 1
        self.save()
        # if you like author's comment
        if Author.objects.filter(user_id = self.user.id).exists():
            Author.objects.get(id = self.user.id).update_rating(1)
        # you like commemt under author's post
        Author.objects.get(id = self.post.author.id).update_rating(1)

    def dislike(self):
        self.rating -= 1
        self.save()
        # if you dislike author's comment
        if Author.objects.filter(user_id = self.user.id).exists():
            Author.objects.get(id = self.user.id).update_rating(-1)
        # you dislike commemt under author's post
        Author.objects.get(id = self.post.author.id).update_rating(-1)



class PostCategory(models.Model):
    post     = models.ForeignKey(Post,     on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

