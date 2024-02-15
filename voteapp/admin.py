from typing import Any
from django.contrib import admin
from django import forms
from django.utils import timezone
from datetime import timedelta
from django.utils.translation import gettext_lazy as _
from voteapp.models import Position, Passcode, AspirantListStudent, ElectionTime

# Register your models here.
class PasscodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'passcode', 'user', 'is_used']
    readonly_fields = ['passcode']
    search_fields = ['passcode', 'user__fullname', 'is_used']

admin.site.register(Passcode, PasscodeAdmin)

class PositionAdmin(admin.ModelAdmin):
    list_display = ['id' , 'asociate_number' , 'title', 'total_vote']
    search_fields = ['title', 'asociate_number']
    prepopulated_fields = {'slug' : ('title',) }

admin.site.register(Position, PositionAdmin)

@admin.register(AspirantListStudent)
class AspirantListStudentAdmin(admin.ModelAdmin):
    list_display = ['matric_number', 'get_fullname', 'get_level', 'get_department', 'position', 'total_vote']
    list_filter = ['matric_number', 'total_vote', 'position']

    def get_fullname(self, obj):
        return obj.student.fullname if obj.student else ""
    
    def position(self, obj):
        return obj.position.title if obj.position else ""
    
    def get_level(self, obj):
        return obj.student.level if obj.student else ""

    def get_department(self, obj):
        return obj.student.department if obj.student else "" 

    get_fullname.short_description = 'Full Name'
    # get_position.short_description = 'Position'
    get_level.short_description = 'Level'
    get_department.short_description = 'department'


@admin.register(ElectionTime)
class ElectionTimeAdmin(admin.ModelAdmin):
    list_display = ['election_datetime', 'duration']
    list_filter = ['election_datetime']
    search_fields = ['election_datetime']

    # def save_model(self, request, obj, form, change):
    #     if obj.election_datetime < timezone.now():
    #         raise forms.ValidationError("Election date and time cannot be in the past.")
    
    #     obj.save()
