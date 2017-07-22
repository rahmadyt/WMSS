from django.db import models

# Create your models here.

class Crawl(models.Model):
    name = models.CharField(max_length=100)
    content = models.CharField(max_length=140)
    c_at = models.DateField()
    #Retweet = models.CharField(max_length=100)
    #hashtag = models.CharField(max_length=100)
    
    def _str_(self):
        return  self.content, self.name

class TwitterCrawl(models.Model):
    name = models.CharField(max_length=100)
    tweet = models.CharField(max_length=140)
    date = models.DateField()
    Retweet_user = models.CharField(max_length=100, null=True)
    Retweet_post = models.CharField(max_length=140, null=True)
    hashtag = models.CharField(max_length=100, null = True)
    
    def _str_(self):
        return  self.tweet, self.name, self.Retweet_post, self.Retweet_user, self.hashtag
    

class FacebookCrawl(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=63206)
    like = models.CharField(max_length=10, null=True)
    comment = models.CharField(max_length=10, null=True)
    share = models.CharField(max_length=10, null = True)
    
    def _str_(self):
        return   self.name, self.Retweet_post, self.Retweet_user, self.hashtag