from controllers import *

routing = [
    (r'/', test.testHandler),
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
    (r'/deal/request', deal.RequestDealHandler),
    (r'/deal/settle', deal.SettleDealHandler),
    (r'/deal/cancel', deal.CancelDealHandler),
    (r'/deal/requested', deal.DealsRequestedHandler),
    (r'/deal/received', deal.DealRequestsReceivedHandler),
    (r'/deal/buyer/settled', deal.BuyerSettledDealsHandler),
    (r'/deal/seller/settled', deal.SellerSettledDealsHandler),
    (r'/deal/buyer/cancelled', deal.BuyerCancelledDealsHandler),
    (r'/deal/seller/cancelled', deal.SellerCancelledDealsHandler),
]
