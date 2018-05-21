import json

from django.views import View
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize

from .models import Goods


class GoodBaseView(View):
    """
    商品列表页
    """
    def get(self, request):
        all_goods = Goods.objects.all()[:10]
        json_data = serialize('json', all_goods)
        json_data = json.loads(json_data)
        # return HttpResponse(json_data, content_type='application/json')
        return JsonResponse(json_data, safe=False)

