from django.contrib import admin

# Register your models here.
from django.contrib import admin
from food.models import Category,Food,Type,Order,Feedback

# Register your models here.

class FoodAdmin(admin.ModelAdmin):
    list_display =('name','category','price','is_available')
    search_fields=('name',)
    list_filter = ("counter", )

class TypeAdmin(admin.ModelAdmin):
    list_display =('type',)
    search_fields=('type',)
    list_filter = ('type', )

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'food','counter','quantity','status')
    search_fields = ('user','food' )
    list_editable = ('status', )
    list_filter = ('status','counter')

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'food', 'rating','comment')
    list_filter = ('rating','food',)
    search_fields = ('user','food','comment' )

admin.site.register(Category)
admin.site.register(Food,FoodAdmin)
admin.site.register(Type,TypeAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Feedback,FeedbackAdmin)

