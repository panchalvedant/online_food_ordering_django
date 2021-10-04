from django.urls import path
from delivery_boy import views
# for forget password
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('home/',views.home,name="home"),
    path('d_login/',views.d_login,name="logindeliveryboy"),
    path('d_signup/',views.d_signup,name="deliveryboysignup"), 
    path('profile_show/',views.profile_show,name="d_profile"), 
    path('update/',views.update,name="updateprofile_deliveryboy"), 
    path('logout_deliveryboy/',views.logout_deliveryboy,name="logout_deliveryboy"),
    path('change_password/',views.change_password,name="change_password"),
    path('delete_deliveryboy/',views.delete_deliveryboy,name="delete_deliveryboy"),
    
    path('update_order/<int:id>',views.update_order,name="update_order"),
    
    
    # forgot password
     # forget password
     path('resetpassword/', 
         auth_views.PasswordResetView.as_view(template_name='delivery_boy/forgetpassword.html'),
         name="reset_passwordreset_password"),
    
    path('resetpassworddone/', 
         auth_views.PasswordResetDoneView.as_view(template_name='delivery_boy/forgetpassword_confirm.html'),
         name="password_reset_done"),
    
    path('resetpasswordconfirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='delivery_boy/forgetpasswordreset.html'),
         name="password_reset_confirm"),
    
    path('resetpasswordchange/',
         auth_views.PasswordResetCompleteView.as_view(template_name='delivery_boy/forgetpasswordreset_confirmation.html'),
         name="password_reset_complete"),
   
 
]