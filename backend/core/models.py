from django.db import models


class PostDetail(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    divar_post_token = models.TextField(null=False, blank=False, unique=True)
    divar_post_data = models.JSONField(null=False, blank=False, default=dict)
    knowledge = models.TextField(null=True, blank=True)


class Conversation(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(PostDetail, on_delete=models.PROTECT, null=False, blank=False)
    user_id = models.TextField(null=False, blank=False)
    supplier_id = models.TextField(null=False, blank=False)
    messages = models.TextField(null=False, blank=False, default=list)
