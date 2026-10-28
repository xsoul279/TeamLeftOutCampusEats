| User story | Acceptance criterion | Tester | Date | Result | Notes |
| --- | --- | --- | --- | --- | --- |
| US1 | 1: When on the registration page, entering a name, unique email, password of at least 8 characters, and selecting a valid role ('vendor', or 'student') will store my account in PostgreSQL and I am then redirected to the login page. | Caine | 10/27/26 | passed | fixed error where username wasn't being passed - mismatch in the templates. Fixed and registering is now working |
| US1 | 2: A duplicated email is rejected and an error message is shown | Caine | 10/27/26 | passed | duplicate email is rejected and the message "Email is already registered" is displayed. |
| US1 | 3: Account is not created if a required field is empty and the empty field is identified | Caine | 10/27/26 | passed | tested for each field and all of them at once - all properly display error messages individually and when all are blank, displays all error messages for every field. |
| US1 | 4: Passwords are stored hashed, not in plain text | Caine | 10/27/26 | passed | checked that passwords are properly hashed - will attach below |
| US1 | 5: If an account exists and the correct user/pass are entered, user is redirected to the home page for selected role. If wrong pass, an error message is displayed | Caine | 10/27/26 | passed | tested for email/pass error message works. Tested directly after registering, everything correctly saved. |


id |    username    |           email            |  role   |                                                                           password_hash                                                                            
| 1 | Flat Top Grill | flattopgrill@msudenver.edu | vendor  | scrypt:32768:8:1$PUs4wq9KwXAE7BqZ$7fbbf0b3ea8ccb680a45943aab14d6414cfc567eee76ce4de27f2ae8153bdce1fba9c5dbb51408920af5e777f8dcab5bf1ef497fd0eee19abe0d242ee6660a28 |
| 2 | Lucky Guy   | identityv@msudenver.edu    | student | scrypt:32768:8:1$iJzlcitFV5K9aEld$e9314e7b90e76e062635a273136e3fe903d3bf3b0a96f73def8bad31da5a8187a033b39151c19578773438381036a10e14590d1d2faf8de0aecce65e462dad76 |
| 3 | Caine    | luciferseve@gmail.com      | student | scrypt:32768:8:1$RIl5aGONMllGf88B$81e73e174bc2cb854a98391883578bc189e597410e963e36758576e8726215869301a8eec9ccfe8923996a4c301b2966607891b4aca62a53c06fcd05eab27acc |
(3 rows)
