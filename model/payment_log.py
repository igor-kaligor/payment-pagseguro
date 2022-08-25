from settings.database import db


class PaymentLog(db.Model):
    __tablename__ = 'payments_log'
    id = db.Column(db.Integer, primary_key=True)
    id_payment = db.Column(db.String())
    payment_request = db.Column(db.Text())
    payment_request_return = db.Column(db.Text())
    id_purchase = db.Column(db.Integer())
    id_client = db.Column(db.Integer())
    date = db.Column(db.DateTime())
    http_status_code = db.Column(db.Integer())
    solicitation_status = db.Column(db.Integer())
    payment_request_user_return = db.Column(db.Text())
    start_request_date = db.Column(db.DateTime())
    finish_request_date = db.Column(db.DateTime())
    request_duration_time = db.Column(db.String())

    def to_obj(self, data):
        self.id_payment = data['id_payment']
        self.payment_request = data['payment_request']
        self.payment_request_return = data['payment_request_return']
        self.id_purchase = data['id_purchase']
        self.id_client = data['id_client']
        self.date = data['date']
        self.http_status_code = data['http_status_code']
        self.solicitation_status = data['solicitation_status']
        self.payment_request_user_return = data['payment_request_user_return']
        self.start_request_date = data['start_request_date']
        self.finish_request_date = data['finish_request_date']
        self.request_duration_time = data['request_duration_time']

    @staticmethod
    def to_json(data):

        r = {
            'id': data.id,
            'id_payment': data.id_payment,
            'payment_request': data.payment_request,
            'payment_request_return': data.payment_request_return,
            'id_purchase': data.id_purchase,
            'id_client': data.id_client,
            'date': data.date,
            'http_status_code': data.http_status_code,
            'solicitation_status': data.solicitation_status,
            'payment_request_user_return': data.payment_request_user_return,
            'start_request_date': data.start_request_date,
            'finish_request_date': data.finish_request_date,
            'request_duration_time': data.request_duration_time
        }

        return r
    
