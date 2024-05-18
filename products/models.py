from django.db import models
from users.models import Users
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class CategoryBooks(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=188)

    class Meta:
        db_table = 'language'

    def __str__(self):
        return self.name


class Books(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    category = models.ForeignKey(CategoryBooks, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='book/', default='default_img/download.jpg')
    page = models.IntegerField()
    book_lang = models.ForeignKey(Language, on_delete=models.DO_NOTHING)

    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'books'

    def __str__(self):
        return self.title


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'author'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class BookAuthor(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        db_table = 'book_author'

    def __str__(self):
        return f"{self.book.title} - {self.author.first_name} {self.author.last_name}"


class Review(models.Model):
    comment = models.CharField(max_length=300)
    star_given = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    class Meta:
        db_table = 'review'

    def __str__(self):
        return f"{self.star_given} - {self.book.title} - {self.user.username}"





































