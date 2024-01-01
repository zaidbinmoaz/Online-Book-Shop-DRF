from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from .managers import CustomManager


class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=50)
    is_author = models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = CustomManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "is_author"]

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    cover_img = models.ImageField(
        upload_to="images/", default="images/img.png", blank=True, null=True
    )
    publisher = models.CharField(max_length=200, blank=True, null=True)
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="books",
        blank=True,
        null=True,
    )
    in_stock = models.BooleanField(default=True, blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    is_favourite = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_favourite:
            Favourite.objects.get_or_create(user=self.author, book=self)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("-created",)


class Favourite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.book.title
