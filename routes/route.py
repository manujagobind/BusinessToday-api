from controllers import *

routing = [
    (r'/test', test.testHandler),
    (r'/auth/business/register', auth.RegisterBusinessHandler),
    (r'/auth/business/login', auth.BusinessLoginHandler),
    (r'/auth/admin/login', auth.AdminLoginHandler),
    (r'/auth/checktoken', auth.CheckTokenHandler),
]
