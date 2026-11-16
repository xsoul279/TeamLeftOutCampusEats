Date/Time: 11/09/26

Participants: Soul Martin, Ethan Sroka, Caine Mayhew, Jose Torres, Pete Dives

# Planned Work:

Our goal for Sprint 2 was to let students browse available listings (US3, 2 points) and reserve portions (US4, 5 points), with the US8 filter bonus (2 points) if US3 finished early. That was 9 story points. We also planned to finish the US1 Selenium test, re-test US1 and US2, add more seed data, and write the US5, US6, and US7 test cases so Sprint 3 could start right away.

# Completed Work:

US3 Browse listings was merged in PR #59. Students see only listings that haven't ended, aren't cancelled, and have portions left, sorted by soonest pickup end, with a message when nothing is available. All 4 US3 acceptance criteria passed in manual testing.

US4 Reserve portions was merged in PR #63. Students can reserve 1 or 2 portions and get a unique 6-character pickup code on a confirmation page. Asking for too many portions, reserving the same listing twice, or reserving a cancelled or ended listing all show an error. For the "last portion" criterion, the listing row is locked while a reservation is made, and a script that sent two students' requests at the exact same moment for 20 rounds always had exactly one winner. All 4 US4 acceptance criteria passed.

We also merged:
- More seed data for testing: ended, cancelled, and sold-out listings and a second vendor (PR #56)
- The US1 and US2 re-test in Docker (PR #55)
- The US7 manual test cases (PR #58) and the fixed US7 sequence diagram (PR #60)
- An updated class diagram that matches the actual database (PR #64)

Release v2 contains US3 and US4 (PR #71, tagged v2).

Completed: 7 of 9 planned story points.

# Not Completed (moved to Sprint 3):

- US8 Filter listings (bonus): built during Sprint 2 on top of US3, but it could only open for review once US3 merged. Merged in Sprint 3 (PR #66).
- US1 Selenium test (PR #54): went through three rounds of review because the expected messages and page titles didn't match the app. Approved in Sprint 3.
- US6 test cases and the README steps for running the Selenium test.

# Challenges:

Release v1 was merged on Nov 3 but not tagged until Nov 8. We had agreed not to merge anything into dev until v1 was tagged, so several approved PRs sat waiting for days and Sprint 2 ran past its planned end date.

During review of US4, Jose found that the app's forms have no CSRF protection. It was a good catch, but it was outside the scope of this project: it affects every form in the app, isn't part of any acceptance criteria, and isn't in the rubric, so we agreed not to hold up the stories that depend on US4 for it. If we had more time, we would add CSRF protection across the whole app.

# Sprint Outcome:

Sprint 2 delivered both required stories, US3 and US4, which unblocked US5, US6, and US7 for Sprint 3. For Sprint 3 we're focusing on US5 Manage listings, US6 My reservations, and US7 Confirm pickup, plus finishing US8 and the Selenium test.
