from django.shortcuts import render, redirect
import json
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import HttpResponseRedirect, JsonResponse
from rest_framework.response import Response
from django.shortcuts import render
from backend.client import divar
from backend.core.models import PostDetail, Conversation
import asyncio
from backend.core.tasks import process_conversation_update


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

    data = request.POST

    sender = data.get("payload").get("sender")
    if sender.get("is_supply"):
        # TODO: mark conversation to not respond automatically anymore (age taraf ba moshtari sohbat kone dg bot javab nade be payame moshtari)
        return Response(status=200)
    
    post_token = data.get("payload").get("metadata").get("post_token")
    
    post_detail = PostDetail.objects.get(poster_token=post_token)
    
    conversation, created = Conversation.objects.get_or_create(
        post=post_detail,
        user_id=sender.get("id"),
    )

    conversation.messages.append(data)
    conversation.save()
    
    """
    Important Note:
    If you’re using Django with a production server like Gunicorn or uWSGI, which are often configured to fork processes, asyncio.create_task() may not work as expected because it relies on the event loop of the main process. For production use cases or long-running background tasks, you might want to consider a task queue like Celery.

    For development or lightweight tasks, however, asyncio.create_task() works well within Django views.
    """
    asyncio.create_task(process_conversation_update(conversation))

    return Response(status=200)


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

    # TODO: response? save the response? error handling
    divar.setup_post_on_message_hook(divar_post_token, divar_access_token.get("access_token"))

    return redirect(post_detail.divar_post_return_url)
