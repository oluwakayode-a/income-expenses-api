from rest_framework.views import exception_handler

def custom_exception_handler(exception, context):
    handlers = {
        "ValidationError" : handle_generic_error,
        "Http404" : handle_generic_error,
        "PermissionDenied" : handle_generic_error,
        "NotAuthenticated" : handle_authentication_error,
    }

    response = exception_handler(exception, context)

    if response is not None:
        response.data["status_code"] = response.status_code

    exception_class = exception.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exception, context, response)
    
    return response

def handle_authentication_error(exception, context, response):
    response.data = {
        "error" : "Please log in to proceed",
        "status_code": response.status_code
    }

    return response

def handle_generic_error(exception, context, response):
    return response