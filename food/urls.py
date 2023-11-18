from django.urls import path
from food.views import all_foods,category_food,type_food,add_to_cart,cart,remove_from_cart,update_cart,check_out,place_order,orders,search,add_feedback

urlpatterns = [
    path('',all_foods,name='all_foods'),
    path("category/<int:cid>/",category_food,name="food_category"),
    path("types/<int:tid>/",type_food,name="food_type"),
    path("add_to_cart",add_to_cart, name="add_to_cart"),
    path("cart",cart, name="cart"),
    path("remove_from_cart/<int:id>/",remove_from_cart, name="remove_from_cart"),
    path("update_cart",update_cart, name="update_cart"),
    path("check_out/",check_out, name="check_out"),
    path("place_order/",place_order, name="place_order"),
    path("orders",orders,name="orders"),
    path("search",search,name="search"),
    path("add_feedback",add_feedback,name="add_feedback")
    
    # path("food_details/<int:fid>/",food_details,name="food_details")
]