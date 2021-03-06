from rest_framework.response import Response
from utils.permissions import (IsAuthenticated,
                                        IsAdminUser,
                                        IsModeratorUser,
                                        IsStaffUser,
                                        IsUser) 
from authentication.models import StdUser


P = {'IsAuthenticated': IsAuthenticated,
    'IsAdminUser': IsAdminUser,
    'IsModeratorUser': IsModeratorUser,
    'IsStaffUser': IsStaffUser,
    'IsUser': IsUser, }


# decorator for get access to request by extraneous
def permission(permission):
    def perm(func):
        def p(request, args, **kwargs):
            permis = P.get(permission)
            if (permis.has_permission(StdUser.objects.get(email=args.user))) is True:
                return func(request, args, **kwargs)
            else:
                return Response({'Status': 'User has no permissions'})
        return p
    return perm

# decorator for multiple rights
def permissions(permissions,argument):
    def perm(func):
        def p(request, args, **kwargs):
            for permission in permissions:
                if (permission == "IsAdminUser") or (permission == "IsModeratorUser") or (permission == "IsStaffUser"):
                    permis = P.get(permission)
                    if permis.has_permission(StdUser.objects.get(email=args.user)) is True:
                        return func(request, args, **kwargs)
                elif (permission == "IsUser"):
                    permis = P.get(permission)
                    if argument == "args":
                        if permis.has_object_permission(StdUser.objects.get(email=args.user), StdUser.objects.get(id=args.data.get('id'))) is True:
                            return func(request, args,**kwargs)
                        else:
                            return Response({'Status': 'User has no permissions'})
                    elif argument == "kwargs":
                        if permis.has_object_permission(StdUser.objects.get(email=args.user), StdUser.objects.get(id=kwargs.get('id'))) is True:
                            return func(request, args, **kwargs)
                        else:
                            return Response({'Status': 'User has no permissions'})
                else:
                    return Response({"Status":"No such request"})
        return p
    return perm

# decorator for owner
def object_permission(permission,argument):
    def perm(func):
        def p(request, args, **kwargs):
            permis = P.get(permission)
            if argument == "kwargs":
                if permis.has_object_permission(StdUser.objects.get(email=args.user), StdUser.objects.get(id=kwargs.get('id'))) is True:
                    return func(request, args, kwargs)
                else:
                    return Response({'Status': 'User has no permissions'})
            elif argument == "args":
                if permis.has_object_permission(StdUser.objects.get(email=args.user), StdUser.objects.get(id=args.data.get('id'))) is True:
                    return func(request, args,kwargs)
                else:
                    return Response({'Status': 'User has no permissions'})
            else:
                return Response({"Status":"No such request"})
        return p
    return perm



