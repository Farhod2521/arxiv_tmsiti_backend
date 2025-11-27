from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

# -------------------------
#  USER MANAGER
# -------------------------
class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Phone number is required")

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(phone, password, **extra_fields)


# -------------------------
#  ROLE
# -------------------------
class Role(models.Model):
    name = models.CharField(max_length=150, verbose_name="Rol nomi")

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Rollar"

    def __str__(self):
        return self.name


# -------------------------
#  USER
# -------------------------


class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=255, verbose_name="To‘liq ism")
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, verbose_name="Foydalanuvchi roli")
    phone = models.CharField(max_length=30, unique=True, verbose_name="Telefon raqam")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

    def __str__(self):
        return f"{self.full_name} ({self.phone})"


# -------------------------
#  BIG CATEGORY
# -------------------------
class BigCategory(models.Model):
    title = models.CharField(max_length=255, verbose_name="Bo‘lim nomi")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="big_categories",
                             verbose_name="Rolga tegishli")

    class Meta:
        verbose_name = "Katta bo‘lim"
        verbose_name_plural = "Katta bo‘limlar"

    def __str__(self):
        return self.title


# -------------------------
#  CATEGORY
# -------------------------
class Category(models.Model):
    big_category = models.ForeignKey(BigCategory, on_delete=models.CASCADE, related_name="categories",
                                     verbose_name="Katta bo‘lim")
    ichki_raqam = models.CharField(max_length=500, verbose_name="Indeks raqami")
    tartib_raqami = models.CharField(max_length=500, verbose_name="Yigʻmajild (jild, qism) sarlavhasi")
    izoh = models.TextField(blank=True, null=True, verbose_name="Izoh")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return f"{self.big_category} → {self.ichki_raqam}"


# -------------------------
#  DOCUMENT
# -------------------------
class Doc(models.Model):
    title = models.CharField(max_length=255, verbose_name="Hujjat nomi", blank=True , null=True)
    file = models.FileField(upload_to="docs/", verbose_name="PDF fayl")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="docs", verbose_name="Kategoriya")

    class Meta:
        verbose_name = "Hujjat"
        verbose_name_plural = "Hujjatlar"

    def __str__(self):
        return self.title
