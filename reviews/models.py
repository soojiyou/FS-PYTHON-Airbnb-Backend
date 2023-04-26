from django.db import models
from common.models import CommonModel


class Review(CommonModel):

    """Review from a User to a room or experience"""

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="reviews",)
    room = models.ForeignKey("rooms.Room", null=True,
                             blank=True, on_delete=models.SET_NULL, related_name="reviews",)
    experience = models.ForeignKey(
        "experiences.Experience", null=True, blank=True, on_delete=models.CASCADE, related_name="reviews",)
    payload = models.TextField()
    rating = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.user} / {self.rating}⭐"

    def owner_or_hostname(self):
        if self.room:
            return self.room.owner.username
        elif self.experience:
            return self.experience.owner.username
        else:
            return None
