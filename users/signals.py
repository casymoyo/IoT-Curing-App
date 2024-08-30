# from . models import User
# from django.auth.contrib import get_user_model
# from django.db.models.signals import post_save

# @post_save(post_save, sender=User)
# def assign_admin_role(sender, instance, **kwargs):
#     user = get_user_model()
#     if not user.objects.exists():
#         instance.role = 'Admin'
#         instance.save()
    
    