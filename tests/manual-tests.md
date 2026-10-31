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
