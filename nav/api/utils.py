from functools import wraps

def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kw):
        print(func)
        # if x_sign != None:
        #     print(x_id, x_key, x_sign)
        # else:
        #     print(x_id, x_key, x_sign)
        return func
    return wrapper



# def authenticate_token

# def authenticate(requests, *args, **kw):
#     print("Authenticated")
#     session = requests.headers.get('X-LC-Session', '')
#     user = User.objects(sessionToken=session).first()
#
#     if user is None:
#         raise AuthenticatedError
