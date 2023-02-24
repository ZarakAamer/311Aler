from .models import Price





def priceing(request):
    return {"prices":Price.objects.all()}