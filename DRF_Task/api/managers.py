from django.contrib.auth.models import BaseUserManager


class CustomManager(BaseUserManager):
    def create_user(
        self,
        email,
        name,
        is_author,
        password=None,
        password2=None,
    ):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            is_author=is_author,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, is_author, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            is_author=is_author,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
