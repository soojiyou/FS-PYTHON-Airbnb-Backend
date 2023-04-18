from django.contrib import admin
from .models import House


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    # list 보다 tuple을 더 많이 사용하는데 아이탬이 하나일경우 ,주의
    fields = ("name", "address", ("price_per_night",
                                  "pets_allowed"))
    list_display = (
        "name",
        "price_per_night",
        "address",
        "pets_allowed"
    )
    list_filter = (
        "price_per_night",
        "pets_allowed"
    )
    search_fields = ("address__startswith",)
