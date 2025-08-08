from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from backend.models.course_progress_model import CompletionStatus

class CourseProgressSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(require=True)
    course_id = fields.Int(require=True)
    completion_status = EnumField(CompletionStatus, by_value=True)
    updated_at = fields.DateTime(dump_only=True)