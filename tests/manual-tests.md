# US1 and US2 release re-test - 2026-10-30

Tested by Rinkatur5 against merged `dev` commit
`78c82dfbb3bd15eb7274eb604d11d95f77bed098` after PR #53. The fresh Docker Compose
project `campuseats-a20-check` used PostgreSQL and port 15020 with its own
disposable volume. Forms were exercised through the browser; PostgreSQL was
inspected read-only to verify persistence and password hashing. No application
code was changed for this re-test.

| User story | Acceptance criterion | Tester | Date | Result | Notes |
| --- | --- | --- | --- | --- | --- |
| US1 | 1: register either role and redirect to login | Rinkatur5 | 10/30/26 | passed | New student and vendor with unique emails and an 8-character password both reached login; both rows persisted with the selected role. |
| US1 | 2: reject duplicate email | Rinkatur5 | 10/30/26 | passed | Reused the student's email in uppercase with a different name; duplicate error displayed and user count stayed unchanged. |
| US1 | 3: reject and identify empty required fields | Rinkatur5 | 10/30/26 | passed | Tested name, email, password, role, and all fields empty; each missing field was identified and no account was added. A 7-character password was also rejected. |
| US1 | 4: store hashed passwords | Rinkatur5 | 10/30/26 | passed | Both newly registered passwords were stored as scrypt hashes, distinct from the submitted password; hashes were not copied into this report. |
| US1 | 5: correct role home; wrong password stays logged out | Rinkatur5 | 10/30/26 | passed | Wrong password showed an error on login; correct credentials opened Student Home and Vendor Home respectively. |
| US2 | 1: store a vendor-owned listing with its fields and tags | Rinkatur5 | 10/30/26 | passed | Posted listings with zero, multiple, and all five allowed tags, including 1 and 100 portions. PostgreSQL confirmed all fields, remaining counts, and the posting vendor ID. |
| US2 | 2: reject reversed or past-ended pickup windows | Rinkatur5 | 10/30/26 | passed | Each invalid window displayed the relevant error; neither attempted listing was stored. |
| US2 | 3: deny student access to posting page | Rinkatur5 | 10/30/26 | passed | Logged in as a student and opened the recorded `/listings/new` URL directly; received the 403 Forbidden page. |

All eight acceptance rows passed on the integrated Sprint 1 application. This
records the story re-test; design, Scrum evidence, release review, and the `v1`
tag remain separate release requirements. Earlier runs and later-story case
specifications are retained below.

## Previous runs and other story specifications

| User story | Acceptance criterion | Tester | Date | Result | Notes |
| --- | --- | --- | --- | --- | --- |
| US1 | 1: When on the registration page, entering a name, unique email, password of at least 8 characters, and selecting a valid role ('vendor', or 'student') will store my account in PostgreSQL and I am then redirected to the login page. | Caine | 10/27/26 | passed | fixed error where username wasn't being passed - mismatch in the templates. Fixed and registering is now working |
| US1 | 2: A duplicated email is rejected and an error message is shown | Caine | 10/27/26 | passed | duplicate email is rejected and the message "Email is already registered" is displayed. |
| US1 | 3: Account is not created if a required field is empty and the empty field is identified | Caine | 10/27/26 | passed | tested for each field and all of them at once - all properly display error messages individually and when all are blank, displays all error messages for every field. |
| US1 | 4: Passwords are stored hashed, not in plain text | Caine | 10/27/26 | passed | checked in PostgreSQL that passwords are stored as scrypt hashes, not plain text |
| US1 | 5: If an account exists and the correct user/pass are entered, user is redirected to the home page for selected role. If wrong pass, an error message is displayed | Caine | 10/27/26 | passed | tested for email/pass error message works. Tested directly after registering, everything correctly saved. |

## US2 Manual test cases ##

## Test 1 - Vendor Posts Listing ##
Acceptance Criteria 1: "Given I am logged in as a vendor, when I enter a title, description, number of portions (1 to 100), pickup location, zero or more dietary tags (vegetarian, vegan, gluten-free, halal, contains nuts), and a pickup window start and end, and click "Post", then the listing is stored and linked to my vendor account."

