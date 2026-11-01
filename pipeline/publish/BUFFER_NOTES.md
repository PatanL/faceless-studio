# Buffer API: what L3 verified and what it assumes

Read on 2026-11-01 (UTC ~19:00) from Buffer's own pages. No API key was available, so **nothing below was checked
against the live API**. "Verified" means "stated in Buffer's current docs or schema reference", not "observed in a
response". Run `python -m pipeline.publish.buffer introspect` with the human's key to pin the live schema
(`data/buffer_schema.json`; the command also checks every field this lane uses and exits 1 on a mismatch).

Sources:
- Help center, "What is Buffer's API?": https://support.buffer.com/articles/using-buffers-api-GtIYIQilz5
  (the old URL `support.buffer.com/article/859-what-is-buffers-api` now returns 404)
- Developer docs index: https://developers.buffer.com/llms.txt, and the guides it lists: getting-started,
  authentication, agent-setup, your-first-post, posts-and-scheduling, hosting-media, character-limits,
  error-handling, api-limits
- Examples: create-draft-post, create-scheduled-post, create-video-post, get-organizations, get-channels
- Full schema reference: https://developers.buffer.com/reference.md; changelog: https://developers.buffer.com/changelog.md
  (latest entry 2026-10-22)

## Verified in the docs

| Topic | What the docs say | Where L3 uses it |
|---|---|---|
| Endpoint | One GraphQL endpoint, `https://api.buffer.com`, `POST` with `Content-Type: application/json` and a JSON body `{"query", "variables"}` | `buffer.py` (`BUFFER_API_URL` overrides) |
| Auth | `Authorization: Bearer <key>`. Keys are created at publish.buffer.com/settings/api by an organization **owner**. A key acts for the whole account (every organization). Free plan: 1 key | `buffer.py`, key read only from `~/studio/.env` |
| Availability | The API is on every plan, Free included | |
| Organizations | `query { account { organizations { id name } } }` | `buffer channels`, org fallback when `BUFFER_ORG_ID` is unset |
| Channels | `channels(input: { organizationId })` returns `id name service ...`; `service` enum includes `youtube`, `tiktok`, `instagram`. Channel flags `isDisconnected`, `isLocked`, `isQueuePaused` | `buffer channels`; `post` checks each channel id's service and flags |
| Create post | `createPost(input: CreatePostInput!)` returns the union `PostActionPayload`: `PostActionSuccess { post }` or a `MutationError` (`InvalidInputError`, `LimitReachedError`, `UnauthorizedError`, `NotFoundError`, `UnexpectedError`, `RestProxyError`). Always select `... on MutationError { message }` | `queries.graphql` `CreatePost` |
| Required input | `channelId`, `schedulingType` (`automatic` = Buffer publishes, `notification` = reminder to post by hand), `mode` (`ShareMode`: `addToQueue`, `customScheduled`, `shareNext`, `shareNow`) | `post.build_input` |
| Scheduling | `mode: customScheduled` plus `dueAt` (ISO 8601 UTC) | every post uses the slot time |
| Drafts | `saveToDraft: true` makes the post a draft (status `draft`), skips posting-limit checks, and it "will not be published until explicitly scheduled". `needsApproval` exists but only applies when the channel's posting policy requires approval. If a channel is set to "Requires Approval", API posts become drafts awaiting approval anyway | draft mode |
| Video | `assets: [{ video: { url, metadata: { thumbnailOffset } } }]`. `thumbnailOffset` (ms) picks the cover frame on Instagram, TikTok and Pinterest only. `VideoAssetInput.thumbnailUrl` must not be used ("the API rejects video assets that set this field"); custom video thumbnails are not supported | `build_input` (offset on IG/TikTok only) |
| Media hosting | No upload endpoint. The URL must be public, direct (no redirect or preview page), HTTPS and stable. **"The URL must stay reachable until the post publishes, not just when you create it"**: Buffer fetches the media when the post goes out, hours or days later for scheduled posts. A URL that cannot be fetched at create time fails the mutation (example message "Failed to fetch image dimensions: Not Found") | `host.py`, the hold in `post._hold` (see "Design consequences") |
| YouTube fields | `metadata.youtube`: `title` and `categoryId` (both "Required on create"), `privacy` (`public`/`unlisted`/`private`), `madeForKids` (default false), `isAiGenerated`, `notifySubscribers`, `embeddable`, `license`. Title limit 100; the post `text` is the video description (limit 5000) | `build_input` youtube |
| Instagram fields | `metadata.instagram`: `type` (`PostType!`: `post`/`story`/`reel`...), `shouldShareToFeed` (`Boolean!`), `isAiGenerated`, `firstComment` | `type: reel`, `shouldShareToFeed: true`, `isAiGenerated: true` |
| TikTok fields | `metadata.tiktok`: `isAiGenerated` ("TikTok video only") and `title` (photo posts only) | `isAiGenerated: true` |
| AI disclosure | `isAiGenerated` exists on the YouTube, Instagram and TikTok metadata inputs (added to the schema per the changelog) | set `true` on all three |
| Supported channels | Help center: Instagram, Threads, LinkedIn, X, Facebook, **TikTok**, Google Business, Mastodon, YouTube, Pinterest, Bluesky | |
| Text limits | Counted in UTF-16 code units. TikTok with a video 2200, Instagram 2196 (each line break counts 2), YouTube description 5000, YouTube title 100 | `captions.py` |
| Post fields | `Post`: `id status dueAt sentAt externalLink error { message } assets { source ... on VideoAsset { video { isVideoProcessing } } } metadata`. `PostStatus`: `draft needs_approval scheduled sending sent error`. `post(input: { id })` fetches one | `status.py` (aliased batch query) |
| Errors | HTTP 200 for GraphQL; system errors in `errors[].extensions.code`: `UNAUTHORIZED`, `FORBIDDEN`, `NOT_FOUND`, `UNEXPECTED`, `RATE_LIMIT_EXCEEDED` (plus HTTP 401 for a missing or bad key) | `BufferClient.request`: auth -> exit 5, rate limit -> wait and retry |
| Rate limits | Shared by all keys of the account. Free: 150 per 15 min, 600 per 24 h, 1,000 per channel per 30 days (max 3,000). Essentials: 450, 1,800, 3,000 per channel (max 30,000). A 429 carries `Retry-After` (seconds) and `RateLimit` headers per window | 429 sleeps `Retry-After` (cap 900 s, 4 tries). Hold polling every 15 min |
| Metrics | `Post.metrics` (experimental, personal key only, refreshed about once a day): includes `views`, `averageTimeWatched` (TikTok, IG Reels) and `totalTimeWatched`. The help center says not to rely on it for reporting | not used by L3; see the L4 note below |

