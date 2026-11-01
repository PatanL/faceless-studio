_Saved by the orchestrator from the closeout R5 lane (official sources; subagents cannot write report files). The earlier Part A version is report-partA-0950.md._

# R5 — Platform policy and monetization (official sources only)

Lane R5 (redo), checked 2026-11-01 ~11:40 UTC. Every claim below is tied to an official page: YouTube Help or the YouTube Blog; TikTok Support, Legal, Community Guidelines or Newsroom; or Meta Transparency Center or Newsroom. Quotes are kept under 15 words. Policies change: **re-open the linked pages on publish day.**

What our pilots are made of, for this analysis:
- original scripts (originality gate PASS)
- hand-coded 2D vector animation (Remotion/SVG, no AI image or video models)
- procedurally synthesized music beds and SFX (`pipeline/audio/synth.py`, no samples)
- narration from a local TTS model (Kokoro-82M, Apache-2.0; voices am_michael / af_heart). The voice is not a clone of any real person.

Lengths: orca 75.1 s, blue whale 70.1 s, horror 65.2 s (all 9:16).

## TL;DR (what to do on upload)

| Platform | Setting | Our answer | Why (official rule) |
|---|---|---|---|
| YouTube / Shorts | Studio upload > Attributes > **"AI use"** (older UI: "Altered content") | **Yes** (voluntary, conservative) | Strictly, only *realistic* content needs it, and fully animated video is exempt. But the narrator is a realistic synthetic voice, and the 2024 rules list a synthetic voice narrating a video. Disclosing "won't limit a video's audience or impact its eligibility to earn money" (YouTube Help). |
| TikTok | More options > **"AI-generated content"** toggle | **On** | TikTok requires labels on realistic AI images, **audio** or video. |
| Instagram / Facebook | AI label ("AI info") when sharing | **On** | Meta requires the disclosure tool for "realistic-sounding audio" that was digitally created. |
| All | Caption line | Keep a plain-text synthetic-voice line | TikTok also accepts "a sticker or caption" as a disclosure, and the line costs nothing elsewhere. |

Monetization: our format (own script, own animation, and narration with educational or story value) falls on the "allowed" side of every originality rule found. The risks are:
- **templated sameness across uploads**
- **reading other people's stories**
- **text-only chat scrolls**
- **claimed music in Shorts over one minute**

## 1. YouTube monetization: reused and "inauthentic" content

