from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static
from .views import *
urlpatterns = [
    path('branch/',branchs.as_view(), name="branch" ),
    path('staffs/',Staffs.as_view(), name="staffs" ),
    path('passengers/',usertravel.as_view(), name="passengers" ),
    path('driver/',driver.as_view(), name="driver" ),
    path('payments/',payments.as_view(), name="payment" ),
    path('driver_payments/',driver_payments.as_view(), name="payment" ),
    path('route/',routes_sub.as_view(), name="route_sub" ),
    path('routeView/',routes.as_view(), name="route" ),
    path('route/<int:pk>',detailRoutes.as_view(), name="detail_route" ),
    path('getUser/<int:phonenumber>',getuser.as_view(), name="get_user" ),
    path('sub_travels/<int:rid>',sub_travels.as_view(), name="sub_travel" ),
    path('user/change-password/', PasswordChangeView.as_view(), name='change-password'),
    path('report/',report.as_view(), name="report" ),
    path('level/',levels.as_view(), name="level" ),
    path('vehicles/',vehicles.as_view(), name="vehicle" ),
    path('buyticket/<int:bid>',buyticket.as_view(), name="buyticket" ),
    path('vehicle/<int:pk>',vehiclesDetail.as_view(), name="location" ),
    path('branchdetail/<int:pk>',branchDetail.as_view(), name="branch" ),
    path('stafflist/<int:bid>',staffListAD.as_view(), name="staff list admin" ),
    path('addtraveller/',addtraveller.as_view(), name="add traveller" ),
    path('staffdetail/<int:pk>',userDetail.as_view(), name="staff detail admin" ),
    path('subadmin_dashboard/', sub_dashboard.as_view(), name = "subadmin_dashboard"),
    path('ad_notif/<int:id>', ad_notif.as_view(),name = "admin notification"),
    path('messages/<int:id>', messages.as_view(),name = "admin notification"),
    path('ad_notifs/<int:pk>', ad_editnotif.as_view(),name = "edit  notification"),
    path('route/', sub_route.as_view(),name = "sub route"),
    path('delete/', delete, name = "delete"),
    path("nid/<int:pn>",phone_number_search.as_view(),name="phone_number search" ),
    path("othercred/",other_cred.as_view(),name="FAN search" ),
    path("nids/<int:fan>",Fan_search.as_view(),name="FAN search" )
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)