
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class SiteSettings(TimeStampedModel):
    pta_name = models.CharField(max_length=120, default='Cox Elementary PTA')
    school_name = models.CharField(max_length=120, default='Cox Elementary School')
    tagline = models.CharField(max_length=180, default='Building Community, Supporting Students, Strengthening Our School')
    hero_message = models.TextField(default='A warm, organized hub for events, newsletters, volunteer opportunities, fundraising, and family resources.')
    contact_email = models.EmailField(default='pta@coxelementary.org')
    instagram_url = models.URLField(blank=True)
    linktree_url = models.URLField(blank=True)
    school_contact_url = models.URLField(blank=True)
    lunch_menu_url = models.URLField(blank=True)
    attendance_url = models.URLField(blank=True)
    spirit_wear_url = models.URLField(blank=True)
    calendar_url = models.URLField(blank=True)
    logo = models.ImageField(upload_to='site/', blank=True)
    mascot = models.ImageField(upload_to='site/', blank=True)
    def __str__(self): return self.pta_name
    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

class Event(TimeStampedModel):
    CATEGORY_CHOICES = [('family','Family Event'),('pta','PTA Meeting'),('fundraiser','Fundraiser'),('spirit','Spirit Day'),('appreciation','Teacher Appreciation'),('other','Other')]
    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True, blank=True)
    date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='family')
    short_description = models.CharField(max_length=240, blank=True)
    description = models.TextField(blank=True)
    flyer = models.FileField(upload_to='events/', blank=True)
    cta_label = models.CharField(max_length=80, blank=True, default='Learn more')
    cta_url = models.URLField(blank=True)
    published = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    class Meta:
        ordering = ['date', 'title']
    def save(self,*args,**kwargs):
        if not self.slug: self.slug = slugify(self.title)
        super().save(*args,**kwargs)
    def get_absolute_url(self): return reverse('pta:event_detail', args=[self.slug])
    def __str__(self): return f'{self.date:%b %-d} — {self.title}'

class VolunteerOpportunity(TimeStampedModel):
    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True, blank=True)
    time_commitment = models.CharField(max_length=80, blank=True)
    committee = models.CharField(max_length=120, blank=True)
    description = models.TextField()
    active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['sort_order','title']
        verbose_name_plural = 'Volunteer opportunities'
    def save(self,*args,**kwargs):
        if not self.slug: self.slug = slugify(self.title)
        super().save(*args,**kwargs)
    def __str__(self): return self.title

class VolunteerInterest(TimeStampedModel):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    student_grade = models.CharField(max_length=40, blank=True)
    opportunity = models.ForeignKey(VolunteerOpportunity, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField(blank=True)
    reviewed = models.BooleanField(default=False)
    class Meta:
        ordering = ['-created_at']
    def __str__(self): return f'{self.name} — {self.email}'

class NewsletterIssue(TimeStampedModel):
    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True, blank=True)
    issue_date = models.DateField(help_text='Used for ordering. Latest appears first.')
    summary = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='newsletters/covers/', blank=True)
    pdf = models.FileField(upload_to='newsletters/files/', blank=True)
    external_url = models.URLField(blank=True)
    published = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    class Meta:
        ordering = ['-issue_date','-created_at']
    def save(self,*args,**kwargs):
        if not self.slug: self.slug = slugify(self.title)
        super().save(*args,**kwargs)
    def get_absolute_url(self): return reverse('pta:newsletter_detail', args=[self.slug])
    def __str__(self): return self.title

class Announcement(TimeStampedModel):
    TYPE_CHOICES=[('announcement','Announcement'),('flyer','Flyer'),('fundraiser','Fundraiser'),('spirit','Spirit Wear'),('reminder','Reminder')]
    title=models.CharField(max_length=160)
    kind=models.CharField(max_length=20, choices=TYPE_CHOICES, default='announcement')
    short_text=models.TextField(blank=True)
    image=models.ImageField(upload_to='announcements/', blank=True)
    file=models.FileField(upload_to='announcements/files/', blank=True)
    cta_url=models.URLField(blank=True)
    publish_date=models.DateField()
    expires_date=models.DateField(blank=True,null=True)
    published=models.BooleanField(default=True)
    class Meta:
        ordering=['-publish_date','title']
    def __str__(self): return self.title

class Sponsor(TimeStampedModel):
    name=models.CharField(max_length=160)
    logo=models.ImageField(upload_to='sponsors/', blank=True)
    website=models.URLField(blank=True)
    level=models.CharField(max_length=80, blank=True)
    active=models.BooleanField(default=True)
    def __str__(self): return self.name

class DonationCampaign(TimeStampedModel):
    title=models.CharField(max_length=160)
    goal_amount=models.PositiveIntegerField(validators=[MinValueValidator(1)])
    current_amount=models.PositiveIntegerField(default=0)
    description=models.TextField(blank=True)
    stripe_payment_link=models.URLField(help_text='Use a Stripe Payment Link, e.g. https://buy.stripe.com/...')
    active=models.BooleanField(default=True)
    def clean(self):
        if self.stripe_payment_link and not (self.stripe_payment_link.startswith('https://buy.stripe.com/') or self.stripe_payment_link.startswith('https://checkout.stripe.com/')):
            raise ValidationError({'stripe_payment_link':'Use a Stripe Payment Link beginning with https://buy.stripe.com/ or https://checkout.stripe.com/.'})
    @property
    def progress_percent(self):
        return min(100, round((self.current_amount / self.goal_amount) * 100)) if self.goal_amount else 0
    def __str__(self): return self.title
