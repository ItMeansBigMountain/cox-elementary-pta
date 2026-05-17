# Cox Elementary PTA Website

A modern, mobile-first, client-editable PTA website for **Cox Elementary PTA**.

The site is built to help parents quickly understand what is happening, volunteer with low friction, read newsletters, share announcements, print flyers with QR codes, and manage content through a simple admin panel.

## Live Links

Production website:

```text
https://cox-elementary-pta.onrender.com/
```

Admin panel:

```text
https://cox-elementary-pta.onrender.com/admin/
```

Render dashboard:

```text
https://dashboard.render.com/
```

GitHub repo:

```text
https://github.com/ItMeansBigMountain/cox-elementary-pta
```

## How the Infrastructure Works

```text
AI / developer updates code
        ↓
GitHub stores the code
        ↓
Render watches GitHub main branch
        ↓
Render builds and deploys the Django website
        ↓
Website runs online with a Django Admin panel
        ↓
Client updates weekly content through /admin/
```

Plain English version:

1. Code changes are made on a computer or with AI assistance.
2. The code is pushed to GitHub.
3. Render automatically sees the GitHub update.
4. Render rebuilds and redeploys the website.
5. The public website updates after a few minutes.
6. The admin panel remains the place for client content updates.

## Accounts / Services Needed

To fully operate the site, the project needs:

- **GitHub account** — stores the website code and triggers deployments.
- **Render account** — runs the live Django website and database.
- **Stripe account** — used later for fundraising/payment links.
- **Domain registrar account** — used later when attaching the custom domain.

## Current Deployment Setup

The production site is a Django app hosted on Render.

Render runs:

- the Python/Django web app
- the production database connection
- static assets via WhiteNoise
- automatic deployments from GitHub

The included `render.yaml` defines the Render service and database connection.

GitHub Pages is **not** the production host for the dynamic site because GitHub Pages cannot run Django, Python, databases, forms, or an admin panel.

## How to Update Website Code

Use this workflow for design, feature, or code changes:

1. Change the code locally or using AI services.
2. Test the change.
3. Commit the change.
4. Push to GitHub `main`.
5. Render automatically deploys the newest GitHub code.
6. Wait a few minutes.
7. Refresh the website:

```text
https://cox-elementary-pta.onrender.com/
```

## How to Update Website Content

Use the admin panel for normal PTA updates:

```text
https://cox-elementary-pta.onrender.com/admin/
```

The admin panel can manage:

- announcements and homepage flyers
- newsletters
- events
- volunteer opportunities
- volunteer interest submissions
- resources and links
- fundraising campaigns and Stripe Payment Links
- PTA membership fee and membership Payment Link
- site settings/contact links

Client/admin users should use `/admin/` for weekly updates instead of editing code.

## Dynamic Django Features

- Admin panel at `/admin/`
- Navbar order: Home, Newsletter, Events, Volunteer, Resources, Fundraising, About & Contact
- Standalone pages:
  - `/newsletter/`
  - `/events/`
  - `/volunteer/`
  - `/resources/`
  - `/fundraising/`
  - `/about-contact/`
- Homepage announcements managed through admin
- $15 Join PTA page with an admin-editable membership Payment Link
- Announcement detail pages with QR sharing
- Printable flyer pages for announcements
- Newsletters sorted newest-first by date
- Newsletter images stored with a database-backed fallback for Render Free
- Announcement images stored with a database-backed fallback for Render Free
- Events managed from Django Admin
- Volunteer opportunities managed from Django Admin
- Volunteer interest forms saved for admin review
- Admin dashboard shows unreviewed volunteer interest count
- Fundraising uses Stripe Payment Links stored in the admin
- Resources/social links are editable through Site Settings

## Render Free Image Upload Note

Render Free uses an ephemeral filesystem. That means files uploaded through Django Admin can disappear after a redeploy or restart if the site depends only on `/media/...` files.

To avoid broken images on the current free setup, uploaded **announcement images** and **newsletter cover images** are copied into the database as a fallback and rendered from the database on public pages.

If an old image is already showing only its alt text, re-upload it once through the admin panel after this fix is deployed.

For a more permanent client-ready media setup later, use one of these:

- Cloudinary
- Supabase Storage
- AWS S3 or compatible object storage
- Render paid persistent disk

## Local Django Development

```bash
uv venv .venv
. .venv/bin/activate
uv pip install -r requirements.txt
python manage.py migrate
python manage.py seed_initial_content
python manage.py createsuperuser
python manage.py runserver
```

Open locally:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/admin/
```

## Tests

```bash
. .venv/bin/activate
python manage.py test
```

Current behavior covered by tests includes:

- navigation order
- newsletter newest-first ordering
- homepage announcements
- database-backed announcement images
- database-backed newsletter cover images
- QR/print announcement pages
- volunteer form submissions
- Stripe Payment Link rendering

## Custom Domain Later

Do this after the Render site is fully approved:

1. Open Render dashboard.
2. Go to the `cox-elementary-pta` web service.
3. Add the custom domain under Render settings/custom domains.
4. Copy Render’s DNS instructions exactly.
5. Add those DNS records at the domain registrar.
6. Wait for DNS/HTTPS verification.
7. Add the final domain to Django `ALLOWED_HOSTS` / trusted origins if needed.

## Stripe Donation Setup Later

1. Create a Stripe account for the PTA/client.
2. Create a Stripe Payment Link in Stripe.
3. Go to Django Admin → Donation Campaigns.
4. Paste the Stripe Payment Link into `Stripe payment link`.
5. Keep credit-card processing inside Stripe, not inside Django.

## Client Links

- Instagram: https://www.instagram.com/coxeagles_pta?igsh=NTc4MTIwNjQ2YQ%3D%3D
- PTA Linktree: https://linktr.ee/coxeaglespta?utm_source=qr_code&utm_medium=social&utm_content=link_in_bio&fbclid=PAdGRleAR2JhVleHRuA2FlbQIxMQBzcnRjBmFwcF9pZA8xMjQwMjQ1NzQyODc0MTQAAae1BgmXhU6iZCbfkE3M25e2aPKDtXPhVL9AY8M3pMgjL7N-2pX_VOuTQdXZUA_aem_P5UX-Hm-RUJpt8_7Ss4bQw
- Official Cox contact page: https://cox.fvsd.us/apps/contact/
