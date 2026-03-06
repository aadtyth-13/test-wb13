import os
import uuid


def event_image_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f"events/{uuid.uuid4().hex}{ext}"


def event_gallery_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f"events/gallery/{uuid.uuid4().hex}{ext}"


def product_image_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f"products/{uuid.uuid4().hex}{ext}"


def church_image_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f"churches/{uuid.uuid4().hex}{ext}"


def staff_image_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f"staff/{uuid.uuid4().hex}{ext}"