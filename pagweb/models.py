from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from .helperStorage import (
    event_image_path,
    event_gallery_path,
    product_image_path,
    church_image_path,
    staff_image_path
)

class Account(models.Model):
    ROLE_CHOICES = (
        (1, 'Admin'),
        (2, 'Staff'),
        (3, 'Anggota'),
    )

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='account'
    )

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        null=True,
        blank=True
    )

    role_id = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES,
        default=3
    )

    is_default_password = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'T_Account'
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return f"{self.user.username} - {self.get_role_id_display()}"


# ==========================================================
# HELPERS
# ==========================================================

def _unique_slug(model_cls, value: str, slug_field: str = "slug", instance_pk=None) -> str:
    """
    Generate unique slug for model_cls based on `value`.
    - model_cls: Django model class
    - value: text source (name/title)
    - slug_field: usually 'slug'
    - instance_pk: exclude current instance pk (for updates)
    """
    base = slugify(value) or "item"
    slug = base
    i = 1

    lookup = {slug_field: slug}
    qs = model_cls.objects.filter(**lookup)
    if instance_pk is not None:
        qs = qs.exclude(pk=instance_pk)

    while qs.exists():
        i += 1
        slug = f"{base}-{i}"
        lookup = {slug_field: slug}
        qs = model_cls.objects.filter(**lookup)
        if instance_pk is not None:
            qs = qs.exclude(pk=instance_pk)

    return slug



class TM_EventCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'TM_EventCategory'
        verbose_name = 'Event Category'
        verbose_name_plural = 'Event Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unique_slug(TM_EventCategory, self.name, instance_pk=self.pk)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class T_Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    description = models.TextField()

    date = models.DateField(help_text="Tanggal event")
    time = models.CharField(max_length=50, blank=True, help_text="Contoh: 19:00 - 21:00 WIB")

    location = models.CharField(max_length=255)
    pic_contact = models.CharField(max_length=50, blank=True, verbose_name="Contact Person (WA)")

    registration_link = models.URLField(blank=True, null=True)
    main_image = models.ImageField(upload_to=event_image_path, blank=True, null=True)

    categories = models.ManyToManyField(TM_EventCategory, related_name='events', blank=True)

    is_closed = models.BooleanField(default=False, help_text="Centang jika pendaftaran ditutup manual")
    is_featured = models.BooleanField(default=False, help_text="Tampilkan sebagai unggulan")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'T_Event'
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['date']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['slug']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['is_closed']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unique_slug(T_Event, self.title, instance_pk=self.pk)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class T_EventMedia(models.Model):
    event = models.ForeignKey(T_Event, on_delete=models.CASCADE, related_name="media")
    image = models.ImageField(upload_to=event_gallery_path, blank=False, null=False)
    order = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "T_EventMedia"
        verbose_name = "Event Media"
        verbose_name_plural = "Event Media"
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.event.title} - media #{self.id}"

class TM_ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        db_table = 'TM_ProductCategory'
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unique_slug(TM_ProductCategory, self.name, instance_pk=self.pk)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class TM_ProductStatus(models.Model):
    """Status seperti 'baru', 'populer', 'gratis' (bisa multiple)"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=70, unique=True, blank=True)

    class Meta:
        db_table = 'TM_ProductStatus'
        verbose_name = 'Product Status'
        verbose_name_plural = 'Product Statuses'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unique_slug(TM_ProductStatus, self.name, instance_pk=self.pk)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class T_Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    description = models.TextField()
    main_image = models.ImageField(upload_to=product_image_path, blank=True, null=True)

    categories = models.ManyToManyField(TM_ProductCategory, blank=True, related_name='products')
    statuses = models.ManyToManyField(
        TM_ProductStatus,
        blank=True,
        related_name='products',
        help_text="Bisa pilih lebih dari satu"
    )

    duration = models.CharField(max_length=100, blank=True, help_text="Misal '1-2 minggu'")
    price = models.CharField(max_length=100, help_text="Misal 'Start from Rp 300.000'")
    is_open = models.BooleanField(default=True, help_text="Masih tersedia?")
    system = models.CharField(max_length=100, blank=True, help_text="Misal 'Pre-order via WA'")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'T_Product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_open']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unique_slug(T_Product, self.name, instance_pk=self.pk)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class T_ProductFeature(models.Model):
    """Fitur unggulan per produk (poin-poin)"""
    product = models.ForeignKey(T_Product, on_delete=models.CASCADE, related_name='features')
    description = models.CharField(max_length=200)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'T_ProductFeature'
        verbose_name = 'Product Feature'
        verbose_name_plural = 'Product Features'
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.product.name}: {self.description[:30]}"


class T_Church(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    address = models.TextField()
    map_link = models.URLField(blank=True, help_text="Link Google Maps atau Waze")

    contact_pdt = models.CharField(max_length=100, blank=True, help_text="Kontak Pendeta")
    contact_ketua = models.CharField(max_length=100, blank=True, help_text="Kontak Ketua Jemaat")
    other_contact = models.TextField(blank=True, help_text="Kontak lain jika ada")

    main_image = models.ImageField(upload_to=church_image_path, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'T_Church'
        verbose_name = 'Church'
        verbose_name_plural = 'Churches'
        indexes = [models.Index(fields=['slug'])]
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unique_slug(T_Church, self.name, instance_pk=self.pk)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class T_ChurchService(models.Model):
    """Jadwal ibadah (bisa lebih dari satu per gereja)"""
    church = models.ForeignKey(T_Church, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=100, help_text="Nama ibadah, misal 'Ibadah Raya'")
    day = models.CharField(max_length=50, help_text="Hari, misal 'Sabtu' atau 'Jumat Malam'")
    time = models.CharField(max_length=100, help_text="Waktu, misal '08:00 - 10:00'")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'T_ChurchService'
        verbose_name = 'Church Service'
        verbose_name_plural = 'Church Services'
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.church.name} - {self.name} ({self.day})"


class T_ContactRequest(models.Model):
    REQUEST_TYPES = (
        ('prayer', 'Prayer Request'),
        ('general', 'Pertanyaan Umum'),
        ('event', 'Informasi Event'),
        ('product', 'Product dan Layanan'),
        ('cooperation', 'Kerja Sama'),
        ('visit', 'Kunjungan'),
        ('other', 'Lainnya'),
    )
    STATUS_CHOICES = (
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    )

    name = models.CharField(max_length=100)
    wa_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    request_type = models.CharField(max_length=20, choices=REQUEST_TYPES)
    details = models.TextField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    admin_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'T_ContactRequest'
        verbose_name = 'Contact Request'
        verbose_name_plural = 'Contact Requests'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['request_type']),
        ]

    def __str__(self):
        return f"{self.name} - {self.get_request_type_display()}"


class TM_Position(models.Model):
    """Jabatan (Sponsor, Ketua, Bendahara, dll)"""
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'TM_Position'
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'
        ordering = ['name']

    def __str__(self):
        return self.name


class TM_Division(models.Model):
    """Devisi (Officer, SDM, Acara, dll)"""
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'TM_Division'
        verbose_name = 'Division'
        verbose_name_plural = 'Divisions'
        ordering = ['name']

    def __str__(self):
        return self.name


class T_Staff(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to=staff_image_path, blank=True, null=True)

    position = models.ForeignKey(
        TM_Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff'
    )
    division = models.ForeignKey(
        TM_Division,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff'
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'T_Staff'
        verbose_name = 'Staff'
        verbose_name_plural = 'Staff'
        ordering = ['division__name', 'position__name', 'name']
        indexes = [
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.name