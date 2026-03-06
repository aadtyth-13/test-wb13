from django.contrib import admin
from .models import (
    Account,
    TM_EventCategory, T_Event, T_EventMedia,
    TM_ProductCategory, TM_ProductStatus, T_Product, T_ProductFeature,
    T_Church, T_ChurchService,
    T_ContactRequest,
    TM_Position, TM_Division, T_Staff,
)



# =========================
# ACCOUNT
# =========================

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'gender',
        'role_id',
        'is_default_password',
        'created_at',
    )
    list_filter = (
        'gender',
        'role_id',
        'is_default_password',
    )
    search_fields = (
        'user__username',
        'user__email',
        'user__first_name',
        'user__last_name',
    )


# =========================
# EVENT
# =========================

@admin.register(TM_EventCategory)
class TMEventCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}


@admin.register(T_Event)
class TEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'is_featured', 'is_closed', 'created_at')
    list_filter = ('is_featured', 'is_closed', 'date', 'categories')
    search_fields = ('title', 'slug', 'location', 'description')
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ('categories',)
    date_hierarchy = 'date'
    ordering = ('date',)

@admin.register(T_EventMedia)
class TEventMediaAdmin(admin.ModelAdmin):
    """
    Kamu bisa add/read/replace/delete media di sini.
    Tidak pakai extra karena ini bukan Inline.
    """
    list_display = ("id", "event", "order", "created_at")
    list_filter = ("event",)
    search_fields = ("event__title",)
    ordering = ("event", "order", "id")

    # field mana yang muncul di form edit/add
    fields = ("event", "image", "order")

    # Biar tidak bisa diubah manual (optional)
    readonly_fields = ("created_at", "updated_at")


# =========================
# PRODUCT
# =========================

@admin.register(TM_ProductCategory)
class TMProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}


@admin.register(TM_ProductStatus)
class TMProductStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}


class TProductFeatureInline(admin.TabularInline):
    model = T_ProductFeature
    extra = 1
    fields = ('order', 'description')
    ordering = ('order',)


@admin.register(T_Product)
class TProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_open', 'created_at', 'updated_at')
    list_filter = ('is_open', 'categories', 'statuses')
    search_fields = ('name', 'slug', 'description', 'price')
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ('categories', 'statuses')
    inlines = [TProductFeatureInline]


# =========================
# CHURCH
# =========================

class TChurchServiceInline(admin.TabularInline):
    model = T_ChurchService
    extra = 1
    fields = ('order', 'name', 'day', 'time')
    ordering = ('order',)


@admin.register(T_Church)
class TChurchAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'contact_pdt', 'contact_ketua')
    search_fields = ('name', 'slug', 'address')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [TChurchServiceInline]


@admin.register(T_ChurchService)
class TChurchServiceAdmin(admin.ModelAdmin):
    list_display = ('church', 'name', 'day', 'time', 'order')
    list_filter = ('day', 'church')
    search_fields = ('church__name', 'name', 'day', 'time')
    ordering = ('church', 'order', 'id')


# =========================
# CONTACT REQUEST
# =========================

@admin.register(T_ContactRequest)
class TContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'request_type', 'status', 'wa_number', 'email', 'created_at')
    list_filter = ('request_type', 'status', 'created_at')
    search_fields = ('name', 'wa_number', 'email', 'details', 'admin_notes')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


# =========================
# ORGANIZATION / VERSION
# =========================

@admin.register(TM_Position)
class TMPositionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(TM_Division)
class TMDivisionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(T_Staff)
class TStaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'division', 'position', 'is_active', 'created_at')
    list_filter = ('division', 'position', 'is_active')
    search_fields = ('name',)
    list_editable = ('is_active',)
    ordering = ('division__name', 'position__name', 'name')