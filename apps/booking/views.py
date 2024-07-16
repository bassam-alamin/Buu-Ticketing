from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Theater, Reservation, TheatreSession
from .serializers import TheaterSerializer, TheatreSessionSerializer, ReservationSerializer


class IsAdminOrReadonly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Only allow creation if the user is admin
        return (request.user and request.user.is_authenticated
                and request.user.is_staff)


class TheaterViewSet(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrReadonly]
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer

    def get_queryset(self, *args, **kwargs):
        return Theater.objects.all()


class TheatreSessionViewSet(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrReadonly]
    queryset = TheatreSession.objects.all()
    serializer_class = TheatreSessionSerializer

    def get_queryset(self, *args, **kwargs):
        return TheatreSession.objects.all()


class ReservationViewSet(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, ]
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self, *args, **kwargs):
        return Reservation.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)


class ListAvailableSeatsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = TheatreSession.objects.all()
    serializer_class = TheatreSessionSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'seating_id', openapi.IN_QUERY,
                description="Seating ID",
                type=openapi.FORMAT_UUID)
        ]
    )
    def get(self, request, *args, **kwargs):
        queryset = self.queryset.get(id=request.GET.get('seating_id'))
        return Response(
            queryset.available_seats,
            status=status.HTTP_200_OK
        )


class ListTheatresView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'date', openapi.IN_QUERY,
                description="Seating date",
                type=openapi.FORMAT_DATE)
        ]
    )
    def get(self, request, *args, **kwargs):
        queryset = self.queryset.filter(
            theatresession__date=request.GET.get('date')
        )
        data = cache.get(f"theater_list_{request.GET.get('date')}")
        if data is None:
            data = self.serializer_class(queryset, many=True).data
            # This is set to 15 minutes but since it will take long
            # to setup a new theater you can set this to even 1 year
            cache.set(f"theater_list_{request.GET.get('date')}", data, timeout=60 * 15)
        return Response(
            data,
            status=status.HTTP_200_OK
        )


class ReservationDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, ]
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'seating_id', openapi.IN_QUERY,
                description="Seating ID",
                type=openapi.FORMAT_DATE)
        ]
    )
    def get(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            queryset = self.queryset.filter(
                seating_id=request.GET.get('seating_id')
            )
            return Response(
                self.serializer_class(queryset, many=True).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                "message": "Not allowed to view reservation details"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
