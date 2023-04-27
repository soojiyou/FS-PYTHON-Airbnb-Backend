from django.db import transaction
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from . import serializers, models
from categories.models import Category
from medias.serializers import PhotoSerializer
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateExperienceBookingSerializer


class Experiences(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_experiences = models.Experience.objects.all()
        serializer = serializers.ExperienceListSerializer(
            all_experiences, many=True, context={"request": request},)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.ExperienceDetailSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required.")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.ROOMS:
                    raise ParseError(
                        "The kind of category should be 'experineces'.")
            except Category.DoesNotExist:
                raise ParseError("Category not found.")
            try:
                with transaction.atomic():
                    experience = serializer.save(
                        host=request.user,
                        category=category,
                    )
                    perks = request.data.get("perks")
                    for perk_pk in perks:
                        perk = models.Perk.objects.get(pk=perk_pk)
                        experience.perks.add(perk)
                    serializer = serializers.ExperienceDetailSerializer(
                        experience, context={"request": request},)
                    return Response(serializer.data)
            except Exception:
                raise ParseError("Perk not found.")
        else:
            return Response(serializer.errors)


class ExperienceDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return models.Experience.objects.get(pk=pk)
        except models.Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = serializers.ExperienceDetailSerializer(
            experience, context={"request": request},)
        return Response(serializer.data)

    def put(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise PermissionDenied
        serializer = serializers.ExperienceDetailSerializer(
            experience, data=request.data, partial=True,)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.ROOMS:
                        raise ParseError(
                            "The kind of category should be 'experiences'.")
                    experience.category = category
                except Category.DoesNotExist:
                    raise ParseError("Category not found.")
            perks = request.data.get("perks")
            if perks:
                try:
                    experience.perks.clear()
                    for perk_pk in perks:
                        perk = models.Perk.objects.get(pk=perk_pk)
                        experience.perks.add(perk)
                except Exception:
                    raise ParseError("Perk not found.")
            updated_experience = serializer.save()
            return Response(serializers.ExperienceDetailSerializer(updated_experience, context={"request": request},).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise PermissionDenied
        experience.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class ExperiencePerkDetail(APIView):
    def get_object(self, pk):
        try:
            return models.Experience.objects.get(pk=pk)
        except models.Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        perks = experience.perks
        serializer = serializers.PerkSerializer(perks, many=True)
        return Response(serializer.data)


class ExperiencePhotos(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return models.Experience.objects.get(pk=pk)
        except models.Experience.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        experience = self.get_object(pk)
        if request.user != experience.host:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(experience=experience)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ExperienceBookings(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return models.Experience.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        bookings = Booking.objects.filter(
            experience=experience, kind=Booking.BookingKindChoices.EXPERIENCE, experience_time__gt=now,)
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        experience = self.get_object(pk)
        serializer = CreateExperienceBookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save(
                experience=experience, user=request.user, kind=Booking.BookingKindChoices.EXPERIENCE,)
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ExperienceBookingDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return models.Experience.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk, booking_pk):
        experience = self.get_object(pk)
        try:
            booking = Booking.objects.get(
                experience=experience,
                kind=Booking.BookingKindChoices.EXPERIENCE,
                pk=booking_pk,
            )
        except Booking.DoesNotExist:
            raise NotFound
        serializer = PublicBookingSerializer(booking)
        return Response(serializer.data)

    def put(self, request, pk, booking_pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise PermissionDenied
        try:
            booking = Booking.objects.get(
                pk=booking_pk,
                experience=experience,
            )
        except Booking.DoesNotExist:
            raise NotFound
        serializer = PublicBookingSerializer(
            booking, data=request.data, partial=True,)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    updated_booking = serializer.save(kind=booking.BookingKindChoices.EXPERIENCE,
                                                      user=request.user,)
                    serializer = PublicBookingSerializer(updated_booking)
                    return Response(serializer.data)
            except Exception:
                return Response(serializer.errors)

    def delete(self, request, pk, booking_pk):
        booking = Booking.objects.get(pk=booking_pk)
        booking.delete()
        return Response(status=HTTP_200_OK)


class Perks(APIView):

    def get(self, request):
        all_perks = models.Perk.objects.all()
        serializer = serializers.PerkSerializer(all_perks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(serializers.PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):
    def get_object(self, pk):
        try:
            return models.Perk.objects.get(pk=pk)
        except models.Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = serializers.PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = serializers.PerkSerializer(
            perk, data=request.data, partial=True)
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(serializers.PerkSerializer(updated_perk).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)
