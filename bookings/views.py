import json, uuid
from typing import Any, Tuple

from datetime         import datetime, timedelta
from django.db.models import Q
from django.db        import transaction
from django.http      import JsonResponse
from django.views     import View
from requests import Response
from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework.permissions import IsAuthenticated
# from core.utils          import login_decorator
from petsitters.models   import Petsitter
from bookings.models     import Booking
from users.models        import User
from bookings.serializers   import BookingSerializer

class BookingView(APIView):
    # @login_decorator
    def post(self, request):
        user = request.user
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)



# def get_booking_n_check_err(booking_id, user) -> Tuple[Any, str]:
#     if not booking_id:
#         return None, "no booking id"
#     try:
#         booking = Booking.objects.get(id=booking_id) 
#     except Booking.DoesNotExist:
#         return None, f"booking {booking_id} does not exists"
#     if booking.status == 'deleted':
#         return None, f"booking {booking_id} is deleted"
#     if user not in booking.users.all():
#         return None, f"{user.email} have no permission to booking {booking.name}"
#     return booking, None 