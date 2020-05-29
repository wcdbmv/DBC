from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.views import View
from json import dumps

from myblog.models.vote import Vote


class VoteView(LoginRequiredMixin, View):
    model = None
    vote_value = None

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        content_type = ContentType.objects.get_for_model(obj)
        try:
            vote = Vote.objects.get(content_type=content_type, object_id=obj.id, user=request.user)
            if vote.value is not self.vote_value:
                vote.value = self.vote_value
                vote.save(update_fields=['value'])
                obj.rating += 2 * vote.value
                obj.save(update_fields=['rating'])
                result = True
            else:
                obj.rating -= vote.value
                obj.save(update_fields=['rating'])
                vote.delete()
                result = False
        except Vote.DoesNotExist:
            obj.votes.create(user=request.user, value=self.vote_value)
            obj.rating += self.vote_value
            obj.save(update_fields=['rating'])
            result = True

        return HttpResponse(
            dumps({
                "result": result,
                "rating": obj.rating,
            }),
            content_type="application/json"
        )
