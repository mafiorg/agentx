from django.shortcuts import render, redirect
import json
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import HttpResponseRedirect, JsonResponse

from django.shortcuts import render
from backend.client import divar
from backend.core.models import PostDetail


@api_view(["GET", "POST"])
# @authentication_classes([JWTStatelessUserAuthentication])
# @permission_classes([IsAuthenticated])
def app_start(request):

    if request.method == 'POST':
        knowledge = request.POST.get('knowledge')

        divar_post_token = request.GET.get("post_token")
        divar_post_return_url = request.GET.get("return_url")

        divar_post_data = divar.get_post(divar_post_token)

        post_detail, created = PostDetail.objects.get_or_create(
            divar_post_return_url=divar_post_return_url,
            divar_post_token=divar_post_token,
        )
        post_detail.divar_post_data = divar_post_data
        post_detail.knowledge=knowledge
        post_detail.save()

        oauth_grant_url = divar.create_oauth_init_url(
            post_token=divar_post_token, 
            scope='CHAT_POST_CONVERSATIONS_READ'
        )

        return redirect(oauth_grant_url)

    # TODO: check params?
    # post_token = request.GET.get("post_token")
    # return_url = request.GET.get("return_url")

    # Show enable agent-x for post view
    return render(request, 'appstart.html')


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


@api_view(["GET"])
def oauth_callback(request):

    if request.GET.get("error"): # TODO
        print(request.GET.get("error"))
        print(request.GET.get("error_description"))
        return redirect("https://error.com")

    # scope = request.GET.get("scope")
    state = request.GET.get("state")
    code = request.GET.get("code")
    post_token = state.split("_")[0]

    divar_access_token = divar.get_access_token(code)

    # get access token save it in the post and return to post return url
    post_detail = PostDetail.objects.filter(divar_post_token).first()
    post_detail.divar_access_token = divar_access_token
    post_detail.save()

    # TODO: do we need a middle page that notify the user we are processing the data needed?

    # TODO: setup post on_message hook
    # TODO: response? save the response? error handling
    divar.setup_post_on_message_hook(divar_post_token, divar_access_token.get("access_token"))

    return redirect(post_detail.divar_post_return_url)
