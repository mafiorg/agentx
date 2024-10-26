import requests
import uuid
from django.conf import settings


def create_oauth_init_url(post_token, scope):
    #scope = 'CHAT_POST_CONVERSATIONS_READ'  #USER_PHONE
    return f'https://api.divar.ir/oauth2/auth?response_type=code&client_id={settings.DIVAR_OAUTH_CLIENT_ID}&redirect_uri={settings.DIVAR_OAUTH_REDIRECT_URL}&scope={scope}&state={post_token}_{str(uuid.uuid4())}'


# TODO: refresh token?
def get_access_token(code):
    url = "https://api.divar.ir/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    payload = {
        "code": code,
        "client_id": settings.DIVAR_OAUTH_CLIENT_ID,
        "client_secret": settings.DIVAR_OAUTH_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": settings.DIVAR_OAUTH_REDIRECT_URL,
    }

    response = requests.post(url, data=payload, headers=headers)
    
    """response
    {
        "access_token": "ory_at_mAODvjM21UayVFDtP_KxsCDVwwpb5pwHoNks3vCIeJ8.Gx2sCv2jT4VIbbZDHDIRRwhi45AwV-St1W-gDNdxUUw",
        "expires_in": 3600,
        "scope": "...",
        "token_type": "bearer"
    }
    """
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


# https://github.com/divar-ir/kenar-docs/blob/master/finder/get_post.md
def get_post(post_token):
    url = f"https://api.divar.ir/v1/open-platform/finder/post/{post_token}"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": settings.DIVAR_API_TOKEN,
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


# https://github.com/divar-ir/kenar-docs/blob/master/chat/read_messages.md
def setup_post_on_message_hook(post_token, oauth_access_token):
    url = "https://api.divar.ir/v1/open-platform/notify/chat/post-conversations"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": settings.DIVAR_API_TOKEN,
        "x-access-token": oauth_access_token
    }
    payload = {
        "post_token": post_token,
        "endpoint": settings.DIVAR_ON_MESSAGE_HOOK_URL,
        "identification_key": settings.DIVAR_AUTHORIZATION_HEADER_KEY,
    }

    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


# TODO: send message
