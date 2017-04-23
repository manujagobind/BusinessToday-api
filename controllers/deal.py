from modules import *
from utilities import *

class RequestDealHandler(RequestHandler):
    @coroutine
    def post(self):
        token = self.request.headers['token']
        product_id = self.get_argument('product_id')
        seller_id = self.get_argument('seller_id')
        buyer_id = self.get_argument('buyer_id')
        qty = self.get_argument('qty')

        tokenExists = yield db.tokens.find_one({'token': token, 'type': 'business'})
        if tokenExists:

            dealInitiated = yield db.deals.insert(
                {
                    'product_id': product_id,
                    'seller_id': seller_id,
                    'buyer_id': buyer_id,
                    'qty': qty,
                    'status': 'active'
                })

            if dealInitiated:
                ob = {
                    'status': {
                        'success': 'true',
                        'code': 201,
                        'message': 'Deal Initiated'
                    },
                }
            else:
                ob = {
                    'status': {
                        'success': 'false',
                        'code': 500,
                        'message': 'Deal Not Initiated'
                    }
                }
        else:
            ob = {
                'status': {
                    'success': 'false',
                    'code': 401,
                    'message': 'Invalid Token'
                }
            }
        self.write(json_encode(ob))


class DealsRequestedHandler(RequestHandler):

    @coroutine
    def post(self):
        token = self.request.headers['token']
        token_data = yield db.tokens.find_one({'token': token, 'type': 'business'})
        if token_data:
            org_id = token_data['user_id']
            cursor = db.deals.find({'buyer_id': org_id, 'status': 'active'})
            deals_data = list()
            count = 0
            while(yield cursor.fetch_next):
                deal_data = cursor.next_object()
                deal_data['id'] = str(deal_data['_id'])
                del deal_data['_id']
                count += 1
                deals_data.append(deal_data)
            if deals_data:
                ob = {
                    'status': {
                        'success': 'true',
                        'code': 200,
                        'message': 'Active Deals Found'
                    },
                    'response': {
                        'count': count,
                        'data': deals_data
                    }
                }
            else:
                ob = {
                    'status': {
                        'success': 'false',
                        'code': 404,
                        'message': 'No Active Deals Found'
                    }
                }
        else:
            ob = {
                'status': {
                    'success': 'false',
                    'code': 401,
                    'message': 'Invalid Token'
                }
            }
        self.write(json_encode(ob))

class DealRequestsReceivedHandler(RequestHandler):
    @coroutine
    def post(self):
        token = self.request.headers['token']
        token_data = yield db.tokens.find_one({'token': token, 'type': 'business'})
        if token_data:
            org_id = token_data['user_id']
            cursor = db.deals.find({'seller_id': org_id, 'status': 'active'})
            deals_data = list()
            count = 0
            while(yield cursor.fetch_next):
                deal_data = cursor.next_object()
                deal_data['id'] = str(deal_data['_id'])
                del deal_data['_id']
                count += 1
                deals_data.append(deal_data)
            if deals_data:
                ob = {
                    'status': {
                        'success': 'true',
                        'code': 200,
                        'message': 'Active Deals Found'
                    },
                    'response': {
                        'count': count,
                        'data': deals_data
                    }
                }
            else:
                ob = {
                    'status': {
                        'success': 'false',
                        'code': 404,
                        'message': 'No Active Deals Found'
                    }
                }
        else:
            ob = {
                'status': {
                    'success': 'false',
                    'code': 401,
                    'message': 'Invalid Token'
                }
            }
        self.write(json_encode(ob))


class SettleDealHandler(RequestHandler):
    @coroutine
    def post(self):
        token = self.request.headers['token']
        deal_id = self.get_argument('deal_id')

        tokenExists = yield db.tokens.find_one({'token': token, 'type': 'business'})
        if tokenExists:
            statusUpdated = yield db.deals.update_one(
                {'_id': ObjectId(deal_id) }, { '$set': { 'status': 'settled' } }, upsert=False)
            if statusUpdated:
                ob = {
                    'status': {
                        'success': 'true',
                        'code': 201,
                        'message': 'Deal Settled'
                    },
                }
            else:
                ob = {
                    'status': {
                        'success': 'false',
                        'code': 500,
                        'message': 'Deal Not Settled'
                    }
                }
        else:
            ob = {
                'status': {
                    'success': 'false',
                    'code': 401,
                    'message': 'Invalid Token'
                }
            }
        self.write(json_encode(ob))

class CancelDealHandler(RequestHandler):

    @coroutine
    def post(self):
        token = self.request.headers['token']
        deal_id = self.get_argument('deal_id')
        tokenExists = yield db.tokens.find_one({'token': token, 'type': 'business'})
        if tokenExists:
            statusUpdated = yield db.deals.update_one(
                {'_id': ObjectId(deal_id) }, { '$set': { 'status': 'cancelled' } }, upsert=False)
            if statusUpdated:
                ob = {
                    'status': {
                        'success': 'true',
                        'code': 201,
                        'message': 'Deal Cancelled'
                    },
                }
            else:
                ob = {
                    'status': {
                        'success': 'false',
                        'code': 500,
                        'message': 'Deal Not Cancelled'
                    }
                }
        else:
            ob = {
                'status': {
                    'success': 'false',
                    'code': 401,
                    'message': 'Invalid Token'
                }
            }
        self.write(json_encode(ob))

