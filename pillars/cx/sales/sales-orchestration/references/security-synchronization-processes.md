# Sales Orchestration Security Synchronization Processes

## Contents

- [Purpose and Boundary](#purpose-and-boundary)
- [Retrieve Latest LDAP Changes](#retrieve-latest-ldap-changes)
- [Import User and Role Application Security Data](#import-user-and-role-application-security-data)
- [Sequence and Readiness](#sequence-and-readiness)
- [Sources](#sources)

## Purpose and Boundary

Use these instructions for Sales Motion, Sales Plays and Content, and Data
Capture Rules security-readiness questions. They explain how an authorized
administrator runs or schedules the required security synchronization
processes. The three task skills are read-only: they may return these steps but
must not submit, schedule, poll, or retry an ESS process.

Read `security-console-role-provisioning.md` first when the question involves
the profile option, predefined-role enablement, custom-role permission groups,
security views, privileges, duty roles, or data security policies.

Navigation labels can vary by offering and release. Use the exact process and
task names below. In the Sales offering, the **Run User and Roles
Synchronization Process** task may appear under **Users and Security**; in
other implementation flows it may appear under **Initial Users**.

## Retrieve Latest LDAP Changes

The **Retrieve Latest LDAP Changes** process copies user, role, and role
assignment data from the LDAP directory to the Oracle Fusion Applications
Security tables. Run it once before implementation begins. After the initial
run, synchronization occurs automatically. Also consider running it after a
release update or when LDAP and application-security data appear inconsistent.

### Setup and Maintenance task path

1. Open the **Setup and Maintenance** work area.
2. Go to the **Run User and Roles Synchronization Process** task. Depending on
   the offering and release, find it in the **Initial Users** functional area
   or under **Sales** > **Users and Security**.
3. On the process submission page, optionally select **Notify me when this
   process ends**.
4. Select **Submit**.
5. Review the confirmation message and select **OK**.
6. Confirm that the submitted **Retrieve Latest LDAP Changes** process
   completes successfully before relying on the synchronized data.

### Direct Scheduled Processes path

Use this current-release path when the Setup and Maintenance task isn't
available:

1. Sign in with an authorized security-administration role, such as the IT
   Security Manager job role.
2. Open the **Scheduled Processes** work area.
3. In the **Search Results** section of the Overview page, select **Schedule
   New Process**.
4. In the **Name** field, search for and select **Retrieve Latest LDAP
   Changes**.
5. Select **OK**.
6. In the **Process Details** dialog box, select **Submit**.
7. Select **OK**, and then select **Close**.
8. Refresh the Scheduled Processes page periodically until the process reaches
   a terminal status.
9. Confirm that it completed successfully. Only one instance of **Retrieve
   Latest LDAP Changes** can run at a time.

## Import User and Role Application Security Data

The **Import User and Role Application Security Data** process imports users,
roles, privileges, and data security policies from the identity store, policy
store, and Oracle Fusion Applications Security tables. After the first
successful run, schedule it to run daily so the Security Console remains
current.

1. Open the **Scheduled Processes** work area.
2. In the **Search Results** section of the Overview page, select **Schedule
   New Process**.
3. In the **Schedule New Process** dialog box, search for and select **Import
   User and Role Application Security Data**.
4. Select **OK**.
5. In the **Process Details** dialog box, select **Advanced**.
6. On the **Schedule** tab, set **Run** to **Using a schedule**.
7. Set **Frequency** to **Daily** and **Days Between Runs** to **1**.
8. Enter the start and end dates and times. Set the start time after the daily
   **Send Pending LDAP Requests** process is expected to complete.
9. Select **Submit**.
10. Select **OK** to close the confirmation message.
11. Confirm that the initial run and subsequent scheduled runs complete
    successfully before relying on imported role, privilege, or data-security
    changes.

## Sequence and Readiness

1. Run **Retrieve Latest LDAP Changes** once before implementation to initialize
   the application-security tables from LDAP.
2. After a permission-group, role, or privilege change, allow the applicable
   **Send Pending LDAP Requests** run to complete.
3. Run or wait for the subsequent **Import User and Role Application Security
   Data** process. Its daily start time must follow the daily **Send Pending
   LDAP Requests** process.
4. Do not report the security change as ready for verification until the
   required synchronization and import processes complete successfully.

**Retrieve Latest LDAP Changes** is an inbound LDAP synchronization process;
it does not replace **Send Pending LDAP Requests** in the post-change sequence.

## Sources

- Oracle Sales: `https://docs.oracle.com/en/cloud/saas/sales/fasry/synchronize-user-and-role-information.html`
- Oracle Applications Common 26C: `https://docs.oracle.com/en/cloud/saas/applications-common/26c/facsa/retrieve-latest-ldap-changes.html`
- Oracle Applications Common 26C: `https://docs.oracle.com/en/cloud/saas/applications-common/26c/faser/schedule-the-import-user-and-role-application-security-data.html`
