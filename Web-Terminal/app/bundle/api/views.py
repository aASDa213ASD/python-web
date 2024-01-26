from .                  import api
from .models            import db, PhoneCall

from flask              import request
from flask_restful      import Resource, Api
from flask_jwt_extended import jwt_required
from app                import api_instance


class PhoneCallResource(Resource):
    @jwt_required()
    def get(self, phonecall_id):
        phonecall = PhoneCall.query.get_or_404(phonecall_id)
        return {"caller": phonecall.caller, "recipient": phonecall.recipient, "duration": phonecall.duration}

    @jwt_required()
    def put(self, phonecall_id):
        phonecall = PhoneCall.query.get_or_404(phonecall_id)
        data = request.get_json()
        phonecall.caller = data.get('caller', phonecall.caller)
        phonecall.recipient = data.get('recipient', phonecall.recipient)
        phonecall.duration = data.get('duration', phonecall.duration)
        db.session.commit()
        return {"message": "Phone call updated successfully"}

    @jwt_required()
    def delete(self, phonecall_id):
        phonecall = PhoneCall.query.get_or_404(phonecall_id)
        db.session.delete(phonecall)
        db.session.commit()
        return {"message": "Phone call deleted successfully"}


class PhoneCallListResource(Resource):
    @jwt_required()
    def get(self):
        phonecalls = PhoneCall.query.all()
        return [{"caller": p.caller, "recipient": p.recipient, "duration": p.duration} for p in phonecalls]

    @jwt_required()
    def post(self):
        data = request.get_json()
        new_phonecall = PhoneCall(**data)
        db.session.add(new_phonecall)
        db.session.commit()
        return {"message": "Phone call created successfully", "id": new_phonecall.id}


api_instance = Api(api)
api_instance.add_resource(PhoneCallListResource, '/phonecalls')
api_instance.add_resource(PhoneCallResource, '/phonecalls/<int:phonecall_id>')
