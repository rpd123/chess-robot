from android.permissions import Permission, request_permissions, check_permission

def check_permissions(perms):
    for perm in perms:
        if check_permission(perm) != True:
            return False
    return True

perms = [Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE]
    
if  check_permissions(perms)!= True:
    request_permissions(perms)
else:
    print ("No permission")
    