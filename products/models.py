from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    @property
    def count_reviews(self):
        return self.review.all().count()

    @property
    def all_reviews(self):
        reviews = Review.objects.filter(product=self)
        return [{'id': i.id, 'text': i.text} for i in reviews]

    @property
    def rating(self):
        reviews = Review.objects.filter(product=self)
        sum_ = 0
        for i in reviews:
            sum_ += int(i.stars)
        try:
            return sum_/reviews.count()
        except:
            return 0

STARS = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
)

class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True,
                                related_name='review')
    stars = models.IntegerField(choices=STARS, null=True, max_length=5)

    def __str__(self):
        return self.text
