from django.contrib import admin
from django.urls import include, path
from django.http import JsonResponse
from django.shortcuts import render
from store.models import Branch, Category, Product


def home(request):
    # Keep the root URL useful as both a human-facing landing page and a quick
    # deployment smoke check, even before inventory has been imported.
    context = {
        "branches": Branch.objects.filter(is_active=True).order_by("city", "name"),
        "categories": Category.objects.filter(is_active=True, parent__isnull=True).order_by("sort_order", "name")[:8],
        "featured_products": Product.objects.filter(is_active=True, is_featured=True)
        .select_related("category").prefetch_related("images")[:4],
        "product_count": Product.objects.filter(is_active=True).count(),
    }
    return render(request, "store/home.html", context)

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("api/v1/", include("store.urls")),
    path("health/", lambda request: JsonResponse({"status": "ok"})),
]

