from urllib import response
from django.http import JsonResponse


def error404(request, *args, **kwargs):
    message = "Route does not exist"

    response = JsonResponse(data={"message" : message, "status_code" : 404})
    response.status_code = 404

    return response


def error500(request, *args, **kwargs):
    message = "Server error occured. Please try again, or contact admin."

    response = JsonResponse(data={"message" : message, "status_code" : 500})
    response.status_code = 500

    return response
