from django.http import JsonResponse

def handler404(request):
    response = JsonResponse({'msg':'not found'})
    response.status_code = 404
    return response


def handler500(request):
    response = JsonResponse({'msg':'internal server error'})
    response.status_code = 500
    return response