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
                print(args)
                if StdUser.objects.get(id=2).has_perm(permission) is True:
                    print("Check") 
                else:
                    return Response(
                            data={"Error": "User has no permissions"})
            return func(request,*args,**kwargs)
        return p
    return perm
