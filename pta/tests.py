
from django.test import TestCase, Client
from django.urls import reverse
from pta.models import Event, NewsletterIssue, VolunteerOpportunity, VolunteerInterest, DonationCampaign, SiteSettings
from django.utils import timezone
from datetime import date

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
        html = response.content.decode()
        order = [html.index('>Home<'), html.index('>Newsletter<'), html.index('>Events<'), html.index('>Volunteer<')]
        self.assertEqual(order, sorted(order))

    def test_newsletter_page_lists_latest_issue_first(self):
        NewsletterIssue.objects.create(title='September Newsletter', issue_date=date(2026, 9, 1), summary='Older news', published=True)
        NewsletterIssue.objects.create(title='October Newsletter', issue_date=date(2026, 10, 1), summary='Latest news', published=True)
        response = self.client.get(reverse('pta:newsletter'))
        html = response.content.decode()
        self.assertLess(html.index('October Newsletter'), html.index('September Newsletter'))

    def test_volunteer_interest_form_creates_admin_reviewable_submission(self):
        opp = VolunteerOpportunity.objects.create(title='Book Fair Helper', slug='book-fair-helper', time_commitment='1 hour', description='Help students', active=True)
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
