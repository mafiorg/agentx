from django.conf import settings
from openai import OpenAI

client = OpenAI(
    base_url=settings.METISAI_WRAPPER_OPENAI_BASEURL,
    api_key=settings.METISAI_API_KEY,
)

# constants
RESPONSE_FORMAT_JSON_OBJECT = {"type": "json_object"}
RESPONSE_FORMAT_TEXT = {"type": "text"}

MODEL_GPT_3_5_TURBO = "gpt-3.5-turbo"
MODEL_GPT_4O_MINI = "gpt-4o-mini"


"""response object
ChatCompletion(
    id='', 
    choices=[
        Choice(
            finish_reason='stop', 
            index=0, 
            logprobs=None, 
            message=ChatCompletionMessage(
                content='Hi there! How are you doing today?', 
                refusal=None, 
                role='assistant', 
                audio=None, 
                function_call=None, 
                tool_calls=None)
        )
    ], 
    created=1729959784858, 
    model='gpt-4o-mini', 
    object='', 
    service_tier=None, 
    system_fingerprint=None, 
    usage=CompletionUsage(
        completion_tokens=9, 
        prompt_tokens=11, 
        total_tokens=20, 
        completion_tokens_details=None, 
        prompt_tokens_details=None)
    )
"""
def chat_completion(content: str, response_format=RESPONSE_FORMAT_TEXT, model=MODEL_GPT_4O_MINI):
    return client.chat.completions.create(
        model=model,
        response_format=response_format,
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
    )
