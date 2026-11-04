# US5: Manage listings - manual test cases

These are planned cases for README acceptance criteria US5.1-US5.5 (issue #19).
No application results have been recorded. Execute them for issue #31 after
US5 is implemented; writing the cases does not mean US5 has passed.

## Prerequisites

- US1, US2, and US4 must be merged into `dev` and passing before US5 implementation
  or execution. Test against PostgreSQL in the Docker Compose deployment started
  with `docker compose up --build`.
- Use a disposable test deployment with two vendors, Vendor A and Vendor B, and
  two students, Student One and Student Two. Use separate browser profiles or
  private sessions for each role so accounts do not overwrite each other's login.
- Create the fixtures below through the implemented UI or documented seed setup.
  Record their actual IDs, URLs, pickup times, and starting counts. Do not assume
  numeric IDs or route names. Use the application's timezone for pickup times.
- Recreate or restore the affected fixtures before each case. For future windows,
  allow enough time to complete the case before the end. To prepare an ended
  listing, create a valid short window and let it end, or use documented fixtures.
  Do not try to create a past-ended listing through US2, which must reject it.
- If a dependency or fixture is unavailable, record `blocked` with the reason.
  Do not record `passed` from this document or from a page merely loading.

## Fixtures

| Reference | Owner | Initial state | Total portions | Reservations | Remaining |
| --- | --- | --- | --- | --- | --- |
| A-Free | Vendor A | Active, pickup end in the future | 8 | None | 8 |
| A-Reserved | Vendor A | Active, pickup end in the future | 8 | Student One: 2 active portions; Student Two: 1 active portion | 5 |
| A-Ended | Vendor A | Pickup end in the past, never cancelled | 4 | None | 4 |
| A-Cancelled | Vendor A | Cancelled, pickup end in the future | 6 | None | Record after cancellation |
| B-Private | Vendor B | Active, pickup end in the future | 7 | Student One: 1 active portion | 6 |

Create A-Cancelled with the implemented cancellation flow. Record both students'
reservation IDs and codes for A-Reserved before editing or cancellation. Do not
publish real account credentials or pickup codes in test evidence.

## Acceptance coverage

| Case | AC | What to do | Expected result |
| --- | --- | --- | --- |
| US5-1 | 1 | As Vendor A, open My Listings with all Vendor A fixtures present; compare statuses and counts, then reload. | All four own listings appear: A-Free and A-Reserved are active, A-Ended is ended, and A-Cancelled is cancelled. Reserved/remaining counts are 0/8, 3/5, and 0/4 for the first three fixtures; A-Cancelled matches its recorded counts after cancellation. B-Private is absent. |
| US5-2 | 2 | Edit A-Free with valid changed fields, then repeat each invalid-input variant below from a restored fixture. | Valid changes persist after reload and a new login. Invalid edits show an error, preserve the saved listing, and do not create a new listing. |
| US5-3 | 3 | With 3 portions reserved on A-Reserved, try totals of 2, 3, and 10, restoring the fixture before each attempt. | Total 2 is rejected without changes (8 total, 3 reserved, 5 remaining). Total 3 saves with 3 reserved and 0 remaining. Total 10 saves with 3 reserved and 7 remaining. Both original reservations and their codes are preserved. |
| US5-4 | 4 | As Vendor A, cancel A-Reserved; inspect the student listings view and both persisted reservations, then reload and log in again. | The listing is cancelled and no longer appears to students. Both active reservations become cancelled, with no active reservation left on that listing. B-Private and its reservation remain unchanged. |
| US5-5 | 5 | Open A-Reserved as Vendor A; then attempt to view, edit, and cancel B-Private using its recorded URLs and requests. | The owned listing shows Student One with 2 portions and Student Two with 1 portion. Vendor A cannot read or change B-Private or its reservation details; Vendor B still sees the original values. |

## US5-2: Edit validation variants

For the valid edit, change the title, description, pickup location, and future
pickup window, set portions to 10, and choose vegetarian and gluten-free tags.
Reopen the listing and verify every changed field, both tags, Vendor A ownership,
0 reserved, and 10 remaining. Also save once with no dietary tags; zero tags is
valid under US2. Check valid portion boundaries of 1 and 100 on a free listing.

Repeat each invalid edit independently, with all other values valid. Compare
saved fields and counts before and after each rejected request, including after
reload. When browser input validation blocks submission, also submit the value
to the server using the edit request to verify server-side validation.

| Variant | Value to submit | Expected result |
| --- | --- | --- |
| Portions below range | 0 | Error; stored total and remaining stay 8. |
| Portions above range | 101 | Error; stored total and remaining stay 8. |
| Non-integer portions | A fractional value such as 1.5, then nonnumeric text | Each is rejected without changing the listing. |
| Reversed pickup window | End before start, with both times in the future | Error; the original window is preserved. |
| End in the past | Start two hours ago, end one hour ago | Error; the original window is preserved. |

## US5-4: Cancellation checks

Check that **both** active reservations change status; checking only the listing
badge is insufficient. Read reservation status through the current management
interface or a read-only PostgreSQL query filtered to the recorded listing ID.
Record the check used. This does not require waiting for the US6 My Reservations
page. Do not change reservation rows manually to make the test pass.

As each student, refresh the available listings page and try the previously
recorded reserve request for the cancelled listing. It must create no active
reservation. Also cancel a restored A-Free fixture with no reservations: the
listing becomes cancelled and disappears from student availability without an
error. These checks must leave Vendor B's fixture unchanged.

## US5-5: Ownership checks

Capture B-Private's detail and edit URLs, update request, and cancel request while
logged in as Vendor B. Then log in as Vendor A and test the direct detail URL,
the direct edit URL, and both mutation requests for B-Private. Use Vendor A's own
valid form/session token if CSRF protection is present, so rejection actually
checks ownership. Hiding a link or rejecting an invalid form token alone does
not establish authorization.

Every attempt must be denied or return not found, disclose no private listing or
student details, and leave the listing, counts, and reservations unchanged. Log
in as Vendor B to verify that state. Repeat unauthorized access to My Listings,
detail, edit, and cancel as a student and while logged out; require denial or a
login redirect with no change to persisted data.

## Recording execution

When the prerequisites are ready, add one result per acceptance criterion to
`tests/manual-tests.md` using the project's required columns below. Reference the
case ID in Notes, record the tested commit and actual fixture IDs, and link any
failure to its issue. All variants for a criterion must pass before its result
is `passed`; retain earlier dated runs when re-testing before a release.

| User story | Acceptance criterion | Tester | Date | Result | Notes |
| --- | --- | --- | --- | --- | --- |
| US5 | 1: own listings, statuses, and portion counts | | | not run | US5-1 |
| US5 | 2: edit without reservations, applying US2 validation | | | not run | US5-2; run every validation variant |
| US5 | 3: portions cannot drop below the reserved count | | | not run | US5-3; rejected and boundary totals |
| US5 | 4: cancellation hides the listing and cancels active reservations | | | not run | US5-4; check both reservations |
| US5 | 5: reservation names/portions and vendor ownership | | | not run | US5-5; direct reads and mutations |