## Assumed (unverified until the first real call)

1. **A draft keeps its `dueAt`.** Draft mode sends `saveToDraft: true` together with `mode: customScheduled` and
   `dueAt`, on the assumption that approving the draft in Buffer schedules it for that time. The docs only say a draft
   "will not be published until explicitly scheduled". If the draft comes back with `dueAt: null`, the human picks the
   time when approving (the slot time is also in `HUMAN.md` and in our ledger).
2. **Automatic publishing works for these three channels.** We send `schedulingType: automatic`. Channels have
   `YoutubeMetadata.defaultToReminders` / `TiktokMetadata.defaultToReminders`, so a channel might only support
   reminder (`notification`) publishing. If the mutation rejects `automatic`, the row is `failed` with Buffer's
   message and the operator escalates.
3. **Whether Buffer copies the video at create time.** The docs say Buffer fetches the media at publish time. After
   the first real post, `post.py` reads `post.assets[].source`. If it is a Buffer-hosted URL, the tunnel closes at once.
   If it is still our URL, the process holds the tunnel (see below).
4. **`isAiGenerated` sets the platform's own label** (YouTube "altered or synthetic content", TikTok "AI-generated
   content", Instagram "AI info"). The field exists, but nobody has checked that it reaches each platform's toggle. The
   human checks this on the first draft of each platform before setting `disclosure_ok_auto.<platform>`.
5. **`externalLink` format.** We parse YouTube `.../shorts/<id>` or `?v=<id>`, TikTok `/video/<digits>` and
   Instagram `/reel/<shortcode>`. For Instagram that gives a shortcode, not the Graph media id.
6. **Quick tunnel URLs are accepted.** `*.trycloudflare.com` is public HTTPS and serves the file directly, which meets
   the documented bar. The docs warn that some Cloudflare bot protection blocks automated fetches; quick tunnels have
   none (the selftest's fetches went through), but Buffer's own fetcher has not been tried.
7. **YouTube category.** We default to `categoryId: "28"` (Science & Technology). Override it with `BUFFER_YT_CATEGORY_ID`
   (for example `27` Education).
8. **Introspection is enabled.** The browser API Explorer implies it, but this is untested. If it is disabled,
   `introspect` says so, and the docs above remain the reference.
9. **The TikTok channel works with Buffer.** TikTok is in the help center's list of API channels, but it is missing from
   the developer guide's "Supported platforms" list (the docs disagree). `buffer channels` must show `service: tiktok`.

## Not possible through Buffer (as documented)

- Uploading the file itself: a hosted URL is required.
- Custom thumbnail images on any platform. YouTube and Shorts get no frame choice through the API at all.
- YouTube tags (no field). Our tags stay in `captions.json` for reference only.
- Reading comments, and full analytics (only the experimental `Post.metrics`).

## Design consequences (requests for the integrator, see README.md)

- **Ephemeral URL vs. fetch at publish time.** A 30-minute quick tunnel (OPERATOR_DESIGN 8.4) is not enough. In
  `cloudflared` mode, `post.py` keeps the tunnel open after creating the posts. It closes when every post is
  sent/error/deleted, or when Buffer reports its own asset URL, or at the slot time plus `drafts_missed_h` (draft) or
  plus 1 h (auto), and in any case after at most `--hold-max-h` (12 h). So the publish job runs for hours: L5 must
  start it detached and must not count it as hung. A quick tunnel has no uptime guarantee, so for auto mode the
  recommended setup is `PUBLIC_HOST_MODE=static`: a stable public URL the human provisions (for example a named
  Cloudflare tunnel or an R2 bucket) that maps to `PUBLIC_MEDIA_DIR`. `python -m pipeline.publish.host serve --dir
  $PUBLIC_MEDIA_DIR` is the matching file server. In static mode the file stays until `status.py` prunes it, once every
  post of that slug is terminal.
- **Request budget on the Free plan** (3 channels give 3,000 requests per 30 days, about 100 a day): a post costs 2
  requests (organizations, channels) plus 3 creates. Each status refresh is 1 request when anything is open, so run it
  every 30 min only while posts are open (`status` sends nothing when none are). The hold polls every 15 min, about
  60-75 requests a day in all. If L4 also reads `Post.metrics`, budget for it or move to Essentials.
- **L4 note:** `Post.metrics` may be the only automated source of TikTok numbers (`views`, `averageTimeWatched`). It is
  experimental and refreshed once a day, so treat it as secondary to the human's TikTok imports. Instagram
  `external_id` is the shortcode: L4 maps it to a Graph media id (`/{ig-user-id}/media?fields=shortcode`).
