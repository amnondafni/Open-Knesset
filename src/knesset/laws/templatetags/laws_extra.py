from django import template
from tagging.models import Tag, TaggedItem
from knesset.tagvotes.models import TagVote
from datetime import date, timedelta
from django.utils.translation import ugettext_lazy as _

register = template.Library()

@register.inclusion_tag('laws/_tag_vote.html')
def user_votes(user, vote, tag):
    ti = TaggedItem.objects.filter(tag=tag).filter(object_id=vote.id)[0]
    try:
        tv = TagVote.objects.filter(tagged_item=ti, user=user)[0]
        cv = tv.vote
    except Exception:
        cv = 0
    return {'user': user, 'vote':vote, 'tag':tag, 'current_vote_up':cv==1, 'current_vote_down':cv==-1}

@register.inclusion_tag('laws/_bar.html')
def bar(number, is_for):
    """ draws a bar to represent number of voters.
        number - number of people voted this way.
        is_for - is this a "for" bar. false means "against" bar.
    """
    width = round(number/1.2)
    return {'width': width, 'is_for':is_for}

@register.filter
def recent_discipline(m):
    d = date.today() - timedelta(30)
    return m.voting_statistics.discipline(d) or _('Not enough data')

@register.filter
def recent_coalition_discipline(m):
    d = date.today() - timedelta(30)
    return m.voting_statistics.coalition_discipline(d) or _('Not enough data')

@register.filter
def recent_votes_count(m):
    d = date.today() - timedelta(30)
    return m.voting_statistics.votes_count(d)
