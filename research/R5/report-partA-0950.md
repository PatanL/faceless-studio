# R5 report

_Saved by the orchestrator from the lane's returned findings (subagents cannot write report files). Outputs: _

R5 policy and monetization research is done. The full report is below. I could not save research/R5/report.md: the harness rejected the Write call ("Subagents should return findings as text, not write report files"), so the parent needs to save this text to /Users/patrickliu/Documents/faceless-studio/research/R5/report.md. Items marked (*) come from secondary sources and need checking in the apps.

# R5 — Policy and monetization (2026-11-01)

## What this means for the studio
1. **The approach can be monetized.** YouTube says using AI does not by itself disqualify a channel. What gets demonetized is mass-produced, templated, low-variation content, and reused content. Original scripts, code-drawn visuals and narration that explains or tells a story are on the allowed side of every policy below.
2. **The biggest risk is our own pipeline.** If `studio make --topic X` turns out episodes that only swap the animal, that is YouTube's own example of inauthentic content ("looks like it's made with a template with little to no variation"). Its named examples include "nearly identical narrated stories". Every batch needs a sameness review: compare scene structure, set pieces, endings, thumbnails and titles across recent episodes.
3. **No altered-content disclosure is needed** for animated, non-realistic videos with a generic TTS narrator. YouTube exempts animated content and only requires disclosure for realistic content. TikTok only requires a label for realistic-looking scenes or people. Disclosure becomes required if we add a voice that imitates a real person or photoreal synthetic material. Disclosing does not reduce reach or monetization on YouTube.
4. **YouTube entry thresholds double for new applicants on 2027-02-01.**
   - Today: 1,000 subscribers plus 4,000 watch hours in 12 months, or 10M Shorts views in 90 days.
   - From 2027-02-01: 8,000 watch hours in 365 days, or 20M Shorts views in 90 days.
   - Also from Feb 2027, every channel, members included, needs at least 10M Shorts views in the last 90 days to get Shorts ad revenue in a given month.
   - Existing members keep their place but must accept the new terms by 2027-01-31. Fan Funding and Shopping thresholds are unchanged.
   - Long-form is the realistic way into the Partner Program. Watch hours and Shorts views do not combine.
5. **TikTok Creator Rewards only pays for original videos longer than 1 minute.**
   - Account rules: 18+, at least 10K followers, at least 100K views in the last 30 days, a personal account, a supported country.
   - Duets, Stitches, Photo Mode and sponsored posts don't count.
   - Payouts weigh originality, play duration (watch time and finish rate), search value and engagement.
   - Qualified views*: from the For You feed, watched at least 5 s, and the video reportedly needs at least 1K of them.
   - Vertical cuts should run 61–120 s.
6. **TTS licence matters for anything we publish.**
   - Kokoro-82M is Apache-2.0, so commercial use is fine. Use it.
   - Piper `ryan` is CC BY-NC-SA 4.0 (non-commercial).
   - Piper `lessac` comes from the Blizzard 2013 dataset, which is under a research licence. `amy`, `alan`, `joe` and `libritts_r` are fine-tuned from lessac, so avoid shipping Piper voices.
7. **Horror must stay non-graphic.**
   - YouTube counts animated content as "dramatized". Non-graphic dramatized violence can earn full ads.
   - Visible serious injury, gore focus, or graphic material in the thumbnail or opening seconds gets limited or no ads.
   - Content made to look family-friendly that frightens kids (horror scenes, scary characters) gets limited or no ads.
   - On TikTok, graphic fictional violence can be limited to 18+ or kept off the For You feed.
8. **Set both niches to "Not made for kids".** Cartoon characters count as a made-for-kids factor, and "one of several audiences" is enough to trigger it. Made-for-kids videos lose personalized ads, comments, the notification bell and end screens.

## YouTube details
- **The July 15, 2025 update:** "repetitious content" was renamed "inauthentic content". Creator liaison Rene Ritchie called it a "minor update" and said this content was already ineligible.
  - Allowed: the same intro and outro across videos; a series format where each video has its own storyline.
  - Not allowed: repetitive videos with low educational value; the same situation with the same outcome; slideshows, templated storylines or scrolling text with little narrative; AI content built on generic templates that suggests mass production.
  - Enforcement is channel-level: removal from the Partner Program or withheld earnings.
