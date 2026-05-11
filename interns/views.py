from rest_framework import viewsets
from .models import Interns
from .serializers import InternSerializer

class InternsViewSet(viewsets.ModelViewSet):

    queryset = Interns.objects.all()
    serializer_class = InternSerializer