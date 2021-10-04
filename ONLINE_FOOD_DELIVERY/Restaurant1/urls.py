from django.urls import path
from Restaurant1 import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('home/',views.home,name="r_home"),
    path('r_login/',views.r_login,name="r_login"),
    path('r_signup/',views.r_signup,name="r_signup"), 
    path('profile/',views.profile_show,name="profile"), 
    
    # update restauarant profile
    path('update_rest/',views.update,name="updateprofile_rest"), 
    path('logout_rest/',views.logout_rest,name="logout_rest"),
    path('changingpassword/',views.changingpassword,name="changingpassword"),
    path('deleteAccount/',views.deleteaccount,name="delete_restaurant_account"),
    
    # inserting data
    path('additems/',views.add_items,name="additems"),
    
    # for showing all food items
    path('manageitems/',views.manageitems,name="manageitems"),
    
    # update items
    path('item_details/<int:id>/',views.itemdetails,name="item_details"),
    path('deleteitems/<int:id>/',views.deleteitems,name="deleteitems"),
    
    #update orders
   # path('status_Order/',views.status_update,name="status"),
    
    
    path('resetpassword/', 
         auth_views.PasswordResetView.as_view(template_name='Restaurant1/forgetpassword.html'),
         name="reset_password"),
    
    path('resetpassworddone/', 
         auth_views.PasswordResetDoneView.as_view(template_name='Restaurant1/forgetpassword_confirm.html'),
         name="password_reset_done"),
    
    path('resetpasswordconfirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='Restaurant1/forgetpasswordreset.html'),
         name="password_reset_confirm"),
    
    path('resetpasswordchange/',
         auth_views.PasswordResetCompleteView.as_view(template_name='Restaurant1/forgetpasswordreset_confirmation.html'),
         name="password_reset_complete"),
    
    
] 