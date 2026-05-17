
from datetime import date
from django.core.files import File
from django.core.management.base import BaseCommand
from pathlib import Path
from pta.models import Announcement, DonationCampaign, Event, NewsletterIssue, SiteSettings, VolunteerOpportunity

class Command(BaseCommand):
    help = 'Seed Cox Elementary PTA starter content for client handoff.'

    def handle(self, *args, **options):
        settings, _ = SiteSettings.objects.get_or_create(pk=1)
        settings.pta_name = 'Cox Elementary PTA'
        settings.school_name = 'Cox Elementary School'
        settings.instagram_url = 'https://www.instagram.com/coxeagles_pta?igsh=NTc4MTIwNjQ2YQ%3D%3D'
        settings.linktree_url = 'https://linktr.ee/coxeaglespta?utm_source=qr_code&utm_medium=social&utm_content=link_in_bio&fbclid=PAdGRleAR2JhVleHRuA2FlbQIxMQBzcnRjBmFwcF9pZA8xMjQwMjQ1NzQyODc0MTQAAae1BgmXhU6iZCbfkE3M25e2aPKDtXPhVL9AY8M3pMgjL7N-2pX_VOuTQdXZUA_aem_P5UX-Hm-RUJpt8_7Ss4bQw'
        settings.school_contact_url = 'https://cox.fvsd.us/apps/contact/'
        settings.save()
        events = [
            ('Book Fair Week','book-fair-week',date(2026,9,18),'family','Browse books, wish lists, and volunteer shifts all week.'),
            ('Family STEM Night','family-stem-night',date(2026,10,3),'family','Hands-on experiments, robotics demos, and family stations.'),
            ('Cox Spirit Day','cox-spirit-day',date(2026,10,10),'spirit','Wear Cox colors and show eagle pride across campus.'),
            ('PTA General Meeting','pta-general-meeting',date(2026,10,14),'pta','Meet the board, review plans, and share ideas.'),
            ('Dine-Out Fundraiser','dine-out-fundraiser',date(2026,10,22),'fundraiser','Enjoy dinner while supporting student programs.'),
        ]
        for title,slug,when,cat,short in events:
            Event.objects.update_or_create(slug=slug, defaults={'title':title,'date':when,'category':cat,'short_description':short,'description':short,'published':True,'featured':True})
        for order, (title, slug, time, desc) in enumerate([
            ('Event Check-In','event-check-in','20–30 min','Greet families, scan signups, hand out name tags, and help events start smoothly.'),
            ('Book Fair Helper','book-fair-helper','1 hour','Assist students with wish lists, restock tables, and support checkout lines.'),
            ('Hospitality Committee','hospitality-committee','Flexible','Coordinate snacks, appreciation notes, and celebrations for teachers and staff.'),
            ('Newsletter + Flyers','newsletter-flyers','At home','Help format announcements, collect photos, and keep the newsletter hub fresh.'),
        ]):
            VolunteerOpportunity.objects.update_or_create(slug=slug, defaults={'title':title,'time_commitment':time,'description':desc,'active':True,'sort_order':order})
        NewsletterIssue.objects.update_or_create(slug='september-2026-newsletter', defaults={'title':'September 2026 Newsletter','issue_date':date(2026,9,1),'summary':'Back-to-school updates, PTA reminders, membership drive, and upcoming events.','published':True,'featured':True})
        Announcement.objects.update_or_create(title='Membership Drive Begins', defaults={'kind':'announcement','short_text':'Joining supports programs, events, classroom resources, and enrichment — no volunteering required.','publish_date':date(2026,9,1),'published':True})
        DonationCampaign.objects.update_or_create(title='Fall Giving Campaign', defaults={'goal_amount':10000,'current_amount':6800,'description':'Funds support classroom supplies, family events, student enrichment, teacher appreciation, and campus improvements. Replace this test Stripe URL with the PTA Stripe Payment Link before launch.','stripe_payment_link':'https://buy.stripe.com/test_123','active':True})
        self.stdout.write(self.style.SUCCESS('Seeded Cox Elementary PTA starter content.'))
