# List of Test Cases

| Seq | Test Case ID & Name | Feature / Requirement | Description |
| :--- | :--- | :--- | :--- |
| 1 | **TC-01:** Create a valid academic profile | F-01 / FR-01 / U001 | Verify that a complete and valid academic profile can be saved. |
| 2 | **TC-02:** Reject missing required profile info | F-01 / FR-01 / U001 | Verify validation error handling when mandatory profile fields are omitted. |
| 3 | **TC-03:** Validate target credit-load boundaries | F-01 / FR-01 / U001 | Verify acceptance of 14 and 24 credits, and rejection of 13 and 25 credits. |
| 4 | **TC-04:** Handle unavailable curriculum mapping | F-01 / FR-01 / U001 | Verify system behavior and warning when no curriculum matches program/intake. |
| 5 | **TC-05:** Update an existing academic profile | F-01 / FR-01 / U001 | Verify that existing profile fields update cleanly without creating duplicate records. |
| 6 | **TC-06:** Add a valid Passed course attempt | F-02 / FR-02 / U002 | Verify that a passed attempt contributes to earned credits and prerequisite satisfaction. |
| 7 | **TC-07:** Record Failed and InProgress attempts | F-02 / FR-02 / U002 | Verify that failed and in-progress attempts do not grant credits or satisfy prerequisites. |
| 8 | **TC-08:** Reject an unknown course | F-02 / FR-02 / U002 | Verify rejection when an entered course code does not exist in the catalog. |
| 9 | **TC-09:** Reject missing grade or credit info | F-02 / FR-02 / U002 | Verify validation failure when attempt grade or credit fields are missing. |
| 10 | **TC-10:** Validate attempt-number boundaries | F-02 / FR-02 / C3 | Verify attempt number must be an integer >= 1 (rejecting 0). |
| 11 | **TC-11:** Validate earned-credit boundaries | F-02 / FR-02 / C3 | Verify that earned credits cannot be negative (< 0). |
| 12 | **TC-12:** Calculate progress from mixed attempts | F-06 / FR-08 / U003 | Verify that only Passed attempts increment cumulative graduation progress. |
| 13 | **TC-13:** Evaluate required-credit boundary | F-06 / FR-08 / U003 | Verify evaluation at boundary (required credits minus one vs. exact credits). |
| 14 | **TC-14:** Detect missing required courses | F-06 / FR-08 / U003 | Verify graduation is blocked when required courses are missing despite sufficient credits. |
| 15 | **TC-15:** Confirm completed graduation status | F-06 / FR-08 / U003 | Verify graduation completion when all credits and required courses are satisfied. |
| 16 | **TC-16:** Validate course without prerequisites | F-05 / FR-07 / U003 | Verify that a base course with zero prerequisites passes eligibility checks. |
| 17 | **TC-17:** Validate satisfied prerequisites | F-05 / FR-07 / U003 | Verify course eligibility when required prerequisites have Passed attempts. |
| 18 | **TC-18:** Validate unsatisfied prerequisite checks | F-05 / FR-07 / U003 | Verify ineligible status for failed, in-progress, or unattempted prerequisites. |
| 19 | **TC-19:** Handle uncertain prerequisite data | F-05 / FR-07 / U003 | Verify warning generation when prerequisite definitions are incomplete. |
| 20 | **TC-20:** Validate course offering availability | F-04 / FR-06 / U003 | Verify section lookup for offered courses and handling of unoffered courses in a term. |
| 21 | **TC-21:** Login success | RBAC / SCR-01 | Verify successful authentication and routing to Student/Advisor/Admin dashboards. |
| 22 | **TC-22:** Login failed | RBAC / SCR-01 | Verify that invalid credentials display an error and deny dashboard access. |
| 23 | **TC-23:** Reset password | RBAC / SCR-01 | Verify that password reset mechanisms handle forgot-password requests. |
| 24 | **TC-24:** View submitted study plan | FR-15 / U004 / SCR-08 | Verify an advisor can access and inspect a student's submitted study plan. |
| 25 | **TC-25:** View student academic info | FR-15 / U004 / SCR-09 | Verify an advisor can view student GPA, credit count, and academic profile. |
| 26 | **TC-26:** Provide plan feedback comments | FR-15 / U004 / SCR-09 | Verify an advisor can submit feedback comments attached to a plan. |
| 27 | **TC-27:** Approve suitable study plans | FR-15 / U004 / SCR-09 | Verify that an advisor can mark a plan as Approved and update its state. |
| 28 | **TC-28:** Request study plan revision | FR-15 / U004 / SCR-09 | Verify that an advisor can set a plan to Revision Requested with mandatory comment. |
| 29 | **TC-29:** Record fallback execution actions | FR-17 / NFR-07 / C10 | Verify fallback activation and logging when the external AI provider is unreachable. |
| 30 | **TC-30:** Save study plan as Draft | FR-22 / C8 / SCR-06 | Verify a student can save an unsubmitted plan in Draft status. |
| 31 | **TC-31:** Submit Draft plan for review | FR-22 / C8 / SCR-06 | Verify transition of a plan from Draft to PendingReview status in advisor queue. |
| 32 | **TC-32:** View plan version history | FR-23 / SCR-07 | Verify a student can view chronological history of all saved and submitted plans. |
| 33 | **TC-33:** View review status and decisions | FR-23 / SCR-02 / SCR-07 | Verify student UI displays advisor approval or revision decision with comments. |
| 34 | **TC-34:** Create new revision without overwriting| FR-23 / C8 / U004 | Verify that revising a plan creates a new draft version without deleting old records. |