Steps:
1. Log in as vendor
2. Open new listing page
3. Enter criteria:
- Title: Vegetarian Lunch Test
- Description: Leftover vegetarian lunches
- Portions: 3
- Pickup location: Cafeteria counter
- Dietary tages: vegetarian and gluten free
- Pickup start: Tomorrow at noon
- Pickup end: Tomorrow at 1 PM
4. Post listing
5. Check PostgreSQL and confirm that the listing was saved as entered.

Expected result: 
Listing is saved and linked to the vendor who posted the listing. Selected tags should be included. 

Actual result: 
Listing is saved as confirmed through PostgreSQL. All relevant information is included such as title, description, pickup location, start times, end times, tags, and number of portions. 

## Test 2 - Invalid Pickup Times Are Rejected ## 
Acceptance criteria 2: "Given the pickup window end is before its start, or the end is in the past, when I click "Post", then the listing is not saved and I see an error."

Steps:
1. Log in as vendor.
2. Open new listing page
3. Enter valid food details and title
4. Set pickup starrt to tomorrow at 1 PM
5. Set pickup end to tomorrow at noon.
6. Click Post and record errors
7. Try another listing with new title
8. Set pickup start to yesterday at noon
9. Set pickup end to yesterday at 1 PM
10. Click Post and record errors.
11. Check PostgreSQL for the attempted listings

Expected Results:
Both submissions display an error that prevents the listing from being posted. 

Actual Result: 
Correct error flags were given when attempting to give invalid end and start times. Listings were not saved as confirmed by PostgreSQL.

## Test 3 - Student Opening Posting Page ##
Acceptance Criteria 3: "Given I am logged in as a student, when I try to open the new-listing page, then access is denied."

Steps:
1. Log in as a vendor and copy listing page's URL.
2. Make sure to log out.
3. Log in as a student.
4. Paste the URL into the browser and open

Expected result:
Access is denied

Actual result: Access is denied by page, and correct error flag is shown. "You are not allowed to create a listing". Works as intended!

# Manual Tests