class BuyerSettledDealsHandler(RequestHandler):
    @coroutine
    def post(self):
        token = self.request.headers['token']
        token_data = yield db.tokens.find_one({'token': token, 'type': 'business'})
        if token_data:
            org_id = token_data['user_id']
            cursor = db.deals.find({'buyer_id': org_id, 'status': 'settled'})
            deals_data = list()
            count = 0
            while(yield cursor.fetch_next):
                deal_data = cursor.next_object()
                deal_data['id'] = str(deal_data['_id'])
                del deal_data['_id']
                count += 1
                deals_data.append(deal_data)
            if deals_data:
                ob = {
                    'status': {
                        'success': 'true',
                        'code': 200,
                        'message': 'Settled Deals Found'
                    },
                    'response': {
                        'count': count,
                        'data': deals_data
                    }
                }
            else:
                ob = {
                    'status': {
                        'success': 'false',
                        'code': 404,
                        'message': 'No Settled Deals Found'
                    }
                }
        else:
            ob = {
                'status': {
                    'success': 'false',
                    'code': 401,
                    'message': 'Invalid Token'
                }
            }
        self.write(json_encode(ob))

class SellerSettledDealsHandler(RequestHandler):
    @coroutine
    def post(self):
        token = self.request.headers['token']
        token_data = yield db.tokens.find_one({'token': token, 'type': 'business'})
        if token_data:
            org_id = token_data['user_id']
            cursor = db.deals.find({'seller_id': org_id, 'status': 'settled'})
            deals_data = list()
            count = 0
            while(yield cursor.fetch_next):
                deal_data = cursor.next_object()
                deal_data['id'] = str(deal_data['_id'])
                del deal_data['_id']
                count += 1
                deals_data.append(deal_data)
            if deals_data:
                ob = {
                    'status': {
                        'success': 'true',
                        'code': 200,
                        'message': 'Settled Deals Found'
                    },
                    'response': {
                        'count': count,
                        'data': deals_data
                    }
                }
            else:
                ob = {
                    'status': {
                        'success': 'false',
                        'code': 404,
                        'message': 'No Settled Deals Found'
                    }
                }
        else:
            ob = {
                'status': {
                    'success': 'false',
                    'code': 401,
                    'message': 'Invalid Token'
                }
            }
        self.write(json_encode(ob))

class BuyerCancelledDealsHandler(RequestHandler):
    @coroutine
    def post(self):
        token = self.request.headers['token']
        token_data = yield db.tokens.find_one({'token': token, 'type': 'business'})
        if token_data:
            org_id = token_data['user_id']
            cursor = db.deals.find({'buyer_id': org_id, 'status': 'cancelled'})
            deals_data = list()
            count = 0
            while(yield cursor.fetch_next):
                deal_data = cursor.next_object()
                deal_data['id'] = str(deal_data['_id'])
                del deal_data['_id']
                count += 1
                deals_data.append(deal_data)
            if deals_data:
                ob = {
                    'status': {
                        'success': 'true',
                        'code': 200,
                        'message': 'Cancelled Deals Found'
                    },
                    'response': {
                        'count': count,
                        'data': deals_data
                    }
                }
            else:
                ob = {
                    'status': {
                        'success': 'false',
                        'code': 404,
                        'message': 'No Cancelled Deals Found'
                    }
                }
        else:
            ob = {
                'status': {
                    'success': 'false',
                    'code': 401,
                    'message': 'Invalid Token'
                }
            }
        self.write(json_encode(ob))

class SellerCancelledDealsHandler(RequestHandler):
    @coroutine
    def post(self):
        token = self.request.headers['token']
        token_data = yield db.tokens.find_one({'token': token, 'type': 'business'})
        if token_data:
            org_id = token_data['user_id']
            cursor = db.deals.find({'seller_id': org_id, 'status': 'cancelled'})
            deals_data = list()
            count = 0
            while(yield cursor.fetch_next):
                deal_data = cursor.next_object()
                deal_data['id'] = str(deal_data['_id'])
                del deal_data['_id']
                count += 1
                deals_data.append(deal_data)
            if deals_data:
                ob = {
                    'status': {
                        'success': 'true',
                        'code': 200,
                        'message': 'Cancelled Deals Found'
                    },
                    'response': {
                        'count': count,
                        'data': deals_data
                    }
                }
            else:
                ob = {
                    'status': {
                        'success': 'false',
                        'code': 404,
                        'message': 'No Cancelled Deals Found'
                    }
                }
        else:
            ob = {
                'status': {
                    'success': 'false',
                    'code': 401,
                    'message': 'Invalid Token'
                }
            }
        self.write(json_encode(ob))
