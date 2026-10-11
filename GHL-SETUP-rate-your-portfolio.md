# Rate Your Property Portfolio: GHL setup

How to set up `ipg-rate-your-portfolio.html` in GoHighLevel.

## 1. Funnel pages

Create a funnel called **Rate Your Property Portfolio** with these steps:

| Step | Path (example) | Content |
| --- | --- | --- |
| Landing + assessment | `/rate-your-portfolio` | One full-width section with a **Custom Code** element. Paste all of `ipg-rate-your-portfolio.html` into it. |
| Booking | `/portfolio-clarity-call` | Headline "Turn Your Rating Into Your Next Property Move", the call bullets from the blueprint, and the **Calendar** element. |
| Thank you | `/youre-booked` | "You're booked." copy from the blueprint. Set the calendar to redirect here after booking. |

Keep the landing page free of a header/menu. The assessment opens full-screen over the page, so nothing else on the page distracts the user.

## 2. Edit the CONFIG block

The `CONFIG` object is at the bottom of the snippet:

```js
WEBHOOK_URL: "https://services.leadconnectorhq.com/hooks/…",  // step 4
BOOKING_URL: "/portfolio-clarity-call",
PRIVACY_URL: "/privacy-policy",
LOGO_URL:    "https://…/ipg-logo-white.png",
```

## 3. Custom fields (Settings → Custom Fields → Contact)

| Field name | Type | Webhook key |
| --- | --- | --- |
| Portfolio Rating | Number | `portfolio_rating` |
| Investor Level | Single line | `investor_level` |
| Strategy Score | Number | `strategy_score` |
| Finance Score | Number | `finance_score` |
| Property Selection Score | Number | `property_selection_score` |
| Growth / Cash Flow Score | Number | `growth_cashflow_score` |
| Portfolio Management Score | Number | `portfolio_management_score` |
| Biggest Strength | Single line | `biggest_strength` |
| Biggest Weakness | Single line | `biggest_weakness` |
| Biggest Challenge | Multi line | `biggest_challenge` (comma-separated) |
| Rating Results URL | Single line | `results_url` |
| Scorecard Source | Single line | `scorecard_source` |
| Campaign | Single line | `campaign` |
| UTM Campaign | Single line | `utm_campaign` |
| Current Property Count | Number | collect on booking form |
| Purchase Timeline | Dropdown | collect on booking form |

The webhook also sends `q1` to `q12` (0, 1 or 2 points each), `answers` (all 12 as one string), `raw_points`, `utm_source/medium/content/term`, `fbclid` and `page_url`. Map any of these that you want to keep.

## 4. Workflow: "Rating Completed"

1. **Trigger:** Inbound Webhook. Copy its URL into `CONFIG.WEBHOOK_URL`, run one test submission on the live page, then click *Fetch sample request*.
2. **Create/Update Contact.** Map `first_name`, `email` and `phone`, plus every custom field in the table above.
3. **Add Tag.** Tag the contact with `Rating-Started` and `Rating-Completed`.
4. **If/Else on `investor_level`.** Add the matching tag: `Score-Foundation`, `Score-Emerging`, `Score-Strategic`, `Score-Advanced` or `Score-Architect`.
   (The webhook also sends the full tag list in `tags` if you'd rather split it in a Custom Code action.)
5. **If/Else on `biggest_challenge` contains…** Add the matching tag: `Challenge-Finance` (Borrowing capacity / Tax or ownership structure), `Challenge-Property` (Finding the right property / Knowing where to invest), `Challenge-Cashflow` (Cash flow), or `Challenge-Strategy` (all the others).
6. **Send Email** (immediately). Subject: `{{contact.first_name}}, your Property Portfolio Rating is {{contact.portfolio_rating}}/100`. Use the blueprint copy, and link "Review My Rating →" to `{{contact.rating_results_url}}`.
7. **Send SMS** (if phone is present). Use the blueprint copy with `{{contact.biggest_weakness}}` and `{{contact.rating_results_url}}`.
8. **Wait 1 day**, then send the Day 1 email. **Wait 2 days**, then send the Day 3 case-study email, branching on `biggest_weakness`.
9. **Goal event:** Appointment booked. This exits the workflow, so booked leads stop getting nurture emails.

Create a second workflow: **Appointment Booked** (calendar = 15-Minute Portfolio Clarity Call). It adds the tag `Rating-Booked` and removes `Rating-NoBooking`. In the first workflow, add `Rating-NoBooking` after the Day 3 email if the lead hasn't booked.

## 5. Calendar

- Name: **15-Minute Portfolio Clarity Call**, 15 min.
- Form fields: Name, Email, Mobile, Current properties owned, Approximate timeframe for next purchase (0-3 / 3-6 / 6-12 months / Researching).
- The results button opens the booking page with `first_name`, `email` and `phone` in the URL, so GHL pre-fills those fields.
- Confirmation: redirect to the thank-you page.

## 6. Meta Pixel / tracking

Add the Meta Pixel base code in the funnel's **Settings → Head tracking code**. The snippet fires these events automatically (and pushes the same names to `dataLayer` as `ipg_<name>` for GTM):

| Funnel event | Pixel event |
| --- | --- |
| Landing Page View | `LandingPageView` (custom) |
| Assessment Started | `AssessmentStarted` |
| 25% / 50% / 75% complete | `Assessment25` / `Assessment50` / `Assessment75` |
| Questions finished | `AssessmentCompleted` |
| Lead submitted | `Lead` (standard) |
| Results viewed | `ResultsViewed` (with `rating`, `level`) |
| Booking CTA clicked | `BookingClicked` |

Track "Appointment Booked" on the thank-you page with `fbq('track', 'Schedule')`.

## 7. Test checklist

- [ ] Run through all 12 questions on mobile. Previous works and the progress bar moves.
- [ ] The lead gate blocks submission when name or email is invalid.
- [ ] The contact appears in GHL with every field and tag filled.
- [ ] The results email arrives, and its link reopens the same results dashboard.
- [ ] The booking page opens with name, email and phone pre-filled.
- [ ] Pixel Helper shows the events listed above.
