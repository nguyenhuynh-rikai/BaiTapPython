from django.contrib import admin
from .models import Student, StudentCard


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'slug')

    search_fields = ('name',)

    prepopulated_fields = {'slug': ('name',)}


admin.site.register(StudentCard)