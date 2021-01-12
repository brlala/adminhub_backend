import pytz
from bson import CodecOptions

from app.server.core.env_variables import local_config
from app.server.db.client import db
tzinfo = pytz.timezone(local_config.TIMEZONE)
codec_options = CodecOptions(tz_aware=True, tzinfo=tzinfo)

flow_collection = db.get_collection('flow', codec_options=codec_options)
portal_user_collection = db.get_collection('portal_user', codec_options=codec_options)
question_collection = db.get_collection('question', codec_options=codec_options)
bot_user_collection = db.get_collection('bot', codec_options=codec_options)
portal_user_group_collection = db.get_collection('portal_user_group', codec_options=codec_options)

# test
student_user_collection = db['students_collection']







