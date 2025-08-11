from marshmallow import Schema, fields, EXCLUDE, post_load
from marshmallow_enum import EnumField
from models.course_progress_model import CourseProgress, CompletionStatus

class CourseProgressSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    course_id = fields.Int(required=True)
    completion_status = EnumField(
                        CompletionStatus, 
                        by_value=True, 
                        missing=CompletionStatus.NOT_STARTED
                        )
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    class Meta: 
        unknown = EXCLUDE

    @post_load
    def make_course_progress(self, data, **kwargs):
        return CourseProgress(**data)