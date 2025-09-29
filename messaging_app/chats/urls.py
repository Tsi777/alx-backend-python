from rest_framework_nested import routers
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r'conversation', ConversationViewSet, basename='conversation')

convo_router = routers.NestedDefaultRouter(router, r'conversation', lookup='conversation')
convo_router.register(r'message', MessageViewSet, basename='conversation-message')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(convo_router.urls)),
]
