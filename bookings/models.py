import uuid

from django.db   import models
from core.models import TimeStampModel

class Booking(TimeStampModel):
    STATUS_TYPE = [
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
        ('in_progress', 'In_Progress'),
        ('deleted', 'Deleted')
    ]
    code          = models.UUIDField(default=uuid.uuid4, editable=False)
    checkin_date  = models.DateField()
    checkout_date = models.DateField()
    status        = models.CharField(max_length=30, choices = STATUS_TYPE, default='in_draft')
    nickname      = models.CharField(max_length=100, null=True)
    email         = models.CharField(max_length=150, null=True)
    user          = models.ForeignKey('users.User', on_delete=models.CASCADE)
    petsitter     = models.ForeignKey('petsitters.Petsitter', on_delete=models.CASCADE)

    class Meta:
        db_table = 'bookings'


