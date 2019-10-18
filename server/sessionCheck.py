from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class sessioncheck(MiddlewareMixin):
    '''
    拦截地址，防止用户误进入其他页面
    '''
    def process_request(self,request):
        path=request.path
        if path.startswith("/server") and path!="/server/login/":
            admin=request.session.get("admin")
            data=request.POST.get("pwd")
            if not admin:
                #如果用户没有登录过而进入到其他页面，那么就直接回到登录界面
                if path=="/server/loginCheck/":
                    #若提交loginCheck
                    if data:
                        pass
                    else:
                        return redirect("/server/login/")
                else:
                    return redirect("/server/login/")