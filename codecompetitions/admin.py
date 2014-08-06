from django.contrib import admin

from .models import *

class LanguageAdmin(admin.ModelAdmin):
    readonly_fields = ("name","version","index")
    list_display = ("name","version","index")

class ProblemInline(admin.StackedInline):
    model = Problem
    extra = 0
    min_num = 1
    
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        ("More Settings", {
            'fields': ('description','time_limit'),
            'classes': ('collapse',)
        }),
        ("Input and Expected Output", {
            'fields': ('expected_output', 'input_data', 'read_from_file'),
            'classes': ('collapse',)
        }),
    )

class CompetitionAdmin(admin.ModelAdmin):
    exclude = ("start_time",)
    readonly_fields = ("paused_time_left",)

    filter_horizontal = ("judges","admins","limit_to")
    inlines = [ ProblemInline ]

    list_display = ("name","languages","date_created")
    list_filter = ("allowed_languages","date_created")
    search_fields = ("name","description")
    ordering = ("date_created",)

class ProblemAdmin(admin.ModelAdmin):
    list_display = ("name","competition")
    list_filter = ("competition","competition__date_created")
    search_fields = ("name","description")

class ExtraInline(admin.TabularInline):
    model = ExtraFile
    min_num = 0
    extra = 0

class RunAdmin(admin.ModelAdmin):
    list_display = ("problem","user","number","language")
    list_filter = ("is_a_test","language","has_been_run","exit_code",
                   "time_of_submission","judgement")
    ordering = ("problem","user","number")
    inlines = [ ExtraInline ]

admin.site.register(Language, LanguageAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(Run,RunAdmin)