import jwt
from functools  import wraps
from flask 		import request, Response ,jsonify
from db import db
auth=db['auth']
config='alswns0221'
def login_required(f):     
    user_info=[] 
    def get_user(user_id):
        x = auth.find_one({'id':user_id})
        return x
    									# 1)
    @wraps(f)                   								# 2)
    def decorated_function(*args, **kwargs):
        user_info=[]
        payload='init'					
        access_token = request.headers.get('Authorization') 	# 3)
        if access_token is not None:  							# 4)
            try:    
                payload = jwt.decode(access_token, config, algorithms=['HS256'])			   # 5)
            except jwt.InvalidTokenError as e:
                payload = None   

            if payload is None: return jsonify(messege='need Authorization',status=401)  	# 7)
            
            user_id   = payload['user_id']  					# 8)
            # user_id = user_id
            user    = get_user(user_id) if user_id else None
        else:
            return jsonify(messege='There is not Access Token',status=401)  	# 7) 						# 9)

        return f(user,*args, **kwargs)
    return decorated_function
