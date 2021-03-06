from django.conf.urls import url
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from cw3.views import WorkspaceApi, WorkspaceElementApi, CodeApi

# urlpatterns = [
#     url(r'^$', views.index, name='index'),
#     url(r'^getWorkspace$', views.get_workspace, name='getWorkspace'),
# ]

# router = routers.SimpleRouter()
# router.register(r'workspace', WorkspaceApi, base_name='create')
# urlpatterns = router.urls
#
# router = routers.DefaultRouter()
#
# # register REST API endpoints with DRF router
# router.register(r'getWorkspace', WorkspaceApi, r"getWorkspace")
# router.register(r'workspaceItem', WorkspaceElementApi, r"workspaceItem")
# router.register(r'code', CodeApi, r"code")
router = routers.SimpleRouter()

urlpatterns = [
    url(r'^getWorkspace/', WorkspaceApi.as_view()),
    url(r'^workspaceItem/', WorkspaceElementApi.as_view()),
    url(r'^code/', CodeApi.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += router.urls
