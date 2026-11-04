# Platform verification

Track A Sprint 1 checks for issues #5 and #6. Tested by Rinkatur5 on
2026-10-29 against the Docker Compose deployment with PostgreSQL 17 and Python
3.13. The isolated project was `campuseats-a5-check`, using port 15005 and its
own disposable volume. The normal development project's data was not reset.

| Check | Procedure | Result |
| --- | --- | --- |
| Fresh startup | Build and start with an empty volume; wait for both services to become healthy. | Passed: HTTP 200; 2 demo users, 3 listings, and 1 completed seed record. |
| Seed logins | Submit each README email/password to `/login` over HTTP and follow the redirect. | Passed: both reached `/home` for their role; vendor could open `/listings/new`, student received 403. |
| Sample data | Inspect persisted users and listings in the test database. | Passed: hashed passwords; 8, 6, and 5 portions; vendor ownership; locations; zero/one/two tags; future, ordered pickup windows. |
| Repeat initialization | Run `docker compose exec web flask seed`, restart services, then recreate containers with `down` and `up` without removing the volume. | Passed: no duplicates; changed vendor name/password, edited listing title, remaining portions, and its reservation persisted. |
| Existing database | Start with an unrelated student, an existing demo vendor with a changed password, and an existing listing; run two seed commands concurrently. | Passed: missing demo student and three samples were added once; existing records and password were preserved. |
| Conflict rollback | Try a conflicting demo email role, a conflicting username, and a student email conflict after a new vendor is created. | Passed: each operation failed without leaving partial users, listings, or a seed record. |
| Fresh reset | Run `down -v` on the disposable project only, then start again. | Passed: both README logins and the three sample listings were recreated automatically. |
| Runtime | Check dependencies with `python -m pip check` and inspect the web user. | Passed: dependency resolution clean; UID 10001. |

The README setup and credentials were verified by the author. Issue #6's
independent teammate walkthrough remains part of PR review. These checks do not
replace the separate story acceptance results in `tests/manual-tests.md`.