- **Reused content:** repurposing without significant original commentary or change. This includes content that only reads others' material (articles, posts). It demonetizes the whole channel, even with permission and even without copyright claims.
- **Shorts revenue:** creators keep 45% of a pooled allocation; long-form creators keep 55% of ad revenue. Licensed music shrinks a Short's pool share (one track halves it, two tracks cut it to a third), so our own SFX keeps 100%. Shorts over 1 minute with claimed content are blocked from monetization.
- **Partner Program review:** the whole channel is reviewed by automated systems and humans, taking about a month. After a rejection you can appeal within 21 days or reapply after 30 days (90 days after a repeat).
- **Direction of travel:** CEO Neal Mohan's January 2026 letter names managing "AI slop" as a 2026 priority. Expect stricter detection.

## TikTok details
- Content with "unoriginal or reused material without anything new" is kept off the For You feed. That means no reach and no Creator Rewards.
- Using automation to bypass TikTok's systems is prohibited. Post manually or through the official API.
- *One unsourced third-party site claims fully AI-generated content (AI voice plus AI visuals) is excluded from Creator Rewards; others say labeled, original AI content stays eligible. No official text was found either way. TTS is our weak point here. Consider A/B testing a human voice-over when an account nears 10K followers.

## Instagram / Meta
- Instagram has no standing per-view pay. The Reels Play bonus closed to new invites in March 2023, and current bonuses are invite-only and seasonal*. Treat Reels as reach.
- Facebook's unified Content Monetization program (invite-based*, pays on qualified views) is Meta's per-view route, via cross-posting.
- Since 2024, accounts that repost content they didn't create 10+ times in 30 days are dropped from recommendations. In April 2026 this extended to accounts that mainly post unoriginal content, including photos and carousels.
- Meta's July 2025 rule: repeat reusers lose Facebook monetization for a period and get reduced distribution on everything they post.
- Export clean masters for each platform, with no TikTok watermark.

## By niche
**Animal explainer**
- Keeps monetization: researched, specific facts paraphrased in our own words with sources in the description; a different structure and set pieces each episode; a teen/adult tone; long-form 8–12 min; stock footage only if licensed.
- Loses it: 30 one-template "Why you'd never want to meet a [X]" videos; stat slideshows with TTS; copying Depth Theory's scripts, assets or title-and-thumbnail combinations; being set as made for kids (a revenue cut rather than demonetization).

**Phone-chat horror**
- Keeps monetization: wholly original stories, characters, rules and endings; endings that differ episode to episode; suspense by implication; clean thumbnails and opening seconds; a generic invented chat UI (no WhatsApp, iMessage or WeChat branding); fiction framing ("Part 1"); no real people; Not made for kids; TikTok parts of at least 61 s.
- Loses it: translated reposts or re-voicing of the Chinese series the references appear to be; reading Reddit or creepypasta posts word for word; gore; a kid-appealing look with scary themes; high-volume same-beat "rules horror".

**What-if**
- Keeps monetization: original premises with real reasoning, and our own characters and sets.
- Loses it: template arcs with stock visuals; realistic AI imagery of real people without disclosure; fiction framed as real news.
- The Part B Awaken recreation is a study piece only. Publishing or monetizing it would be reused content and likely copyright infringement.

## Pipeline rules (suggested for STUDIO.md)
1. Original scripts; facts paraphrased, never read verbatim from a source.
2. A sameness review on every batch, tracking set pieces per episode in the storyboard JSON.
3. Kokoro-82M is the only TTS voice for published work.
4. Self-made or CC0 / commercially licensed music and SFX, with the licence files kept in the repo.
5. Not made for kids; Altered content set to No unless realistic synthetic material is added.
6. Horror stays non-graphic, and its thumbnails and first 7 s stay clean.
7. Vertical cuts of 61–120 s that each stand alone; long-form of 8–12 min.
8. No bulk-upload bots and no bought engagement.
9. Never publish anything derived from Awaken or the reference channels.
10. Consider applying for the Partner Program before 2027-02-01.

