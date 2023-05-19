from django.utils import timezone
from rest_framework import serializers
from .models import Booking


class CreateRoomBookingSerializer(serializers.ModelSerializer):
    # model에서의 check_in, check_out값이 필수가 아니라 덮어쓴것
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = ("check_in", "check_out", "guests")

    # 추가로 필터해야될떄 views에서말고 여기서도 가능함
    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError(
                "The booking date should be in future.")
        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError(
                "The booking date should be in future.")
        return value

    # data안에 "check_in", "check_out", "guests"다 들어있음/ validate()는 모든 속성을 한번에 validate할수있다.
    def validate(self, data):
        room = self.context.get("room")
        if data["check_out"] <= data["check_in"]:
            raise serializers.ValidationError(
                "Check_out date should be later than check_in date.")
        if Booking.objects.filter(
            room=room,
            check_in__lt=data["check_out"],
            check_out__gt=data["check_in"],
        ).exists():
            raise serializers.ValidationError(
                "Those or some of those dates are already taken.")
        return data


class CreateExperienceBookingSerializer(serializers.ModelSerializer):
    experience_time = serializers.DateTimeField()

    class Meta:
        model = Booking
        fields = ("experience_time", "guests")

    # 추후에 experience 정원 setting해서 초과되면 validate 하는 거 추가 가능
    def validate_experience_time(self, value):
        experience = self.context["experience"]
        if value.time() != experience.start:
            raise serializers.ValidationError(
                "Experience time have to be same with the experience start of time"
            )
        return value


class PublicBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ("pk", "check_in", "check_out", "experience_time", "guests")
