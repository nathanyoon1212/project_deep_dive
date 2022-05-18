from datetime import timedelta, datetime
from django.http          import JsonResponse
from django.db.models     import Q, Count
from django.views         import View

from petsitters.models    import Petsitter, Type, PetsitterImage, Comment
from bookings.models      import Booking 

class PetsitterListView(View):
    def get(self, request):
        sort_by      = request.GET.get('sort_by')
        check_in     = request.GET.get('check_in', None)
        check_out    = request.GET.get('check_out', None)
        keyword      = request.GET.get('keyword', "")
        type_id      = request.GET.get('type_id', None)
        offset       = int(request.GET.get('offset', 0))
        limit        = int(request.GET.get('limit', 10))
        booked_list  = []

        sorting_options = {
            "low_price"      : "price", 
            "many_comments"  : "-comment_count"        
        }

        if check_in and check_out:
            check_in  = datetime.strptime(check_in, '%Y-%m-%d')  
            check_out = datetime.strptime(check_out, '%Y-%m-%d') 

            q_booking = Q(checkout_date__range=[check_in+timedelta(days=1), check_out]) | \
                        Q(checkin_date__range=[check_in, check_out-timedelta(days=1)])
        
            booked_list = Booking.objects.filter(q_booking)

        q = Q()

        if type_id:
            q &= Q(types__id = type_id)

        if keyword:
            q &= Q(address__icontains = keyword)
        
        petsitters = Petsitter.objects\
                              .exclude(booking__in=booked_list)\
                              .annotate(comment_count = Count('comment__id'))\
                              .filter(q)\
                              .order_by(sorting_options.get(sort_by, "id"))[offset : offset+limit]

        results = [{           
            "id"              : petsitter.id, 
            "title"           : petsitter.title,
            "price"           : int(petsitter.price),
            "grade"           : petsitter.grade,
            "type"            : [type.name for type in petsitter.types.all()],
            "information"     : petsitter.information,
            "address"         : petsitter.address,
            "comment_count"   : petsitter.comment_set.all().count(),
            "petsitter_image" : [image.image_url for image in petsitter.petsitterimage_set.all()]
        } for petsitter in petsitters]
        return JsonResponse({"results" : results}, status=200)

class PetsitterDetailView(View):
    def get(self, request, petsitter_id):
        try:
            petsitter = Petsitter.objects.get(id=petsitter_id)

            result    = {
                "id"              : petsitter.id, 
                "name"            : petsitter.name,
                "title"           : petsitter.title,
                "price"           : int(petsitter.price),
                "grade"           : petsitter.grade,
                "count"           : petsitter.count,
                "type"            : [type.name for type in petsitter.types.all()],
                "information"     : petsitter.information,
                "address"         : petsitter.address,
                "longitude"       : float(petsitter.longitude),
                "latitude"        : float(petsitter.latitude),
                "petsitter_image" : [image.image_url for image in petsitter.petsitterimage_set.all()]
            }
            return JsonResponse({"result" : result}, status=200)

        except petsitter.DoesNotExist:
            return JsonResponse({"message" : "PETSITTER DOES NOT EXIST"}, status=404)
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)