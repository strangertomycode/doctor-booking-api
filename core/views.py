from django.http import JsonResponse


def home(request):
    return JsonResponse(
        {
            "message": "Doctor Booking API is running successfully",
            "documentation": "/api/docs/",
            "redoc": "/api/redoc/",
        }
    )
