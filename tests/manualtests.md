#Sprint 1 - US2 Manual test cases

Story: As a vendor, I want to post a surplus food listing with portions and pickup window. 

## Steps before testing: ##
- Run application in Docker Compose
- With vendor and student account
- Use unique listing titles
- Choose dates relative to day the tests are run(No past dates)

## Test 1 - Vendor Posts Listing ##
Acceptance Criteria 1

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
Not run

## Test 2 - Invalid Pickup Times Are Rejected ## 
Acceptance criteria 2

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
Not Run

## Test 3 - Student Opening Posting Page ##
Acceptance Criteria 3

Steps:
1. Log in as a vendor and copy listing page's URL.
2. Make sure to log out.
3. Log in as a student.
4. Paste the URL into the browser and open

Expected result:
Access is denied

Actual result: Not run.


