Date/Time: 11/09/26

Participants: Soul Martin, Ethan Sroka, Caine Mayhew, Jose Torres, Pete Dives

# Did we follow through on Sprint 1's improvements?

- Agree on shared model fields before building on them: Yes! US3, US4, and US7 all built on the shared models without needing to change them, and we updated the class diagram so it matches the real database (PR #64).
- Review PRs as soon as we can: Partly. Our reviews were really thorough, but some approved PRs sat for a few days while we waited on the v1 tag.
- Keep the board updated as work moves: Partly. Some cards hung out in old columns longer than they should have. We also learned that "Closes #N" doesn't close issues on PRs into dev, so a few issues stayed open after their PRs merged.
- Integrate changes sooner: Partly. Branching from dev worked well, and building US4 on top of the US3 branch meant US4 didn't have to wait for US3 to merge. The v1 hold slowed things down though, and two PRs that both added rows to manual-tests.md ran into each other.

What went well:
- We decided every PR would include "How to test it" steps, and we actually stuck to it. That made reviewing and testing each other's work way easier.
- US3 and US4 were tested against every acceptance criterion, including a script that ran the "last portion" race 20 times to make sure only one student ever got it.
- Reviews caught real problems before they got merged, like Selenium tests looking for text the app doesn't show, and the missing CSRF protection.
- Pete picked up the US7 test cases and the US8 bonus partway through the project and got them done quickly.

# What could improve:
- The v1 tag went up 5 days after the release PR merged, and since we'd agreed not to merge into dev until it was tagged, dev was stuck for that whole time.
- We kept each other updated in Discord, but we never found a time where everyone could meet to wrap up Sprint 2 and plan Sprint 3, since everyone was busy and Ethan was out of town.
- Sprint 2 ran past its planned end date, which left us with less time for Sprint 3.

What we'll do differently:
- Tag the release right after the release PR merges, and don't pause dev while we wait.
- Close issues by dragging the card to Done, since the board closes the issue for us.
- If we can't all meet, post a quick end-of-sprint wrap-up in Discord so everyone's on the same page for the next sprint.
- When two PRs both edit manual-tests.md, merge one and update the other from dev right away.