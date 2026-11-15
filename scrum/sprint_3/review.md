Date/Time: 11/15/26

Participants: Soul Martin, Ethan Sroka, Caine Mayhew, Jose Torres, Pete Dives

# Planned Work:

Our goal for Sprint 3 was to finish US5 Manage listings, US6 My reservations, and US7 Confirm pickup. These added up to 11 points. We also needed to finish US8 filtering and the Selenium work carried over from Sprint 2.

# Completed Work:

US5 Manage listings merged November 14 in PR #72. Vendors can view and edit their own listings, see who reserved portions, and cancel listings. They cannot lower the total below the number already reserved or access another vendor's listings. All five acceptance criteria were recorded as passed.

US6 My reservations merged November 14 in PR #68, with manual results in PR #69. Students can view their reservations and cancel active ones before the pickup window ends. Cancelling returns the portions to the listing. All three acceptance criteria were recorded as passed.

US7 Confirm pickup merged November 10 in PR #62, with manual results merged November 14 in PR #67. Vendors can enter a pickup code and see the student and portions to hand out. Invalid, used, cancelled, expired, and other-vendor codes are rejected. Ended active reservations become no-shows. The acceptance checks were recorded as passed.

US8 filtering carried over from Sprint 2 and merged November 12 in PR #66. Its manual results merged November 14 in PR #70. Students can combine dietary tags and location filters and clear them to see all available listings. All three acceptance criteria were recorded as passed.

We also finished:

- The US1 Selenium test, merged November 14 in PR #54.
- The Selenium run instructions, merged November 14 in PR #73.
- The US7 sequence diagram, merged November 10 in PR #60.
- A reported manual walkthrough of US1–US8 in Docker.
- A successful Selenium run on November 15.

# Challenges:

Carryover from Sprint 2 left more work for the final sprint than originally planned. We also had conflicts where branches changed the same reservation code and manual test file.

We ran into some time management issues, especially during the end. We tried to finish up carried over components from Sprint 2, and ended up getting behind on Sprint 3 at many points. 

# Sprint Outcome:

The required US5, US6, and US7 features are merged, along with US8 filtering and the Selenium work. The app now supports the full flow from posting food to reserving, cancelling, and collecting it. The remaining work is to finish the optional stories and the final release evidence.
