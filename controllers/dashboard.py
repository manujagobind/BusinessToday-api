from modules import *
from utilities import *

class BusinessDashboardHandler(RequestHandler):
    @coroutine
    def get(self):
        token = self.request.headers['token']
        token_data = yield db.tokens.find_one({'token': token, 'type': 'business'})
        if token_data:
            org_id = token_data['user_id']
            org_data = yield db.businesses.find_one({'_id': ObjectId(org_id)})
            org_data['id'] = str(org_data['_id'])
            del org_data['_id']
            del org_data['password']
            del org_data['salt']

            total_deals = yield db.deals.count({'buyer_id': org_id})
            active_requested = yield db.deals.count({'buyer_id': org_id, 'status': 'active'})
            active_received = yield db.deals.count({'seller_id': org_id, 'status': 'active'})
            settled_buyer = yield db.deals.count({'buyer_id': org_id, 'status': 'settled'})
            settled_seller = yield db.deals.count({'seller_id': org_id, 'status': 'settled'})
            cancelled_buyer = yield db.deals.count({'buyer_id': org_id, 'status': 'cancelled'})
            cancelled_seller = yield db.deals.count({'seller_id': org_id, 'status': 'cancelled'})

            ob = {
                'status': {
                    'success': 'true',
                    'code': 200,
                    'message': '',
                },
                'response': {
                    'org_data': org_data,
                    'total_deals': total_deals,
                    'deal_active_requested': active_requested,
                    'deal_active_received': active_received,
                    'deal_settled_buyer': settled_buyer,
                    'deal_settled_seller': settled_seller,
                    'deal_cancelled_buyer': cancelled_buyer,
                    'deal_cancelled_seller': cancelled_seller,
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
