from controllers import *

routing = [
    (r'/test', test.testHandler),
    (r'/auth/business/register', auth.RegisterBusinessHandler),
    (r'/auth/business/login', auth.BusinessLoginHandler),
    (r'/auth/admin/new', auth.AddNewAdminHandler),
    (r'/auth/admin/login', auth.AdminLoginHandler),
    (r'/auth/logout', auth.LogoutHandler),
    (r'/user', user.RetrieveCurrentUserHandler),
    (r'/user/products', user.RetrieveAllProductsOfCurrentBusinessHandler),
    (r'/user/product/new', user.AddProductsHandler),
    (r'/product/id', product.RetrieveProductByIdHandler),
    (r'/feed', feed.FeedHandler),
]
