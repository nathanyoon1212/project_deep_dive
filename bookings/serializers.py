from telnetlib import STATUS
import uuid
from django.db.models import Q
from datetime         import datetime, timedelta
from django.db                  import transaction
from rest_framework             import serializers, exceptions
from rest_framework.serializers import ModelSerializer
from bookings.models        import Booking
from petsitters.models      import Petsitter
from users.models           import User

class BookingSerializer(ModelSerializer):

    @transaction.atomic()
    def create(self, request, validated_data):
        try:
            user      = validated_data.pop('user')
            check_in  = datetime.strptime(validated_data['check_in'],'%Y-%m-%d')
            check_out = datetime.strptime(validated_data['check_out'],'%Y-%m-%d')
            
            if check_in < datetime.today() :
                raise serializers.ValidationError("Not_Allowed_to_Book_Before_Today")
            
            if check_out < check_in :
                raise serializers.ValidationError("INVALID_BOOKING_DATE")
            
            q = Q() 
            q |= Q(check_in__range  = [check_in,check_out-timedelta(days=1)])
            q |= Q(check_out__range = [check_in+timedelta(days=1),check_out])
            
            if Booking.objects.filter(q, petsitter_id = petsitter.id, user=request.user).exists():
                raise serializers.ValidationError("DOUBLE_BOOKED_FOR_THE_DAY")

            petsitter = Petsitter.objects.get(id=petsitter.id)
            
            with transaction.atomic():
                
                booking = Booking.objects.create(
                            code                  = str(uuid.uuid4()),
                            check_in              = check_in,
                            check_out             = check_out,
                            status                = 'booked',
                            email                 = request.data.get('email'),
                            nickname              = request.data.get('nickname'),
                            user                  = request.user,
                            petsitter             = petsitter,
                        )
                
                for i in range(int((check_out-check_in).days)):
                    date = datetime.date(check_in + timedelta(days=i))
                    
                    Booking.objects.create(
                            booking = booking.get(check_in=date),
                        )

                return booking
        
        except Booking.DoesNotExist:
            raise serializers.ValidationError("BOOKING_NOT_AVAILABLE")
    
    @transaction.atomic()
    def update(self, instance, validated_data):
        instance.checkin_date  = validated_data.get('checkin_date', instance.checkin_date)
        instance.checkout_date = validated_data.get('checkout_date', instance.checkout_date)
        instance.petsitter_id  = validated_data.get('petsitter_id', instance.petsitter_id)
        instance.nickname      = validated_data.get('nickname', instance.nickname)
        instance.email         = validated_data.get('email', instance.email)
        instance.save()
        return instance
    
    class Meta:
        model = Booking
        fields = ["id", "checkin_date", "checkout_date", "status", "petsitter_id", "nickname", "email"]
        extra_kwargs = {
            "id": {"read_only": True}
        }

        
