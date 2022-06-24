from django.contrib import admin
from django.urls import path, include

from saving_plans_apps import views

urlpatterns = [
    path('create-user', views.create_user, name='create_user'),
    path('get-plans', views.get_plans, name='get_plans'),
    path('create-plan', views.create_plan, name='create-plan'),
    path('create-promotion', views.create_promotion, name='create-promotion'),
    path('get-promotion/<plan_id>', views.get_promotion, name='get_promotion'),
    path('create-customer-goal/<plan_id>/<user_id>', views.create_customer_goal, name='create-customer-goal'),
    path('get-customer-goal/<customer_goal_id>', views.get_customer_goal, name='get-customer-goal')
]
