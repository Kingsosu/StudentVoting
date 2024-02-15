from django import template

register = template.Library()


@register.filter(name="has_voted")
def has_voted(user, candidates):
    return candidates.student_voters.filter(id=user.id).exists()

@register.filter(name="has_voted_for_candidate")
def has_voted_for_candidate(user, candidates):
    return candidates.student_voters.filter(id=user.id).exists()