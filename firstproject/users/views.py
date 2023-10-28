from django.shortcuts import render
from django.http import HttpResponse
from .decorators import group_required


# Create your views here.
@group_required("operations")
def view_operations_dashboard(request):
    return HttpResponse("Operations Dashboard")


# checking permissions
# ct = ContentType.objects.get_for_model()
# user.permissions.filter(codename="view_", contenttype=ct).exists()

# or user.has_perms(('firstapp.view_', ))
# or user.has_perm('firstapp.view_')



# for creating permissions
#1 Creating Custom Model Depenedent Permission through Code
#from django.contrib.auth.models import Group, ContentType, Permission
# ct = ContentType.objects.get_for_model(PremiumProduct)
# permission = Permission.objects.create(codename="can_do_this", contentype = ct)


#2 Creating Custom Model Dependent Permission by adding in Meta of that model

#3 Creating Custom Model Independent Permission by creating a separate model for permissions


# filtering existing permissions
# ct = ContentType.objects.get_for_model(PremiumProduct)
# permission = Permission.objects.get(codename='view_premiumproduct', content_type=ct)


# Adding permission to user
# user.permissions.add(permission)

# Adding permission to group
# new_group, created = Group.objects.get_or_create(name="new_group")
# new_group.permissions.add(permission)
