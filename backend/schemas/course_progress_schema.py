from marshmallow import Schema, fields, EXCLUDE, post_load, validate
from marshmallow_enum import EnumField
from models.course_progress_model import CourseProgress, CompletionStatus

class CourseProgressSchema(Schema):
    class Meta: 
        unknown = EXCLUDE
        
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    course_id = fields.Int(required=True)
    completion_status = fields.Str(
                        validate=validate.OneOf(["not_started", "in_progress", "completed"]),
                        load_default="not_started" # Defaults to NOT_STARTED
                        )
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_load
    def make_course_progress(self, data, **kwargs):
        return CourseProgress(**data)