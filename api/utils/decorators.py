from rest_framework.response import Response
from authentication.permissions import * 
from authentication.models import StdUser
P={ 'IsAuthenticated':IsAuthenticated,
    'IsAdminUser':IsAdminUser,
    'IsModeratorUser':IsModeratorUser}

def permission(permissions):
    def perm(func):
        def p(request,args,**kwargs):
            for permission in permissions:
                permission = P.pop(permission)
                if permission.has_permission(StdUser.objects.get(email=args.user)) is True:
                    return func(request,args,kwargs) 
                else:
                    return Response(
                            data={"Error": "User has no permissions"})
        return p
    return perm
