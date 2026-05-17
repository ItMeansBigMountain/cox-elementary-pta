
from django.contrib import admin
from .models import Announcement, DonationCampaign, Event, NewsletterIssue, SiteSettings, Sponsor, VolunteerInterest, VolunteerOpportunity

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ('pta_name','school_name','tagline','hero_message','contact_email')}),('Links', {'fields': ('instagram_url','linktree_url','school_contact_url','lunch_menu_url','attendance_url','spirit_wear_url','calendar_url')}),('Images', {'fields': ('logo','mascot')}))

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display=('title','date','category','published','featured')
    list_filter=('category','published','featured')
    search_fields=('title','short_description','description')
    prepopulated_fields={'slug':('title',)}
    date_hierarchy='date'

@admin.register(VolunteerOpportunity)
class VolunteerOpportunityAdmin(admin.ModelAdmin):
    list_display=('title','committee','time_commitment','active','sort_order')
    list_filter=('active','committee')
    search_fields=('title','description','committee')
    prepopulated_fields={'slug':('title',)}

@admin.register(VolunteerInterest)
class VolunteerInterestAdmin(admin.ModelAdmin):
    list_display=('name','email','opportunity','reviewed','created_at')
    list_filter=('reviewed','opportunity','created_at')
    search_fields=('name','email','phone','message')
    actions=['mark_reviewed']
    @admin.action(description='Mark selected submissions reviewed')
    def mark_reviewed(self, request, queryset): queryset.update(reviewed=True)

@admin.register(NewsletterIssue)
class NewsletterIssueAdmin(admin.ModelAdmin):
    list_display=('title','issue_date','published','featured')
    list_filter=('published','featured','issue_date')
    search_fields=('title','summary')
    prepopulated_fields={'slug':('title',)}
    date_hierarchy='issue_date'

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display=('title','kind','publish_date','expires_date','published')
    list_filter=('kind','published','publish_date')
    search_fields=('title','short_text')

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display=('name','level','active')
    list_filter=('level','active')
    search_fields=('name',)

@admin.register(DonationCampaign)
class DonationCampaignAdmin(admin.ModelAdmin):
    list_display=('title','current_amount','goal_amount','progress_percent','active')
    list_filter=('active',)
