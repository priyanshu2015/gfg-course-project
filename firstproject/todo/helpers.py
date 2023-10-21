from django.http import JsonResponse


def get_404_json_response():
    return JsonResponse(
        {
            "status": "error",
            "message": "Not Found",
            "payload": {}
        },
        status=404
    )


def update_object(obj, **kwargs):
    for k, v in kwargs.items():
        setattr(obj, k, v)
    obj.save()