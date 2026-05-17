
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from pta.models import Announcement, Event, NewsletterIssue, VolunteerOpportunity, VolunteerInterest, DonationCampaign, SiteSettings, Sponsor
from django.utils import timezone
from datetime import date, timedelta

class PublicSiteBehaviorTests(TestCase):
    def setUp(self):
        self.client = Client()
        SiteSettings.objects.create(
            pta_name='Cox Elementary PTA',
            instagram_url='https://www.instagram.com/coxeagles_pta',
            linktree_url='https://linktr.ee/coxeaglespta',
            school_contact_url='https://cox.fvsd.us/apps/contact/',
        )

    def test_nav_order_is_home_newsletter_events_volunteer_then_other_pages(self):
        response = self.client.get(reverse('pta:home'))
        self.assertContains(response, 'Home')
        self.assertContains(response, 'Join PTA $15')
        html = response.content.decode()
        order = [html.index('>Home<'), html.index('>Newsletter<'), html.index('>Events<'), html.index('>Volunteer<')]
        self.assertEqual(order, sorted(order))

    def test_join_pta_page_uses_flat_membership_payment_link(self):
        settings = SiteSettings.objects.first()
        settings.membership_payment_link = 'https://buy.stripe.com/test_membership'
        settings.save()
        response = self.client.get(reverse('pta:join_pta'))
        self.assertContains(response, 'Join PTA')
        self.assertContains(response, '$15')
        self.assertContains(response, 'https://buy.stripe.com/test_membership')
        self.assertContains(response, 'No-pressure belonging')

    def test_newsletter_page_lists_latest_issue_first(self):
        NewsletterIssue.objects.create(title='September Newsletter', issue_date=date(2026, 9, 1), summary='Older news', published=True)
        NewsletterIssue.objects.create(title='October Newsletter', issue_date=date(2026, 10, 1), summary='Latest news', published=True)
        response = self.client.get(reverse('pta:newsletter'))
        html = response.content.decode()
        self.assertLess(html.index('October Newsletter'), html.index('September Newsletter'))

    def test_events_page_groups_events_by_month_and_collapses_past_months(self):
        today = timezone.localdate()
        current_month = today.replace(day=10)
        past_month = (today.replace(day=1) - timedelta(days=1)).replace(day=10)
        future_month = (today.replace(day=28) + timedelta(days=8)).replace(day=10)
        Event.objects.create(title='Past Family Night', slug='past-family-night', date=past_month, short_description='Already happened', published=True)
        Event.objects.create(title='This Month Book Fair', slug='this-month-book-fair', date=current_month, short_description='Coming soon', published=True)
        Event.objects.create(title='Future STEM Night', slug='future-stem-night', date=future_month, short_description='Later', published=True)

        response = self.client.get(reverse('pta:events'))
        html = response.content.decode()
        months = response.context['event_months']

        self.assertContains(response, 'events-accordion')
        self.assertContains(response, current_month.strftime('%B %Y'))
        self.assertContains(response, past_month.strftime('%B %Y'))
        self.assertContains(response, future_month.strftime('%B %Y'))
        self.assertContains(response, 'This month')
        self.assertContains(response, 'Past')
        current_group = next(group for group in months if group['is_current'])
        past_group = next(group for group in months if group['is_past'])
        self.assertTrue(current_group['is_open'])
        self.assertFalse(past_group['is_open'])
        self.assertIn(f'<details class="event-month reveal past-month ', html)

    def test_events_page_opens_first_future_month_when_current_has_no_events(self):
        today = timezone.localdate()
        past_month = (today.replace(day=1) - timedelta(days=1)).replace(day=10)
        future_month = (today.replace(day=28) + timedelta(days=8)).replace(day=10)
        Event.objects.create(title='Past Meeting', slug='past-meeting', date=past_month, short_description='Already happened', published=True)
        Event.objects.create(title='Next Book Fair', slug='next-book-fair', date=future_month, short_description='Coming soon', published=True)

        response = self.client.get(reverse('pta:events'))
        future_group = next(group for group in response.context['event_months'] if group['label'] == future_month.strftime('%B %Y'))
        self.assertTrue(future_group['is_open'])

    def test_announcements_show_on_homepage_not_newsletter_page(self):
        Announcement.objects.create(
            title='Jump for Jackets',
            kind='announcement',
            short_text='Bring a new jacket or sweater to participate.',
            publish_date=date.today(),
            published=True,
        )
        home_response = self.client.get(reverse('pta:home'))
        newsletter_response = self.client.get(reverse('pta:newsletter'))
        self.assertContains(home_response, 'Jump for Jackets')
        self.assertContains(home_response, 'Bring a new jacket or sweater')
        self.assertNotContains(newsletter_response, 'Jump for Jackets')

    def test_announcement_image_upload_uses_database_backed_src(self):
        image = SimpleUploadedFile('jump.png', b'fake image bytes', content_type='image/png')
        Announcement.objects.create(
            title='Jump for Jackets',
            kind='announcement',
            short_text='Bring a new jacket or sweater to participate.',
            image=image,
            publish_date=date.today(),
            published=True,
        )
        response = self.client.get(reverse('pta:home'))
        self.assertContains(response, 'src="data:image/png;base64,')
        self.assertNotContains(response, '/media/announcements/jump.png')

    def test_newsletter_cover_upload_uses_database_backed_src(self):
        image = SimpleUploadedFile('newsletter.png', b'fake newsletter bytes', content_type='image/png')
        newsletter = NewsletterIssue.objects.create(
            title='May Newsletter',
            issue_date=date.today(),
            summary='Growing Together',
            cover_image=image,
            published=True,
        )
        listing = self.client.get(reverse('pta:newsletter'))
        detail = self.client.get(newsletter.get_absolute_url())
        self.assertContains(listing, 'src="data:image/png;base64,')
        self.assertContains(detail, 'src="data:image/png;base64,')
        self.assertNotContains(listing, '/media/newsletters/covers/newsletter.png')
        self.assertNotContains(detail, '/media/newsletters/covers/newsletter.png')

    def test_announcement_has_share_and_print_pages_with_qr_codes(self):
        announcement = Announcement.objects.create(
            title='Jump for Jackets',
            kind='announcement',
            short_text='Bring a new jacket or sweater to participate.',
            publish_date=date.today(),
            published=True,
        )
        detail = self.client.get(announcement.get_absolute_url())
        printable = self.client.get(announcement.get_print_url())
        self.assertContains(detail, 'Printable flyer + QR')
        self.assertContains(detail, 'quickchart.io/qr')
        self.assertContains(printable, 'Print flyer')
        self.assertContains(printable, 'quickchart.io/qr')

    def test_volunteer_interest_form_creates_admin_reviewable_submission(self):
        opp = VolunteerOpportunity.objects.create(title='Book Fair Helper', slug='book-fair-helper', time_commitment='1 hour', description='Help students', active=True)
        response = self.client.get(reverse('pta:volunteer'))
        html = response.content.decode()
        self.assertIn('Book Fair Helper', html)
        self.assertNotIn('---------', html)
        response = self.client.post(reverse('pta:volunteer'), {
            'name': 'Jane Parent',
            'email': 'jane@example.com',
            'phone': '555-1212',
            'student_grade': '3rd',
            'opportunity': opp.id,
            'message': 'I can help Tuesday morning.',
        })
        self.assertEqual(response.status_code, 302)
        submission = VolunteerInterest.objects.get(email='jane@example.com')
        self.assertFalse(submission.reviewed)
        self.assertEqual(submission.opportunity, opp)

    def test_fundraising_page_uses_stripe_payment_link(self):
        DonationCampaign.objects.create(title='Fall Giving Campaign', goal_amount=10000, current_amount=6800, stripe_payment_link='https://buy.stripe.com/test_123', active=True)
        response = self.client.get(reverse('pta:fundraising'))
        self.assertContains(response, 'https://buy.stripe.com/test_123')
        self.assertContains(response, 'Donate with Stripe')

    def test_sponsor_logo_upload_uses_database_backed_src(self):
        DonationCampaign.objects.create(title='Fall Giving Campaign', goal_amount=10000, current_amount=6800, stripe_payment_link='https://buy.stripe.com/test_123', active=True)
        image = SimpleUploadedFile('sponsor.png', b'fake sponsor bytes', content_type='image/png')
        Sponsor.objects.create(name='Book Coastal Coffee Co', logo=image, website='https://example.com', level='Community Sponsor', active=True)
        response = self.client.get(reverse('pta:fundraising'))
        self.assertContains(response, 'Book Coastal Coffee Co')
        self.assertContains(response, 'src="data:image/png;base64,')
        self.assertNotContains(response, '/media/sponsors/sponsor.png')

    def test_existing_sponsor_logo_filename_renders_with_safe_fallback(self):
        Sponsor.objects.create(name='The Creative Ice Company', logo='sponsors/creativeice.png', website='https://thecreativeicecompany.com/', active=True)
        response = self.client.get(reverse('pta:fundraising'))
        self.assertContains(response, 'The Creative Ice Company')
        self.assertContains(response, 'src="/media/sponsors/creativeice.png"')
        self.assertContains(response, 'image-fallback')
