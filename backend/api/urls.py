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
    path('addpayments/',addpayments.as_view(), name="payment" ),
    path('reports/monthly-revenue/', monthly_revenue_report, name='monthly-revenue-report'),
    path('reports/monthly-tax/', monthly_tax_report, name='monthly-revenue-report'),
    path('reports/passenger/', Passengers_report, name='monthly-revenue-report'),
    path('reports/vehicles/pdf/', vehicle_report_pdf, name='vehicle-report-pdf'),
    path('driver_payments/',driver_payments.as_view(), name="payment" ),
    path('routeView/',routes.as_view(), name="route" ),
    path('route/<int:pk>',detailRoutes.as_view(), name="detail_route" ),
    path('getUser/<int:phonenumber>',getuser.as_view(), name="get_user" ),
    path('sub_travels/<int:rid>',sub_travels.as_view(), name="sub_travel" ),
    path('user/change-password/', PasswordChangeView.as_view(), name='change-password'),
    path('report/',report.as_view(), name="report" ),
    path('recent/',recent.as_view(), name="recent" ),
    path('users/<int:id>/', UserDeactivateAPIView.as_view(), name='user-deactivate'),
    path('pay/<int:id>/',payDriver.as_view(), name='user-deactivate'),
    path('exit-slips/', ExitSlipListCreateView.as_view(), name='exit-slip-list'),
    path('exit-slips/<int:pk>/', ExitSlipDetailView.as_view(), name='exit-slip-detail'),
    path('driver_recent/<int:uid>',driver_recent.as_view(), name="recent driver" ),
    path('level/',levels.as_view(), name="level" ),
    path('vehicles/',vehicles.as_view(), name="vehicle" ),
    path('driver_vehicle/<int:did>',driver_vehicle.as_view(), name="vehicle" ),
    path('tickets/',tickets.as_view(), name="buyticket" ),
    path('ticket/',buyticket.as_view(), name="buyticket" ),
    path('vehicle/<int:pk>',vehiclesDetail.as_view(), name="location" ),
    path('add_vehicle/<int:bid>',VehicleViewSet.as_view(), name="vehicle add" ),
    path('branchdetail/<int:pk>',branchDetail.as_view(), name="branch" ),
    path('stafflist/<int:bid>',staffListAD.as_view(), name="staff list admin" ),
    path('addtraveller/',addtraveller.as_view(), name="add traveller" ),
    path('staffdetail/<int:pk>',userDetail.as_view(), name="staff detail admin" ),
    path('subadmin_dashboard/', sub_dashboard.as_view(), name = "subadmin_dashboard"),
    path('ad_notif/<int:id>', ad_notif.as_view(),name = "admin notification"),
    path('messages/', messages_Add.as_view(),name = "admin notification"),
    path('messages/<int:id>', messages.as_view(),name = "admin notification"),
    path('api/messages/mark_read/', MarkMessagesReadView.as_view(), name='mark-messages-read'),
    path('api/messages/mark_conversation_read/<int:sender_id>/', MarkConversationReadView.as_view(), name='mark-conversation-read'),
    path('ad_notifs/<int:pk>', ad_editnotif.as_view(),name = "edit  notification"),
    path('route/', sub_route.as_view(),name = "sub route"),
    path('delete/', delete, name = "delete"),
    path("nid/<int:pn>",phone_number_search.as_view(),name="phone_number search" ),
    path("othercred/",other_cred.as_view(),name="FAN search" ),
    path('nids/<int:fan>',Fan_search.as_view(),name="FAN search" ),
     
    path('payment/', payment_form, name='payment_form'),
    path('payment/callback/', payment_callback, name='payment_callback'),
    path('next/', success_page, name='success_page'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)