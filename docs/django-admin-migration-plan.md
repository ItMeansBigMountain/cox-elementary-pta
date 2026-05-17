# Cox Elementary PTA Django Admin Migration Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Convert the current static GitHub Pages PTA website into a client-editable Django website with an admin panel, dynamic Events/Volunteer/Newsletter content, lead capture, donation links, and custom domain support.

**Architecture:** Use Django as the backend and CMS-like admin. Public pages render from database objects managed through Django Admin. Keep the current visual design as templates/static assets, but split homepage, events, volunteer, newsletter, resources, and contact into professional standalone pages. Deploy on a free/low-cost Python host such as Render, Railway, or Fly.io; GitHub Pages cannot run Django.

**Tech Stack:** Django 5.x, SQLite for MVP or PostgreSQL for production, Django Admin, WhiteNoise for static files, Gunicorn, optional S3/Cloudinary for uploaded newsletter/flyer images, Stripe Payment Links or PayPal for donations.

---

## Key Decision

GitHub Pages is only for static HTML/CSS/JS. It cannot run Django, process forms, store admin-created objects, or receive volunteer interest submissions.

Recommended path:

1. Keep GitHub as the code repository.
2. Move hosting from GitHub Pages to Render or Railway for Django.
3. Use Django Admin for client updates.
4. Use the purchased domain with the Django host instead of GitHub Pages.
5. Optionally keep the current GitHub Pages URL as a temporary preview/archive.

---

## Content Model

### Pages and Objects

- `SiteSettings`
  - school name
  - PTA name
  - logo/mascot images
  - Instagram URL
  - Linktree URL
  - school contact URL
  - donation URL
  - contact email
  - homepage announcement

- `Event`
  - title
  - slug
  - date
  - end date optional
  - category: Book Fair, STEM, PTA Meeting, Spirit Day, Fundraiser, Teacher Appreciation, Other
  - short description
  - full description
  - flyer image/PDF
  - CTA label
  - CTA URL
  - published boolean
  - featured boolean

- `VolunteerOpportunity`
  - title
  - slug
  - time commitment
  - committee/category
  - description
  - active boolean
  - sort order

- `VolunteerInterest`
  - parent/guardian name
  - email
  - phone optional
  - student grade optional
  - opportunity selected
  - message
  - created timestamp
  - reviewed boolean

- `NewsletterIssue`
  - title
  - month
  - school year
  - cover image
  - PDF/file URL or upload
  - summary
  - published boolean
  - featured boolean

- `Announcement` / `Flyer`
  - title
  - type: announcement, flyer, fundraiser, spirit wear, reminder
  - image/PDF
  - short text
  - CTA URL
  - publish date
  - expires date optional
  - published boolean

- `Sponsor`
  - name
  - logo
  - website
  - level
  - active boolean

- `DonationCampaign`
  - title
  - goal amount
  - current amount manually editable or synced later
  - description
  - payment URL
  - active boolean

---

## Public Pages

### Home

- Hero with CTA buttons
- Quick links driven by `SiteSettings`
- Featured events from `Event(featured=True)`
- Featured newsletter from `NewsletterIssue(featured=True)`
- Volunteer spotlight from active `VolunteerOpportunity`
- Fundraising campaign from active `DonationCampaign`
- Student spotlight/announcements from `Announcement`

### Events

- Standalone `/events/` page
- List and calendar-style cards from `Event`
- Category filters
- Event detail page `/events/<slug>/`

### Volunteer

- Standalone `/volunteer/` page
- Active volunteer opportunities
- Interest form creates `VolunteerInterest`
- Admin can view, filter, export, mark reviewed
- Optional email notification to PTA contact

### Newsletter

- New standalone `/newsletter/` page
- Grid/list of `NewsletterIssue`
- Newsletter detail pages
- Flyer/announcement hub separated from homepage

### Fundraising / Donate

- Standalone `/fundraising/` page
- Current campaign progress
- Sponsor highlights
- Donation button links to Stripe Payment Link, PayPal, Givebutter, MemberHub, or PTA-approved payment platform
- Important: do not store credit cards in Django; use payment provider checkout.

### Contact / Resources

- Standalone `/resources/` or `/contact/`
- Instagram, Linktree, official school contact page, lunch menu, attendance, etc.

---

## Implementation Tasks

### Task 1: Create Django project scaffold

**Objective:** Add Django app structure without deleting current static site.

