from django.shortcuts import render

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import HttpResponseRedirect, JsonResponse

@api_view(["GET"])
# @authentication_classes([JWTStatelessUserAuthentication])
# @permission_classes([IsAuthenticated])
def app_start(request):
    user_id = request.user.id
    post_token = request.GET.get("post_token")
    return_url = request.GET.get("return_url")

    # inja etelaAte ezafi az user migirim bara agahish va ok mikonim redirect mikonim bere khone
    # darvaghe service faal kardane agentX roye agahiye
    print(request.body)

    return JsonResponse("OK", safe=False)


@api_view(["POST"]) #nemikhaim?
# @authentication_classes([JWTStatelessUserAuthentication])
# @permission_classes([IsAuthenticated])
def chat_start(request):
    user_id = request.user.id

    # chi bebine? bere OAuth2? ke beshe chat kone?

    print(request.body)  #{"callback_url":"https://open-platform-redirect.divar.ir/completion","post_token":"post-token","user_id":"demand_id","peer_id":"supplier_id","supplier":{"id":"supplier_id"},"demand":{"id":"demand_id"}}
    
    return JsonResponse("OK", safe=False)


@api_view(["POST"])
# @authentication_classes([JWTStatelessUserAuthentication])
# @permission_classes([IsAuthenticated])
def on_message(request):
    user_id = request.user.id

    """
    POST {{ endpoint }}
Content-Type: application/json
authorization: {{ identification_key }}
{
  "payload": {
    "data": {
      "text": ""
    },
    "sender": {
      "id": "",
      "is_supply": bool
    },
    "id": "",
    "metadata": {
      "category": "",
      "post_token": "",
      "title": ""
    },
    "sent_at": "",
    "receiver": {
      "id": "",
      "is_supply": bool
    },
    "type": "TEXT"
  },
  "timestamp": "",
  "type": "CHAT_MESSAGE"
}
    """

    # chi bebine? bere OAuth2? ke beshe chat kone?

    print(request.body)  #{"callback_url":"https://open-platform-redirect.divar.ir/completion","post_token":"post-token","user_id":"demand_id","peer_id":"supplier_id","supplier":{"id":"supplier_id"},"demand":{"id":"demand_id"}}
    
    return JsonResponse("OK", safe=False)
