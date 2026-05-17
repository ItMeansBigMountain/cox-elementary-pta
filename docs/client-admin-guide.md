
# Cox Elementary PTA Client Admin Guide

## Login

Go to:

```text
https://YOUR-DOMAIN.com/admin/
```

Use the admin username/password provided during handoff.

## Weekly Update Workflow

1. Add or update **Newsletter Issues** first. The newest `Issue date` appears at the top of `/newsletter/`.
2. Add new **Events** with date, description, category, and flyer/CTA link.
3. Update **Volunteer Opportunities** and review **Volunteer Interests**.
4. Update **Donation Campaign** progress and Stripe Payment Link.
5. Add flyers/reminders as **Announcements**.

## Newsletter Ordering

The Newsletter page sorts automatically by `Issue date`, newest first.

## Stripe Donations

Use Stripe Dashboard → Payment Links → create or copy a Payment Link. Paste it into the active Donation Campaign's `Stripe payment link` field.

Do not collect card numbers inside the website.

## Domain Setup

For Render:

1. Open Render dashboard → the Cox PTA web service.
2. Go to Settings → Custom Domains.
3. Add `www.your-domain.com`.
4. Render shows a DNS target.
5. In the domain registrar, add a CNAME record:
   - Host: `www`
   - Value: Render's target
6. For the root domain, either:
   - add an ALIAS/ANAME record if registrar supports it, or
   - forward root domain to `www.your-domain.com`.
7. Wait for DNS propagation.
8. Enable HTTPS once Render verifies the domain.
