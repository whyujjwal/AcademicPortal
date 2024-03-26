from django import template
from base.models import EvalMarks

register = template.Library()

@register.filter
def get_eval_mark(eval_marks, eval_id):
    try:
        student = eval_marks.first().student
        eval_mark = eval_marks.get(student=student, eval__id=eval_id)
        return eval_mark
    except (EvalMarks.DoesNotExist, AttributeError):
        return None