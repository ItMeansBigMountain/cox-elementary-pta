
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import VolunteerInterestForm
from .models import Announcement, DonationCampaign, Event, NewsletterIssue, SiteSettings, Sponsor, VolunteerOpportunity

def get_settings():
    return SiteSettings.objects.first()

def active_announcements():
    today = timezone.localdate()
    return Announcement.objects.filter(
        published=True,
        publish_date__lte=today,
    ).filter(Q(expires_date__isnull=True) | Q(expires_date__gte=today))

def home(request):
    return render(request, 'pta/home.html', {
        'featured_events': Event.objects.filter(published=True, featured=True)[:5],
        'latest_newsletter': NewsletterIssue.objects.filter(published=True).first(),
        'opportunities': VolunteerOpportunity.objects.filter(active=True)[:3],
        'campaign': DonationCampaign.objects.filter(active=True).first(),
        'announcements': active_announcements()[:4],
    })

def newsletter(request):
    return render(request, 'pta/newsletter.html', {'issues': NewsletterIssue.objects.filter(published=True)})

def newsletter_detail(request, slug):
    return render(request, 'pta/newsletter_detail.html', {'issue': get_object_or_404(NewsletterIssue, slug=slug, published=True)})

def events(request):
    category=request.GET.get('category')
    qs=Event.objects.filter(published=True)
    if category: qs=qs.filter(category=category)
    return render(request, 'pta/events.html', {'events': qs, 'category': category, 'categories': Event.CATEGORY_CHOICES})

def event_detail(request, slug):
    return render(request, 'pta/event_detail.html', {'event': get_object_or_404(Event, slug=slug, published=True)})

def volunteer(request):
    if request.method == 'POST':
        form=VolunteerInterestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you — the PTA volunteer team received your interest form.')
            return redirect('pta:volunteer')
    else:
        form=VolunteerInterestForm()
    return render(request, 'pta/volunteer.html', {'opportunities': VolunteerOpportunity.objects.filter(active=True), 'form': form})

def resources(request):
    return render(request, 'pta/resources.html')

def fundraising(request):
    return render(request, 'pta/fundraising.html', {'campaign': DonationCampaign.objects.filter(active=True).first(), 'sponsors': Sponsor.objects.filter(active=True)})

def about_contact(request):
    return render(request, 'pta/about_contact.html')
