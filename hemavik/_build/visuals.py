"""Illustrative product screens, one per service. Built in HTML/CSS so they stay
sharp at any size and follow the brand tokens. All figures are examples."""


def window(title, body, label, cls=""):
    return f"""<div class="mock {cls}" role="img" aria-label="{label}">
  <div class="mock-bar"><i></i><i></i><i></i><span>{title}</span></div>
  <div class="mock-body">{body}</div>
</div>"""


def stars(n=5):
    return f'<span class="stars" aria-hidden="true">{"★" * n}{"☆" * (5 - n)}</span>'


V = {}

V["crm-automation"] = window("Pipeline · Sales", """
<div class="kanban">
  <div class="kcol"><p>New lead <b>4</b></p>
    <div class="kcard"><strong>Mehta Realty</strong><span>₹48,000</span><em>Meta ad</em></div>
    <div class="kcard"><strong>Bloom Salon</strong><span>₹22,500</span><em>Website</em></div>
    <div class="kcard ghost"></div>
  </div>
  <div class="kcol"><p>Qualified <b>3</b></p>
    <div class="kcard hot"><strong>Aarav Dental</strong><span>₹65,000</span><em>Google ad</em></div>
    <div class="kcard"><strong>Nova Fitness</strong><span>₹30,000</span><em>WhatsApp</em></div>
  </div>
  <div class="kcol"><p>Booked <b>2</b></p>
    <div class="kcard won"><strong>Sharma &amp; Co</strong><span>₹90,000</span><em>Voice AI</em></div>
  </div>
</div>""", "Example CRM pipeline with deals moving from new lead to booked")

V["google-meta-ads"] = window("Campaigns · Last 30 days", """
<div class="ads-kpis">
  <div><small>Leads</small><b>214</b></div>
  <div><small>Cost / lead</small><b>₹312</b></div>
  <div><small>Booked</small><b>63</b></div>
</div>
<div class="bars" aria-hidden="true">
  <span style="--h:38%"></span><span style="--h:52%"></span><span style="--h:45%"></span><span style="--h:61%"></span>
  <span style="--h:58%"></span><span style="--h:72%"></span><span style="--h:69%"></span><span style="--h:84%"></span>
</div>
<div class="ads-rows">
  <div><i class="pf pf-g">G</i><span>Search · Dental implants</span><b>₹284</b></div>
  <div><i class="pf pf-m">M</i><span>Lead form · Free consult</span><b>₹331</b></div>
  <div><i class="pf pf-y">YT</i><span>Retargeting · Video</span><b>₹356</b></div>
</div>""", "Example ad dashboard showing leads, cost per lead and campaigns")

V["voice-ai"] = f"""<div class="mock phone" role="img" aria-label="Example Voice AI call booking an appointment">
  <div class="phone-top"><span class="dot-live"></span>AI Receptionist · on call <b>01:42</b></div>
  <div class="wave" aria-hidden="true">{"".join(f'<span style="--d:{(i * 7) % 10 / 10}s"></span>' for i in range(28))}</div>
  <div class="bubbles">
    <p class="b-in">Hi, can I book a cleaning for Thursday?</p>
    <p class="b-out">Of course. I have 11:30 or 4:00 free on Thursday. Which suits you?</p>
    <p class="b-in">11:30, please.</p>
    <p class="b-ok">Booked · Thu 11:30 · SMS confirmation sent</p>
  </div>
</div>"""

V["conversational-ai"] = """<div class="mock phone chat" role="img" aria-label="Example WhatsApp AI chat agent answering and booking">
  <div class="phone-top"><span class="avatar">H</span>Assistant · WhatsApp <b>online</b></div>
  <div class="bubbles">
    <p class="b-in">Do you do teeth whitening? How much?</p>
    <p class="b-out">Yes! In-clinic whitening starts at ₹6,500 and takes about an hour. Would you like to book a consultation?</p>
    <div class="quick"><span>Book a visit</span><span>See all prices</span></div>
    <p class="b-in">Book a visit</p>
    <p class="b-out">Great. Saturday 10:00 or Monday 17:30?</p>
  </div>
</div>"""

V["marketing-automation"] = window("Journey · New lead nurture", """
<div class="flowmap">
  <div class="fm-node trig"><small>Trigger</small>Form submitted</div>
  <div class="fm-line"></div>
  <div class="fm-node"><small>Email</small>Welcome + guide</div>
  <div class="fm-line"></div>
  <div class="fm-node wait"><small>Wait</small>1 day</div>
  <div class="fm-line"></div>
  <div class="fm-node cond"><small>If</small>Email opened?</div>
  <div class="fm-split">
    <div><span class="fm-tag">Yes</span><div class="fm-node"><small>WhatsApp</small>Book your call</div></div>
    <div><span class="fm-tag no">No</span><div class="fm-node"><small>SMS</small>Gentle reminder</div></div>
  </div>
</div>""", "Example marketing automation journey with email, wait, condition and WhatsApp steps")

