# EIS Compass — web calendar (prototype)

One data source, three outputs: a mobile-first web page, a print layout, and subscribable calendar feeds. No framework, no build tools.

## What's in this folder

| Path | What it is | Goes on the website? |
|---|---|---|
| `website/EISCompass.html` | The public page. Its event data is the JSON block `<script id="compass-data">` near the bottom. | **Yes** — replaces the current `/EISCompass.html`, so existing Toddle and email links keep working |
| `website/compass/feeds/{en,ja}/*.ics` | Calendar feeds families subscribe to (all, whole, elc, primary, secondary, high, pta, club) | **Yes** |
| `website/compass/images/` | Event photos (108, about 12 KB each), logo, social preview image | **Yes** |
| `admin/admin.html` | Private editor: open the page, import the spreadsheet, check, publish | **No** — keep it on a staff computer or shared drive |
| `admin/EIS-Compass-events.xlsx` | All events as a spreadsheet (Events / Holidays / Guide sheets) | No |

## Updating events

1. Open `admin/admin.html` in Chrome, Edge or Safari.
2. Drop in the current `EISCompass.html` (it is its own template).
3. Either:
   - **edit the spreadsheet** and use **Import spreadsheet** (you see a preview of new, changed and removed events before anything is applied), or
   - edit a single event in the form.

   If an event's date moves, you can show families a "Date changed (was …)" badge.
4. **Check**: lists errors such as bad dates, plus warnings such as missing Japanese or a description copied from another event.
5. **Publish**: downloads a zip containing `EISCompass.html` and the feeds. Upload them to the same paths.

Unsaved admin work is kept in that browser's local storage until you publish or discard it.

## Links you can share

- `EISCompass.html` opens on the **Upcoming** view (today, this week, next day off).
- `EISCompass.html?for=primary` opens pre-filtered (also `elc`, `secondary`, `high`, `pta`, `club`, `whole`, `parents`). Useful in division newsletters.
- `EISCompass.html?lang=ja` opens in Japanese. Otherwise the phone's language is used, then the visitor's last choice.
- `EISCompass.html#/subscribe` opens the "Subscribe" panel.
- `EISCompass.html#/calendar/2026-12` opens a month; `#/event/<id>` opens one event (every event has a Share button).
- `EISCompass.html?q=SAT` opens a search.

## Notes

- Photos: upload new ones to `compass/images/events/` (WebP or JPEG, about 1200 px wide, under 150 KB) and put the path in the `image` column.
- Times are optional (`15:00` or `15:00-17:00`). Without a time, events are all-day everywhere, including in the feeds.
- Google Calendar refreshes subscribed feeds slowly (up to about 24 h). Apple Calendar refreshes more often.
- The page uses system fonts (Hiragino / Yu Gothic / Noto for Japanese), so there are no font downloads.
- If someone opens the page without JavaScript, or a search engine indexes it, they get a plain bilingual list of every event and holiday. The admin page writes this list when you publish.
