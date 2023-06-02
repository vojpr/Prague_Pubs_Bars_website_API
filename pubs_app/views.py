from django.views.generic import TemplateView, ListView
from django_filters.views import FilterView
from .filters import PubsBarsFilter
from .models import PubsBars
from .serializers import PubsBarsSerializer
from rest_framework import generics, mixins
from django.http import Http404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class IndexPageView(TemplateView):
    template_name = "pubs_app/index.html"


class PubsListView(FilterView):
    template_name = "pubs_app/pubsbars_list.html"
    model = PubsBars
    context_object_name = "pubs_list"
    paginate_by = 10
    filterset_class  = PubsBarsFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            querystring = self.request.GET.copy()
            if self.request.GET.get('page'):
                del querystring['page']
            context['querystring'] = querystring.urlencode()
        return context
    

# API views
# GET method with filtering option
class PubsGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = PubsBars.objects.all()
    serializer_class = PubsBarsSerializer
    lookup_field = "id"
    filterset_fields = ['beer_rating', 'outside_tables', 'foosball', 'overall_rating']

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            if self.list(request).data == []:
                raise Http404
            else:
                return self.list(request)


# POST PUT DELETE method with token authentication
class AuthPubsGenericAPIView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = PubsBars.objects.all()
    serializer_class = PubsBarsSerializer
    lookup_field = "id"

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return self.create(request)

    def put(self, request, id):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)