Run every test against the Docker Compose app (`docker compose up --build`,
then http://localhost:5000). Re-test earlier stories before each release and
update the Date and Result columns.

## Results

| User story | Acceptance criterion | Tester | Date | Result | Notes |
| --- | --- | --- | --- | --- | --- |
| US3 | 1: only available listings shown | Ethan | 11/08/26 | passed | Active seed listings were shown. After cancelling one, ending one, and selling out one (plus 20 sold-out test listings), none of them appeared. |
| US3 | 2: listing shows all its details | Ethan | 11/08/26 | passed | Each seed listing card shows title, vendor name, pickup location, dietary tags, portions remaining, and pickup window. |
| US3 | 3: sorted by pickup end, soonest first | Ethan | 11/08/26 | passed | Seed listings ending 10:25 PM, 11:25 PM, and 12:25 AM appeared in that order. |
| US3 | 4: message when no listings | Ethan | 11/08/26 | passed | With every listing cancelled, ended, or sold out, the page showed "No listings are available right now." instead of a blank page. |
| US4 | 1: reserve portions, get pickup code | Ethan | 11/08/26 | passed | Reserved 2 grain bowls: confirmation page showed a 6-character pickup code and portions remaining went from 8 to 6. Reservation stored as ACTIVE in PostgreSQL. |
| US4 | 2: more portions than remain rejected | Ethan | 11/08/26 | passed | Asked for 2 bakery bags with 1 left: "Not enough portions remaining" error shown, no reservation created, still 1 left. |
| US4 | 3: second reservation on same listing rejected | Ethan | 11/08/26 | passed | Reserved 1 lentil soup, then tried again: "You already have a reservation" error shown, still only one reservation and 5 left. |
| US4 | 4: last portion, only one student wins | Ethan | 11/08/26 | passed | Two students in separate windows reserved the last bakery bag: one got a code, the other an error, and 0 left (not -1). Also ran 20 rounds of truly simultaneous requests from a script: exactly one winner every round, never below 0. |
| US7 | 1: in-window code marks picked up, shows student and portions | | | | |
| US7 | 1b: code after the pickup window rejected | | | | |
| US7 | 2a: unknown code rejected | | | | |
| US7 | 2b: another vendor's code rejected | | | | |
| US7 | 2c: already-used code rejected | | | | |
| US7 | 2d: cancelled code rejected | | | | |
| US7 | 3: ended window shows active reservations as no-show | | | | |
| US8 | 1: only listings with all selected tags shown | | | | |
| US8 | 2: location filter, combinable with tags | | | | |
| US8 | 3: Clear filters shows all available listings | | | | |

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

### US8: Filter listings

Uses the seed data (#53 and #56). Start from fresh data (`docker compose down -v`,
then `docker compose up --build`) and test within 4 hours: the seed listings'
pickup windows end 4 to 6 hours after startup. Log in as Lucky Guy and click
**Browse available listings**. Before filtering, four listings show: Vegetarian
grain bowls (Student Union counter; Vegetarian), Vegan lentil soup (Campus Cafe
counter; Vegan, Gluten-free), `[Demo] Campus Cafe sandwiches` (Campus Cafe
counter; no tags), and Bakery bags (Bakery pickup desk; no tags).

| AC | What to do | What should happen |
| --- | --- | --- |
| 1 | Check **Vegan** and **Gluten-free**, then click **Filter**. Then uncheck Gluten-free, check **Vegetarian**, and click **Filter**. | First: only Vegan lentil soup (`[Demo] Sold-out soup` has the same tags but stays hidden). Second: no listings and a message that none match the filters, because a listing must have every selected tag. The chosen tags stay checked. |
| 2 | Click **Clear filters**. Choose **Campus Cafe counter** and click **Filter**. Then also check **Vegan** and click **Filter**. | First: Vegan lentil soup and `[Demo] Campus Cafe sandwiches`. Second: only Vegan lentil soup. The location stays selected. |
| 3 | With filters applied, click **Clear filters**. | All four available listings show again, with no tags checked and "Any location" selected. |

### US7: Confirm pickup

Uses the extra seed data (#56): vendors Flat Top Grill and Campus Cafe, and
Lucky Guy's reservations on `[Demo] Sold-out soup` (active, 2 portions, window
open), `[Demo] Cancelled bakery bags` (cancelled), and `[Demo] Ended vegetarian
tray` (active, window ended). Start from fresh data (`docker compose down -v`,
then `docker compose up --build`) and run AC 1 within 4 hours: the soup's pickup
window ends 4 hours after startup. Pickup codes are random; look them up with:

`docker compose exec db psql -U campuseats -d campuseats -c "SELECT l.title, u.username AS vendor, r.pickup_code, r.portions, r.status FROM reservations r JOIN listings l ON l.id = r.listing_id JOIN users u ON u.id = l.vendor_id ORDER BY l.title"`

Run the rows in this order: 2a, 2b, 1, 2c, 2d, 1b, 3 (2b needs the soup code still
active; 2c needs it already used).

| AC | What to do | What should happen |
| --- | --- | --- |
| 2a | Log in as Flat Top Grill. Click **Confirm a pickup** on Vendor Home (`/pickups`) and enter `ZZZZZZ` (not in the query output). | Rejected with a message that the code was not found. No reservation changes. |
| 2b | Log out. Log in as Campus Cafe and enter the `[Demo] Sold-out soup` code. | Rejected with a message that the code isn't for one of your listings. The soup reservation is still `ACTIVE`. |
| 1 | Log out. Log in as Flat Top Grill and enter the `[Demo] Sold-out soup` code. | The page shows Lucky Guy and 2 portions to hand out. The query shows the reservation as `PICKED_UP`. |
| 2c | Enter the same soup code again. | Rejected with a message that the code was already used. Status stays `PICKED_UP`. |
| 2d | Enter the `[Demo] Cancelled bakery bags` code. | Rejected with a message that the reservation was cancelled. Status stays `CANCELLED`. |
| 1b | Enter the `[Demo] Ended vegetarian tray` code. | Rejected with a message that the pickup window has ended. The reservation is not marked `PICKED_UP`. |
| 3 | On the same page, look under **Reservations on your listings** for `[Demo] Ended vegetarian tray` (its pickup window has ended). | Lucky Guy's reservation is shown with status "No-show", and the query shows `NO_SHOW`. |
