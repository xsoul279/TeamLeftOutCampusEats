# Manual Tests

Run every test against the Docker Compose app (`docker compose up --build`,
then http://localhost:5000). Re-test earlier stories before each release and
update the Date and Result columns.

## Results

| User story | Acceptance criterion | Tester | Date | Result | Notes |
| --- | --- | --- | --- | --- | --- |
| US3 | 1: only available listings shown | | | | |
| US3 | 2: listing shows all its details | | | | |
| US3 | 3: sorted by pickup end, soonest first | | | | |
| US3 | 4: message when no listings | | | | |
| US4 | 1: reserve portions, get pickup code | | | | |
| US4 | 2: more portions than remain rejected | | | | |
| US4 | 3: second reservation on same listing rejected | | | | |
| US4 | 4: last portion, only one student wins | | | | |

## Test cases

What to do for each row above, and what should happen.

### US3: Browse available listings

Uses the seed data: at least one active listing, plus an ended, a cancelled,
and a sold-out listing.

| AC | What to do | What should happen |
| --- | --- | --- |
| 1 | Log in as a student and open the listings page. | Every active listing is shown. The ended, cancelled, and sold-out listings are not. |
| 2 | Look at any listing on the page. | It shows the title, vendor name, pickup location, dietary tags, portions remaining, and pickup window. |
| 3 | Compare the pickup end times down the page. | The listing ending soonest is first, and each one after ends later. |
| 4 | Hide every listing: `docker compose exec db psql -U campuseats -d campuseats -c "UPDATE listings SET cancelled = true"`. Reload the listings page. Afterwards run `docker compose down -v` to reset the data. | A message says there are no listings available, instead of a blank page. |

### US4: Reserve portions

Log in as a student for each test. For AC 4 you also need a second student
account.

| AC | What to do | What should happen |
| --- | --- | --- |
| 1 | Pick a listing with at least 2 portions remaining. Note the number. Reserve 2 portions. | A 6-character pickup code is shown. Back on the listings page, that listing's portions remaining went down by 2. |
| 2 | Pick a listing with exactly 1 portion remaining. Try to reserve 2. | An error says there aren't enough portions. No reservation is created and portions remaining is still 1. |
| 3 | Reserve 1 portion from a listing. Then try to reserve from the same listing again. | A message says you already have a reservation for this listing. No second reservation is created. |
| 4 | Pick a listing with exactly 1 portion remaining. Open the app in a normal window and a private window, logged in as two different students. Open the reserve form for that listing in both, then click Reserve in both as close together as you can. | Exactly one window gets a pickup code. The other gets an error. Portions remaining is 0, not -1. |
