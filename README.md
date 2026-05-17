# Cox Elementary PTA Website

This repo now contains two versions:

1. **Static preview** currently hosted by GitHub Pages from the root `index.html`/`events.html`/`volunteer.html` files.
2. **Dynamic Django version** for production client handoff with Django Admin, database-backed content, volunteer interest capture, newsletter pages, resources, fundraising, and Stripe donation links.

Live static preview:

```text
https://itmeansbigmountain.github.io/cox-elementary-pta/
```

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
- Newsletter issues sort newest-first by issue date.
- Events are created and managed from Django Admin.
- Volunteer opportunities are created and managed from Django Admin.
- Volunteer interest forms save submissions for admin review.
- Fundraising uses a Stripe Payment Link stored on the active Donation Campaign.
- Resources/social links are editable via Site Settings.

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

Open:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/admin/
```

## Tests

```bash
. .venv/bin/activate
python manage.py test
```

## Production Hosting

GitHub Pages cannot run Django. For the dynamic/admin version, deploy to Render, Railway, Fly.io, or PythonAnywhere.

Recommended: **Render**.

A starter `render.yaml` is included.

## Custom Domain

See:

```text
docs/client-admin-guide.md
```

Short version:

1. Deploy the Django app to Render.
2. Add the client domain in Render → Settings → Custom Domains.
3. Copy Render’s DNS record into the domain registrar.
4. Enable HTTPS after DNS verifies.

## Stripe Donation Setup

1. Create a Stripe Payment Link in the PTA/client Stripe dashboard.
2. Go to Django Admin → Donation Campaigns.
3. Paste the Stripe link into `Stripe payment link`.
4. Keep card processing on Stripe, not inside Django.

## Client Links

- Instagram: https://www.instagram.com/coxeagles_pta?igsh=NTc4MTIwNjQ2YQ%3D%3D
- PTA Linktree: https://linktr.ee/coxeaglespta?utm_source=qr_code&utm_medium=social&utm_content=link_in_bio&fbclid=PAdGRleAR2JhVleHRuA2FlbQIxMQBzcnRjBmFwcF9pZA8xMjQwMjQ1NzQyODc0MTQAAae1BgmXhU6iZCbfkE3M25e2aPKDtXPhVL9AY8M3pMgjL7N-2pX_VOuTQdXZUA_aem_P5UX-Hm-RUJpt8_7Ss4bQw
- Official Cox contact page: https://cox.fvsd.us/apps/contact/
