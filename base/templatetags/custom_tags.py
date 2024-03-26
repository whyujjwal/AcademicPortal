from django import template
from ..models import EvalMarks


register = template.Library()

@register.filter
def get_eval_mark(eval_marks, eval_id):
    try:
        student = eval_marks.first().enrollment.student
        return eval_marks.get(enrollment__student=student, eval_id=eval_id)
    except (EvalMarks.DoesNotExist, AttributeError):
        return None