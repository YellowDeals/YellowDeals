"""
URL configuration for YellowDeals project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from YellowDealsAPP import views as view_se
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view_se.home, name='home'),
    path('admin_dashboard/', view_se.admin_dashboard, name='admin_dashboard'),
    path('admin_ManageRequests/', view_se.admin_ManageRequests, name='admin_ManageRequests'),
    path('admin_complaints/', view_se.admin_complaints, name='admin_complaints'),
    path('admin_shops/', view_se.admin_shops, name='admin_shops'),
    path('admin_review_shop/<str:store_owner_id>', view_se.admin_review_shop, name='admin_review_shop'),
    path('ban_shop/<str:store_id>/', view_se.ban_shop, name='ban_shop'),
    path('unban_shop/<str:store_id>/', view_se.unban_shop, name='unban_shop'),
    path('admin_edit/', view_se.admin_edit, name='admin_edit'),
    path('approve_store/<str:store_id>/', view_se.approve_store, name='approve_store'),
    path('reject_store/<str:store_id>/', view_se.reject_store, name='reject_store'),
    path('admin_store_detail/<str:store_id>/', view_se.admin_store_detail, name='admin_store_detail'),
    path('admin_profile/edit/', view_se.admin_profile, name='admin_profile'),
    path('admin_profile_view/', view_se.admin_profile_view, name='admin_profile_view'),
    path('product/<str:product_id>/', view_se.product_detail, name='product_detail'),
    path('product/<str:product_id>/toggle_save/', view_se.toggle_save_product, name='toggle_save_product'),
    path('saved_products_view', view_se.saved_products_view, name='saved_products'),
    path('saved/remove/<int:saved_id>/', view_se.remove_saved_product, name='remove_saved_product'),
    path('submit_complaint/', view_se.submit_complaint_view, name='submit_complaint'),
    path('complaints/<int:complaint_id>/', view_se.complaint_detail, name='complaint_detail'),

    # เพิ่มข้อมูล
    path('add_complaint/', view_se.add_complaint, name='add_complaint'),
    path('add_typeproduct/', view_se.add_typeproduct, name='add_typeproduct'),
    path('add_store/', view_se.add_store, name='add_store'),
    path('add_category/', view_se.add_category, name='add_category'),

    # แก้ไขข้อมูล
    path('edit_complaint/<int:pk>/', view_se.edit_complaint, name='edit_complaint'),
    path('edit_typeproduct/<int:pk>/', view_se.edit_typeproduct, name='edit_typeproduct'),
    path('edit_store/<str:pk>/', view_se.edit_store, name='edit_store'),
    path('edit_category/<int:pk>/', view_se.edit_category, name='edit_category'),
    path('edit_store_location/<str:store_id>/', view_se.edit_store_location, name='edit_store_location'),

    # ลบข้อมูล
    path('delete_complaint/<int:pk>/', view_se.delete_complaint, name='delete_complaint'),
    path('delete_typeproduct/<int:pk>/', view_se.delete_typeproduct, name='delete_typeproduct'),
    path('delete_store/<str:pk>/', view_se.delete_store, name='delete_store'),
    path('delete_category/<int:pk>/', view_se.delete_category, name='delete_category'),

    # Auth
    path('login/', view_se.login_view, name='login'),
    path('logout/', view_se.logout_view, name='logout'),
    path('register/', view_se.register_view, name='register'),
    path('registershop/', view_se.register_shop_view, name='registershop'),
    path('admin_register/', view_se.admin_register_view, name='admin_register'),
    path('admin-secret/', view_se.admin_secret_view, name='admin_secret'),

    # Reset password
    path('password_reset/', view_se.password_reset_request, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', view_se.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'), name='password_reset_complete'),

    # ฝั่งร้านค้า
    path('store_dashboard/', view_se.store_dashboard, name='store_dashboard'),
    path('store_manage_product/', view_se.store_manage_product, name='store_manage_product'),
    path('manage_products', view_se.manage_products, name='manage_products'),
    path('store_reports/', view_se.store_reports, name='store_reports'),
    path('product/toggle_hidden/<str:pk>/', view_se.toggle_hidden, name='toggle_hidden'),
    path('store_reports/export/', view_se.export_product_report, name='export_product_report'),
    path('store_about/', view_se.store_about, name='store_about'),

    # เพิ่ม/แก้ไข/ลบสินค้า
    path('add_product/', view_se.add_product, name='add_product'),
    path('delete_product/<str:pk>/', view_se.delete_product, name='delete_product'),
    path('edit_product/<str:pk>/', view_se.edit_product, name='edit_product'),
    path('store_delete_account/', view_se.store_delete_account, name='store_delete_account'),
    path('store_profile_edit/', view_se.store_profile_edit, name='store_profile_edit'),
]

# รองรับ media (เวลา DEBUG)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