V["appointment-automation"] = window("Calendar · This week", """
<div class="cal">
  <span></span><b>Mon</b><b>Tue</b><b>Wed</b><b>Thu</b><b>Fri</b>
  <em>09</em><i></i><i class="bk">Rahul K.</i><i></i><i></i><i class="bk">Neha P.</i>
  <em>10</em><i class="bk">Anita R.</i><i></i><i class="bk alt">Group class</i><i></i><i></i>
  <em>11</em><i></i><i class="bk">Vikram S.</i><i class="bk alt">Group class</i><i class="bk new">AI booked</i><i></i>
  <em>12</em><i class="bk">Sara M.</i><i></i><i></i><i class="bk">Imran A.</i><i class="bk">Dev T.</i>
</div>
<div class="toast-mock"><span class="dot-live"></span>Reminder sent to Rahul K. on WhatsApp</div>""", "Example booking calendar with appointments and an automatic reminder")

V["website-development"] = """<div class="mock-site" role="img" aria-label="Example website on desktop and mobile">
  <div class="mock browser">
    <div class="mock-bar"><i></i><i></i><i></i><span class="url">yourbusiness.com</span></div>
    <div class="mock-body site">
      <div class="s-nav"><b></b><span></span><span></span><span></span><em></em></div>
      <div class="s-hero"><div><b></b><b class="short"></b><span></span><span></span><em>Book now</em></div><div class="s-img"></div></div>
      <div class="s-cards"><div></div><div></div><div></div></div>
    </div>
  </div>
  <div class="mock mobile">
    <div class="s-img sm"></div><b></b><b class="short"></b><span></span><em>Book now</em>
  </div>
</div>"""

V["commerce-memberships"] = window("Checkout · Growth Programme", """
<div class="shop">
  <div class="pay">
    <small>Monthly membership</small>
    <strong>₹4,999<span>/month</span></strong>
    <ul><li>12 video modules</li><li>Private community</li><li>Live Q&amp;A every week</li></ul>
    <div class="paym"><span>Card</span><span>UPI</span><span>Wallet</span></div>
    <em>Pay securely</em>
  </div>
  <div class="course">
    <small>Your progress</small>
    <b>Module 3 of 8</b>
    <div class="prog"><span style="width:38%"></span></div>
    <p>Lesson: Building your first funnel</p>
    <p class="done">Community: 3 new posts</p>
  </div>
</div>""", "Example checkout page and course progress for a membership")

V["ai-workflows"] = window("Workflow · Invoice processing", """
<div class="graph">
  <div class="gnode"><i>IN</i><span>New invoice email<small>trigger</small></span></div>
  <div class="gline"></div>
  <div class="gnode ai"><i>AI</i><span>Extract vendor, amount, due date<small>98% confidence</small></span></div>
  <div class="gline"></div>
  <div class="gsplit">
    <div class="gnode"><i>ACC</i><span>Create bill<small>accounting</small></span></div>
    <div class="gnode"><i>MSG</i><span>Notify finance<small>team chat</small></span></div>
  </div>
</div>
<div class="runlog"><span class="dot-live"></span>Run #1,284 completed in 3.1 s</div>""", "Example AI workflow that reads invoices and updates accounting")

V["digital-marketing"] = window("Content calendar · October", """
<div class="ccal">
  <b>Mon</b><b>Tue</b><b>Wed</b><b>Thu</b><b>Fri</b><b>Sat</b><b>Sun</b>
  <i><em class="ig">Reel</em></i><i></i><i><em class="bl">Blog</em></i><i><em class="li">Post</em></i><i></i><i><em class="ig">Story</em></i><i></i>
  <i></i><i><em class="gb">GBP</em></i><i><em class="ig">Reel</em></i><i></i><i><em class="nl">Email</em></i><i></i><i><em class="li">Post</em></i>
</div>
<div class="spark">
  <small>Organic visits</small><b>+38%</b>
  <svg viewBox="0 0 200 50" preserveAspectRatio="none" aria-hidden="true"><path d="M0 44 L25 40 L50 41 L75 33 L100 34 L125 26 L150 22 L175 15 L200 8 L200 50 L0 50Z" class="sp-area"/><path d="M0 44 L25 40 L50 41 L75 33 L100 34 L125 26 L150 22 L175 15 L200 8" class="sp-line"/></svg>
</div>""", "Example content calendar and organic traffic trend")

V["reputation-management"] = window("Reviews · Google & Facebook", f"""
<div class="rating"><b>4.8</b>{stars(5)}<span>126 reviews</span></div>
<div class="review"><div><strong>Kavya R.</strong>{stars(5)}</div><p>Booked online in a minute and got a reminder the day before. Lovely team.</p>
  <div class="reply"><small>AI suggested reply</small>Thank you, Kavya! We are glad booking was easy. See you next time.</div></div>
<div class="review"><div><strong>Rohit J.</strong>{stars(4)}</div><p>Great service, a short wait at reception.</p></div>""", "Example review dashboard with rating, reviews and an AI suggested reply")


def visual(slug):
    return V[slug]


def thumb(slug):
    return f'<div class="thumb" aria-hidden="true">{V[slug]}</div>'
