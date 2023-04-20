from django.db import models


class Room(models.Model):

    """Room model definition."""
    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = ("shared_room", "Shared_Room")

    country = models.CharField(max_length=150, default="United States",)
    city = models.CharField(max_length=80, default="Los Angeles",)
    price = models.PositiveIntegerField()
    rooms = models.PositiveBigIntegerField()
    toilets = models.PositiveSmallIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=250,)
    pet_friendly = models.BooleanField(default=True,)
    kind = models.CharField(max_length=20, choices=RoomKindChoices.choices,)