**Files:**
- Create: `manage.py`
- Create: `coxpta/settings.py`
- Create: `coxpta/urls.py`
- Create: `pta/models.py`
- Create: `pta/admin.py`
- Create: `pta/views.py`
- Create: `pta/urls.py`
- Create: `templates/`
- Create: `static/`
- Create: `requirements.txt`

**Verification:**

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python manage.py check
python manage.py runserver
```

Expected: Django starts locally.

### Task 2: Create content models

**Objective:** Define the database objects the client will manage.

**Files:**
- Modify: `pta/models.py`
- Modify: `pta/admin.py`

**Verification:**

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Expected: Client-editable objects appear in Django Admin.

### Task 3: Port current design into Django templates

**Objective:** Reuse the current design while making content dynamic.

**Files:**
- Create: `templates/base.html`
- Create: `templates/pta/home.html`
- Create: `templates/pta/events.html`
- Create: `templates/pta/event_detail.html`
- Create: `templates/pta/volunteer.html`
- Create: `templates/pta/newsletter.html`
- Create: `templates/pta/newsletter_detail.html`
- Create: `templates/pta/fundraising.html`
- Move/copy: `styles.css` to `static/css/styles.css`
- Move/copy: `script.js` to `static/js/script.js`
- Move/copy: `assets/` to `static/assets/`

**Verification:**

Public pages render with current design and real database content.

### Task 4: Add newsletter page

**Objective:** Make newsletter a professional standalone page rather than a home-only section.

**Behavior:**
- `/newsletter/` lists newsletter issues.
- `/newsletter/<slug>/` shows details and download/view link.
- Homepage only shows latest/featured newsletter preview.

**Verification:**

Create two newsletter issues in admin and verify both appear on `/newsletter/`.

### Task 5: Add volunteer interest capture

**Objective:** Let parents submit interest forms and let admin review responses.

**Files:**
- Create: `pta/forms.py`
- Modify: `pta/views.py`
- Modify: `templates/pta/volunteer.html`
- Modify: `pta/admin.py`

**Behavior:**
- Parent submits volunteer form.
- Django saves `VolunteerInterest`.
- Admin can see submissions.
- Optional email notification sends to PTA email.

**Verification:**

Submit test form, confirm database/admin record appears.

### Task 6: Add donation flow

**Objective:** Capture donation intent safely without handling credit cards directly.

**Recommended MVP:**
Use a Stripe Payment Link, PayPal, Givebutter, or existing PTA payment URL stored in `DonationCampaign.payment_url`.

**Behavior:**
- Donation buttons point to external checkout.
- Admin can update campaign title, goal, current amount, description, and payment URL.

**Verification:**

Donation button opens configured payment provider link.

### Task 7: Deploy Django

**Recommended host:** Render.

**Files:**
- Create: `render.yaml` or deployment docs
- Create: `Procfile` if needed
- Modify: `requirements.txt`
- Modify: `coxpta/settings.py` for env vars

**Required env vars:**
- `SECRET_KEY`
- `DEBUG=False`
- `ALLOWED_HOSTS`
- `DATABASE_URL` if using PostgreSQL

**Verification:**

Render app URL loads homepage, admin login works, static assets load.

### Task 8: Attach custom domain

**Objective:** Point the client’s purchased domain to the Django host.

**Steps depend on host. Render example:**
1. Render dashboard → Web Service → Settings → Custom Domains.
2. Add `www.clientdomain.com`.
3. Render gives DNS records.
4. In domain registrar, add CNAME for `www` pointing to Render target.
5. For root domain, use registrar forwarding to `www` or host-supported ALIAS/ANAME record.
6. Wait for DNS propagation.
7. Enable HTTPS in Render.

**Verification:**

- `https://www.clientdomain.com` loads the Django site.
- SSL certificate is active.
- Admin at `https://www.clientdomain.com/admin/` works.

---

## Recommended MVP Scope

Build first:

1. Django Admin
2. Events CRUD
3. Volunteer Opportunities CRUD
4. Volunteer Interest capture
5. Newsletter page/issues CRUD
6. Fundraising campaign with external donation link
7. Site settings/social links
8. Render deployment + custom domain

Avoid for MVP:

- Custom-built admin UI outside Django Admin
- Processing credit cards directly
- Complex calendar integrations
- Parent accounts/logins
- Automated payment reconciliation

---

## Client Handoff

Provide:

- Admin URL
- Admin username/password delivery securely
- 1-page guide: how to add events, newsletters, flyers, volunteer opportunities
- Backup/export instructions
- Who receives volunteer interest notifications
- Donation provider login stays with PTA/client, not the website developer
