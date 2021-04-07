from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    STATUS_CHOICESS = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )
    email = models.EmailField(
        blank=False,
        unique=True,
        max_length=254,
        verbose_name='email address'
    )
    password = models.CharField(
        blank=True,
        max_length=128,
        verbose_name='password'
    )
    username = models.CharField(
        blank=True,
        null=True,
        unique=True,
        max_length=150
    )
    role = models.CharField(
        blank=True,
        max_length=10,
        choices=STATUS_CHOICESS,
        default='user'
    )
    confirme_code = models.CharField(blank=True, max_length=20)
    bio = models.TextField(max_length=500, blank=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(max_length=500)
    year = models.IntegerField(null=True)
    category = models.ForeignKey(
        Category,
        models.SET_NULL,
        null=True,
        related_name="categories"
    )
    genre = models.ManyToManyField(Genre)
    description = models.TextField(null=True)

    def rating(self):
        scores = Reviews.objects.filter(title=self).values_list("score",
                                                                flat=True)
        if len(scores) != 0:
            average = round(sum(scores)/len(scores))
            return average


class Reviews(models.Model):
    SCORE = [(i, i) for i in range(1, 11)]
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    score = models.IntegerField(choices=SCORE)
    pub_date = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    review = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