Source: [YouTube channel monetization policies](https://support.google.com/youtube/answer/1311392)

- **Rename (15 Jul 2025):** "repetitious content" became "inauthentic content". Mass-produced or repetitive content was already ineligible, and the reused-content policy did not change.
- **Core expectation:** content should "Not be mass-produced, generic, repetitive, or manipulative."
- **Not allowed:**
  - "Image slideshows, templated storylines, or scrolling text with minimal or no narrative"
  - "Channels that heavily rely on generic templates or emotionally manipulative themes"
  - "AI-generated content made with generic or unoriginal templates"
  - content that "looks like it's made with a template", "often the result of mass production or autogeneration"
- **Allowed:**
  - "Same intro and outro for your videos" (as long as the bulk of each video differs)
  - tools and templates are fine, but "the final product must still demonstrate your creative vision"
  - "using AI to edit your video scripts"
- **Reused content:** allowed "if viewers can tell that there's a meaningful difference". Not allowed: "readings of other materials you did not originally create" and "Content uploaded many times by other creators".
- **TTS:** the page does not mention TTS or AI voices. A synthetic voice is not itself a monetization problem. What is judged is whether the video is original, varied, and carries narrative or educational value.

Source: [YouTube Shorts monetization policies](https://support.google.com/youtube/answer/12504220)

- Not eligible for revenue sharing:
  - "Non-original Shorts, such as unedited clips from others' movies"
  - reuploads of other creators' content
  - "compilations with no original content added"
- **Length trap:** "Shorts over one minute in length that contain claimed content are blocked." All pilots are over 60 s, so never add library or trending music. Our own synthesized beds are fine.

Source: [How to earn money on YouTube (YPP)](https://support.google.com/youtube/answer/72857)

- Ad revenue needs "1,000 subscribers" plus either "4,000 qualified watch hours" (long form) or "10 million qualified Shorts views in the last 90 days".
- "we review your channel before you're accepted in the YouTube Partner Program". The whole channel is reviewed, so recent uploads must look varied.

How a faceless animated channel stays eligible (derived from the rules above):
1. Original script per upload. Never narrate someone else's story, article or Reddit post.
2. Each video has a real narrative or explanation, never a slideshow or scrolling text read aloud.
3. Vary storyline structure and scene sets between uploads. A shared intro/outro, kit style and voice are fine.
4. Never re-upload the same cut with a new title. Post the 9:16 and 16:9 cuts as one Short plus one long-form video, not as two Shorts.
5. Keep sources in explainer descriptions to show educational value.

## 2. YouTube altered or synthetic content disclosure

Sources: [Disclosing use of GenAI content](https://support.google.com/youtube/answer/14328491) (previously titled "altered or synthetic content"); [YouTube Blog, 18 Mar 2024](https://blog.youtube/news-and-events/disclosing-ai-generated-content/)

- **Required:** "We require creators to disclose AI-generated or altered content that seems realistic." The must-disclose list:
  - "Makes a real person appear to say or do something they didn't do."
  - "Alters footage of a real event or place."
  - "Generates a realistic scene that didn't actually occur."
  - "Creates music that's the main focus of the video."
- **Not required:** "Creators don't need to disclose non-realistic content that's made with AI". Examples:
  - "Using an AI-generated or altered animation of a missile in a fully animated video"
  - production help for an "outline, script, thumbnail, title, or infographic"
  - "Caption creation"
  - "Cloning one's own voice to create voice overs or dubs"
- **Voice:** the 2024 blog lists "synthetically generating a person's voice to narrate a video" under likeness of a realistic person. The current Help page adds that labels "may appear in the expanded description for non-music AI-generated audio".
- **Where to set it:** upload flow > Attributes > "AI use" > Yes/No.
- **Effect:**
  - "Disclosing AI content alone won't limit a video's audience or impact its eligibility to earn money."
  - Repeatedly not disclosing when required risks labels added by YouTube, removal, or "suspension from the YouTube Partner Program".
  - YouTube may also auto-label content its systems "detect is AI generated or altered".

**Does TTS narrating original animation require it?** Read strictly, probably not: the animation is exempt, no real person is imitated, and no realistic event is depicted. But it is a realistic synthetic human voice, the one case the 2024 blog names, and it can be auto-detected. Disclosure has no cost and non-disclosure has a YPP downside, so **we answer AI use = Yes**. The label goes in the expanded description, not on the player.

Never use a voice that imitates a real person ([impersonation policy](https://support.google.com/youtube/answer/2801947)).

## 3. TikTok: AI labels and Creator Rewards

**Labels.** Sources:
- [Newsroom, 19 Sep 2023](https://newsroom.tiktok.com/en-us/new-labels-for-disclosing-ai-generated-content)
- [Community Guidelines: Integrity and Authenticity](https://www.tiktok.com/community-guidelines/en/integrity-authenticity) (released 25 Aug 2026, effective 24 Sep 2026)
- [Supporting responsible, transparent AIGC](https://www.tiktok.com/safety/en/policies-and-engagement/supporting-responsible-transparent-ai-generated-content)
- [Help Center: AI-generated content](https://support.tiktok.com/en/using-tiktok/creating-videos/ai-generated-content)

Rules:
- TikTok "requires people to label AI-generated content that contains realistic images, audio or video". For non-realistic AI content, labelling is encouraged, not required.
- The Community Guidelines cover "realistic-looking scenes or people". Unlabeled content "may be removed, restricted, or labeled".
- A disclosure can also be "a sticker or caption".
- Auto-labels are applied for TikTok's own AI effects and for C2PA Content Credentials. Auto labels can't be removed.
- Help Center (JavaScript-only page, wording via search index): the label does not affect distribution. Labelling unaltered content as AI is a ToS violation.
- **Ours:** realistic synthetic audio, so set **"AI-generated content" = on**.

**Creator Rewards.** Sources:
- [US terms, updated 20 Jul 2026](https://www.tiktok.com/legal/page/global/creator-rewards-program-us/en)
- [EEA terms](https://www.tiktok.com/legal/page/global/tiktok-creator-rewards-program-eea/en)
- [Help Center: Creator Rewards Program](https://support.tiktok.com/en/business-and-creator/creator-rewards-program) (JavaScript-only, wording via search index)

Rules:
- **Length:** "a duration of at least 1 minute publicly posted on the Platform". Pilots are 65.2, 70.1 and 75.1 s. Keep re-cuts at 62 s or longer.
- **Account:** "at least 10,000 authentic followers" and "100,000 authentic total video views in the last 30 days". Must be 18+ with a personal account.
- **Views:** at least 1,000 qualified For You feed views. A view counts after 5 s, and "not interested" views are excluded.
- **Originality:**
  - The help page asks for "original and high-quality content" made by yourself.
  - The EEA terms require "original content and produced entirely by the creator", and exclude ads, Duets, Stitches and Photo Mode posts.
  - Copyrighted music playing over one minute can get a video muted.
- The US terms do not mention AI. Unoriginal content is what gets excluded, not an AI voice.
- The Community Guidelines make content that "includes unoriginal or reused material" ineligible for the For You feed.

## 4. Instagram / Meta AI labels

Sources:
- [Community Standards: Misinformation](https://transparency.meta.com/policies/community-standards/misinformation/)
- [Meta Newsroom, 19 Feb 2026 (updated 27 Oct 2026)](https://about.fb.com/news/2026/02/meta-prepares-for-2026-us-midterms/)
- [Labeling approach (2024, updated)](https://about.fb.com/news/2024/04/metas-approach-to-labeling-ai-generated-content-and-manipulated-media/)
- [Transparency Center: Labeling AI Content](https://transparency.meta.com/governance/tracking-impact/labeling-ai-content/)

Rules:
- "We require people to disclose, using our AI-disclosure tool," for posts "with photorealistic video or realistic-sounding audio" that was "digitally created or altered", "and we may apply penalties if they fail to do so."
- The label is "AI info" (it replaced "Made with AI" on 1 Jul 2024). Meta also applies it automatically from industry signals such as C2PA.
- **Ours:** the visuals are not photorealistic, but the audio is realistic-sounding, so **add the AI label** when sharing. The exact in-app path was not found on help.instagram.com; check the share screen's advanced settings on publish day.

## 5. Per niche: what keeps the channel monetizable

For ad suitability, the [Advertiser-friendly content guidelines](https://support.google.com/youtube/answer/6162278) count animated fiction as "Dramatized".

**2D animal explainer**
- Original research script with sources gives clear educational value.
- Risk: "templated storylines" if every episode is "Why you'd never want to meet X" with the same beats. Vary the formats: scale paradox, depth ladder, myth-busting, options.
- Risk: "made for kids". YouTube counts "animated characters or cartoon figures" as a factor ([Made for kids](https://support.google.com/youtube/answer/9528076)). Set No honestly, and keep titles, thumbnails and tone aimed at a general audience.
- Non-graphic predation fits "Violence that is unrealistic, playful, and generally acceptable for all ages" (full ads).

**Phone-chat horror**
- Format risk: "scrolling text with minimal or no narrative" and "readings of other materials you did not originally create". So:
  - original fiction only: no translated reposts of the Chinese series, no Reddit readings
  - full narration plus animated scenes, not just a scrolling chat log
  - a new premise or new beats in every Part ("series with distinct storylines" are allowed)
- TikTok excludes text-overlay-only and slightly modified content (help page via search index).
- Ad suitability: dramatized non-graphic dread earns full ads. Avoid "severe and shocking injuries" (limited ads) and shocks "solely with the intent to shock" (no ads). No gory thumbnails.
- Keep the "Original fiction" caption line so the first-person story isn't read as a real event or a real company.
- Disclosure block: `research/R5/horror-pinned-rules-DISCLOSURE.md`.

**What-if**
- Base each episode on real science with sources. Avoid generic "what if X disappeared" list templates.
- YouTube requires disclosure for GenAI "realistic scene that didn't actually occur" (for example, a "realistic depiction of a tornado ... moving toward a real city").
  - Our code-drawn, stylized visuals are not GenAI and not photorealistic, so this doesn't apply today.
  - Never mix in AI-generated realistic footage of real places or disasters. If that ever happens, set AI use = Yes and frame the video as hypothetical.
- TikTok bars harmfully misleading AIGC even when labelled. Frame every scenario as hypothetical early in the video and in the caption.

## Open items / not verified directly
- The TikTok Help Center pages (labels, Creator Rewards) need JavaScript and could not be fetched directly. Their wording comes from TikTok's own pages as shown in search results. Legal terms and Newsroom pages were fetched directly.
- Instagram's exact in-app path for the AI label was not found.
- The YouTube field is now "AI use" (Attributes). Older Studio builds call it "Altered content"; it is the same question.
--- END research/R5/report.md ---
