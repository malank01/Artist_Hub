from django.contrib import admin
from  .models import User,Artist,Contacts,Transaction,Booking
# Register your models here.


admin.site.register(User)
admin.site.register(Artist)
admin.site.register(Contacts)
admin.site.register(Transaction)
admin.site.register(Booking)
