from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),



    #     path('user-account/', views.manageble_account, name='manageble_account'),
    path('user-properties/', views.properties_page, name='properties_page'),
    path('property-details/<property_id>',
         views.property_details_page, name='property_details'),
    path('edit-property-page/<property_id>',
         views.edit_property_page, name='edit_property_page'),

    path('complaints', views.complaints,
         name='complaints'),
    path('voilations/', views.voilations,
         name='voilations'),
    path('property-search', views.property_search_page,
         name='property_search_page'),

    #     path('create-contact', views.create_contact_form,
    #          name='create-contact-form'),
    #     path('contact/<pk>/', views.contact_detail, name="detail-contact"),
    #     path('delete-additional-contact/<pk>/',
    #          views.delete_additional_contact, name="delete-additional-contact"),


    path('user-is-pro', views.already_pro, name='pro_user'),
    # path('become-pro-member', views.become_pro, name='become_pro'),
    path('forgot-password/', views.ForgetPassword, name="forget_password"),
    path('password-reset-verification/<auth_token>/',
         views.ChangePassword, name="change_password"),

    path('login-attempt', views.login_attempt, name='login'),
    path('verify/<auth_token>', views.verify, name='verify'),
    path('logout-attempt', views.logout_attempt, name='logout'),
    path('register-attempt', views.register, name='register'),
    path('my_webhook', views.stripe_webhook),
    path('ourapp-pricing', views.princing, name='price'),
    path('adding-property', views.add_property, name='addproperty'),
    path('edit-property/<property_id>',
         views.edit_property, name='edit_property'),
    path('add-property', views.add_properties,
         name='add_property'),
    path('delete_street_property/<int:pro_id>',
         views.delete_street_property, name='delete_street_property'),

    # path('property/<int:pros_id>/edit/',
    #      views.update_property, name='update_property'),

    # path('checkout-confirmation', views.checking_out, name='checking_out'),
    # path('create_checkout_session', views.create_checkout_session, name='checkout'),
    # path('create_checkout_session/<str:membership>/<int:amount>', views.create_checkout_session, name='checkout'),
    path('membership-process', views.become_pro, name='pro'),
    path('success/paid', views.success_second, name='success_2'),
    path('success', views.success, name='success'),
    path('cancel', views.cancel, name='cancel'),
    path('twenty-plus-properties', views.twenty_plus, name='twenty_plus'),
    path('contact-us', views.contact, name='contact'),
    path('contacting', views.contact_process, name="contacting"),
    #     path('about-us', views.about, name="about"),
    #     path('runcsv', views.creating_cleared_data, name='runcsv'),
]
