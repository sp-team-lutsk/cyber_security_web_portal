from rest_framework.response import Response
from authentication.permissions import * 
from authentication.models import StdUser

# decorator for get access to request by extraneous
def permission(permission):
    def perm(func):
        def p(request,args,**kwargs):
                permission = P.pop(permission)
                if permission.has_permission(StdUser.objects.get(email=args.user)) is True:
                    return func(request,args,kwargs)
                else:
                    return Response({'Status': 'User has no permissions'})
        return p
    return perm

# decorator for owner
def object_permission(permission):
    def perm(func):
        def p(request,args,**kwargs):
                permission = P.pop(permission)
                if permission.has_object_permission(StdUser.objects.get(email=args.user),StdUser.objects.get(id=kwargs.get('id'))) is True:
                    return func(request,args,kwargs)
                else:
                    return Response({'Status': 'User has no permissions'})
        return p
    return perm

def permissions(permissions):
    def perm(func):
        def p(request,args,**kwargs):
            for permission in permissions:
                if (permission == "IsAdminUser") or (permission == "IsModeratorUser") or (p == IsStaffUser):
                    p = P.pop(p)
                    if permission.has_permission(StdUser.objects.get(email=args.user)) is True:
                        return func(request,args,kwargs)
                    else:
                        return Response({'Status': 'User has no permissions'})
                else:
                    if permission.has_object_permission(StdUser.objects.get(email=args.user),StdUser.objects.get(id=kwargs.get('id'))) is True:
                        return func(request,args,kwargs)
                    else:
                        return Response({'Status': 'User has no permissions'})
         return p
    return perm
