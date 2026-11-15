# US6; Reservations and Cancellations
Test cases for US6 following the listed acceptance criterion.

# Acceptance Criterion:

|Case| AC | What to Do | Expected Result |
| --- | --- | --- | --- |
|US6-1 | 1 | Login as a student using seed account. Navigate to "My Reservations" and open. | All student reservations should be displayed with listing title, vendor, location, pickup window, portions, pickup code, and current status. Statuses include active, picked up, cancalled, no-show. |
|US6-2 | 2 | Login as a student and view reservations. Click the cancellation button next to a reservation with an active status and a valid pickup window. | The status of the reservation should switch to 'cancelled' and the portions allocated to that reservation are returned to the listings. |
|US6-3 | 3 | Login as a student and open/view your reservations. Check the reservations not labeled active and try to cancel it. | There should be no cancellation option next to any reservation without an active status, and all 