## Sources
**YouTube (official)**
- [YPP eligibility](https://support.google.com/youtube/answer/72851?hl=en)
- [Channel monetization policies: inauthentic and reused content](https://support.google.com/youtube/answer/1311392?hl=en)
- [Altered or synthetic content disclosure](https://support.google.com/youtube/answer/14328491?hl=en)
- [Advertiser-friendly guidelines](https://support.google.com/youtube/answer/6162278?hl=en)
- [Made for kids](https://support.google.com/youtube/answer/9528076?hl=en)
- [Shorts monetization](https://support.google.com/youtube/answer/12504220?hl=en)
- [YPP 2027 updates (blog)](https://blog.youtube/news-and-events/youtube-partner-program-updates-2027-new-opportunities-earn/)
- [AI disclosure (blog)](https://blog.youtube/news-and-events/disclosing-ai-generated-content)

**TikTok (official)**
- [Creator Rewards launch (newsroom)](https://newsroom.tiktok.com/introducing-the-new-creator-rewards-program)
- [Integrity and authenticity](https://www.tiktok.com/community-guidelines/en/integrity-authenticity)
- [Sensitive and mature themes](https://www.tiktok.com/community-guidelines/en/sensitive-mature-themes)
- [For You feed standards](https://www.tiktok.com/community-guidelines/en/fyf-standards)

**TTS licences**
- [Kokoro-82M (Apache-2.0)](https://huggingface.co/hexgrad/Kokoro-82M)
- [Piper voices](https://huggingface.co/rhasspy/piper-voices) (per-voice MODEL_CARD files)
- [Lessac / Blizzard 2013 research licence](https://www.cstr.ed.ac.uk/projects/blizzard/2013/lessac_blizzard2013/license.html)

**Secondary**
- [Tubefilter: 2027 thresholds](https://www.tubefilter.com/2026/08/10/youtube-partner-program-ad-eligibility-requirements-shorts/)
- [Search Engine Journal: Ritchie clarification](https://www.searchenginejournal.com/youtube-monetization-update-spam-not-reaction-channels/550755/)
- [Social Media Today](https://www.socialmediatoday.com/news/youtube-clarifies-monetization-update-inauthentic-repeated-content/752892/)
- [Plagiarism Today](https://www.plagiarismtoday.com/2025/07/08/youtube-targets-inauthentic-content/)
- [eWeek](https://www.eweek.com/news/youtube-responds-to-ai-concerns/)
- [Tubefilter: Mohan 2026 letter](https://www.tubefilter.com/2026/01/21/neal-mohans-2026-letter-to-creators-a-lot-of-ai-a-tiktok-shop-competitor-and-beautifully-produced-tv-to-compete-with-netflix/)
- [Buffer: TikTok Creator Rewards](https://buffer.com/resources/tiktok-creativity-program/)
- [Storrito (unsourced AI claim)](https://storrito.com/resources/what-tiktoks-ai-monetization-restrictions-signal-for-creator-income/)
- [PetaPixel: Instagram, April 2026](https://petapixel.com/2026/04/30/new-instagram-policies-target-reposted-content/)
- [WebProNews](https://www.webpronews.com/instagrams-aggregator-purge-original-creators-gain-ground-as-repost-empires-crumble/)
- [Tubefilter: Instagram originality, 2022](https://www.tubefilter.com/2022/04/21/instagram-adam-mosseri-algorithm-change-original-content/)
- [Tubefilter: Meta, July 2025](https://www.tubefilter.com/2025/07/15/ai-slop-unoriginal-repetitive-content-monetization-facebook-meta/)
- [Search Engine Journal: Meta](https://www.searchenginejournal.com/meta-follows-youtube-in-crackdown-on-unoriginal-content/551096/)
- [ppc.land: Facebook Content Monetization](https://ppc.land/facebook-launches-unified-content-monetization-program-for-creator-earnings/)
