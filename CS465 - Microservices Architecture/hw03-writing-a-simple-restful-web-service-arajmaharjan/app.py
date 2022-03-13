from flask import Flask, abort, request, url_for
from datetime import datetime
from mongoengine import (
    connect,
    StringField,
    IntField,
    Document,
    DateTimeField, ValidationError
)
import os, json , dns , time

app = Flask(__name__)

mongo_db = os.getenv('DATABASE_NAME')
mongo_user = os.getenv('DATABASE_USER')
mongo_password = os.getenv('DATABASE_PASSWORD')
mongo_host = os.getenv('DATABASE_HOST')

connect(host=mongo_host,
        db=mongo_db,
        username=mongo_user,
        password=mongo_password)
        
class ActivityLog(Document):
    ID = StringField()
    user_id = IntField(required=True)
    username = StringField(required=True, max_length=64)
    timestamp = DateTimeField(default=datetime.utcnow)
    location = StringField(max_length=255)
    details = StringField(required=True)

@app.route("/api/activities", methods=["GET"])
def activities():
    acts = ActivityLog.objects.all().order_by("-timestamp").limit(10)
    act_logs = json.loads(acts.to_json())
    return {"activities": act_logs}

@app.route("/api/activities/<string:str_id>", methods=["GET"])
def activity(str_id):
	try:
		a = ActivityLog.objects.get(id=str_id)
		if not a:
			abort(404)
		return a.to_json()
	except ValidationError:
		abort(400)
		
@app.route('/api/activities', methods=["POST"])
def new_activity():
    sleep_time = os.getenv('SLEEP_TIME', default=0) 
    if not request.json:
        abort(400)
    new_activity_json = request.get_json()
    if (
        "username" not in new_activity_json
        or "details" not in new_activity_json
        or "user_id" not in new_activity_json
    ):
        abort(400)
    new_activity_mongo = ActivityLog(
        user_id=new_activity_json["user_id"],
        username=new_activity_json["username"],
        details=new_activity_json["details"],
		)
    new_activity_mongo.save()
    new_activity_json["location"] = url_for("activity", str_id=new_activity_mongo.id)
    new_activity_json["id"] = str(new_activity_mongo.id)
    new_activity_mongo.location = new_activity_json["location"]
    new_activity_mongo.save()
    time.sleep(int(sleep_time))
    return new_activity_json, 201