# django-djpersonnel
Apps for management of personnel and workflows

## PAF workflow

![alt text](https://raw.githubusercontent.com/carthage-college/django-djpersonnel/master/djpersonnel/assets/workflow.jpg)

# Meeting Notes
Workflow:
Ability for supervisor to complete the form electronically

Form will be routed to supervisors for approval (When there is information in
the compensation box)

Form will be routed to CFO for approval (The CFO is skipped if there is no
compensation)

Any new hires or changes in bonus or compensation must also be approved by the
CFO

Form will be routed to HR

Notify Supervisor when process is completed

Access to form is limited to supervisors with the authority to fill them out

Approval through email

Ability to show progress through approval workflow

Ability for the supervisor to timestamp a capture user of major events (
creation, approvals, rejections)

HR is CCed on all forms approved at the end of approval workflow

# From Abby Heinrichs

Typically department chairs will make hires. This would then be approved by the
Dean. There are four individuals with this level of approval. Corinne Ness,
Deanna Byrnes, Jackie Easley, and Bill Miller. It is unrealistic to think that
David Timmerman would have the time to approve all of these forms.
David should have a way to see the faculty PAFs on the dashboard but should not
be bothered with the administrative stuff.

There could be many people that fill out one of these forms but they should
only be approved by the VP's and then the 4 Deans. They are the only ones that
can send through new hires.

Example:

Psychology department hires a new adjunct. Leslie cameron fills out all of the
info as she is the one that knows the most about the person that she
interviewed, then she would select to have it approved by her supervisor who is
Deanna Byrnes. Deanna can say yep this looks good or nope something has to
change.

# Form Matrix
Staff and New Hire are selected

Position Title
Hidden unless "faculty or staff and newhire_rehire" is checked
dB field = position_title

Status Type (Full-Time/Part-Time)
Hidden unless "staff and newhire_rehire" is checked
dB field = status_type

Hire Type (New Hire/Rehire)
Hidden unless "faculty or staff" is checked
dB field = hire_type

Pay Classification (Exempt/Non-exempt)
Hidden unless "faculty or staff and newhire_rehire" is checked
dB field = pay_type

**If 'Non Exempt (hourly)', provide the hours per week this position will work
db = hours_per_week

New Compensation
Hidden unless "staff and newhire_rehire" is checked
dB field = new_compensation

Expected Start Date
Hidden unless "faculty or staff and newhire_rehire" is checked
dB field = expected_start_date

Budget Account
Hidden unless "faculty or staff and newhire_rehire" is checked
dB field = budget_account

Supervise Others
Hidden unless "staff and newhire_rehire" is checked
dB field = supervise_others

Standard Vacation Package
Hidden unless "staff and newhire_rehire" is checked
dB field = standard_vacation_package

**If 'No', provide how many vacation days
db = vacation_days

Position Grant Funded
Hidden unless "faculty or staff and newhire_rehire" is checked
dB field = position_grant_funded

**If 'Yes', provide the grant number and grant amount or percentage
db = grant_number

**If 'Yes', provide the grant amount or percentage
db = grant_amount

Moving Expenses
Hidden unless "faculty or staff and newhire_rehire" is checked
dB field = moving_expenses

**If 'Yes', provide how much
db = moving_expenses_amount

Other Arrangements
Hidden unless "staff and newhire_rehire" is checked
dB field = other_arrangements

---------------------------------------------------------------

Faculty and New Hire are selected

Position Title
Hidden unless "faculty or staff and newhire_rehire" is checked
dB field = position_title

Employment Type
Hidden unless "faculty and newhire_rehire" is checked
dB field = employment_types

If they select (contract-ongoing or contract-terminal)
Number of years?
dB field = contract_years

If they select "Adjunct"
Music (Yes/No)
dB field = music

If "Yes" then show
Courses Teaching
dB field = courses_teaching

Number of Credits
dB field = number_of_credits

Teaching Appointment
Hidden unless "faculty and newhire_rehire" is checked
dB field = teaching_appointment

If they select "Other" then show Teaching appointment arrangements
dB field = teaching_appointment_arrangements

Hire Type (New Hire/Rehire)
Hidden unless "faculty or staff" is checked
dB field = hire_type

Pay Classification (Exempt/Non-exempt)
Hidden unless "faculty or staff and newhire_rehire" is checked
dB field = pay_type

Program Types
Hidden unless "faculty and newhire_rehire" is checked
dB field = program_types

Moving Expenses (Yes/No)
Hidden unless "faculty or staff and newhire_rehire" is checked
dB field = moving_expenses

** If 'Yes', provide how much
db = moving_expenses_amount

Startup Expenses (Yes/No)
Hidden unless "faculty and newhire_rehire" is checked
dB field = startup_expenses

**If 'Yes', provide how much
db = startup_expenses_amount

Position Grant Funded
Hidden unless "faculty or staff and newhire_rehire" is checked
dB field = position_grant_funded

**If 'Yes', provide the grant number and grant amount or percentage
db = grant_number

**If 'Yes', provide the grant amount or percentage
db = grant_amount

Expected Start Date
Hidden unless "faculty or staff and newhire_rehire" is checked
dB field = expected_start_date

Budget Account
Hidden unless "faculty or staff and newhire_rehire" is checked
dB field = budget_account

---------------------------------------------------------------

Faculty or Staff and Department Change are selected
Old Department
Hidden unless "faculty or staff and department change" is checked
dB field = old_department

New Department
Hidden unless "faculty or staff and department change" is checked
dB field = new_department

---------------------------------------------------------------

Faculty or Staff and Compensation Change are selected
Current Compensation
Hidden unless "faculty or staff and compensation change" is checked
dB field = current_compensation

New Compensation
Hidden unless "faculty or staff and compensation change" is checked
dB field = new_compensation

Salary Change Reason
Hidden unless "faculty or staff and compensation change" is checked
dB field = salary_change_reason

Effective Date
Hidden unless "faculty or staff and compensation change" is checked
dB field = compensation_effective_date

Temporary Interim Pay
Hidden unless "faculty or staff and compensation change" is checked
dB field = temporary_interim_pay

End Date
<!-- Hidden unless Temporary Interim Pay checked "Yes" -->
dB field = end_date

---------------------------------------------------------------

Faculty or Staff and Onetime Payment are selected
Amount
Hidden unless "faculty or staff and onetime payment" is checked
dB field = amount

Amount Reason
Hidden unless "faculty or staff and onetime payment" is checked
dB field = amount_reason

Pay After Date
Hidden unless "faculty or staff and onetime payment" is checked
dB field = pay_after_date

Department Account Number
Hidden unless "faculty or staff and onetime payment" is checked
dB field = department_account_number

Grant Pay Name
Hidden unless "faculty or staff and onetime payment" is checked
dB field = grant_pay

Grant Pay Account Number
Hidden unless Grant Pay checked "Yes"
dB field = grant_pay_account_number

---------------------------------------------------------------

Faculty or Staff and Supervisor Change are selected
Old Supervisor
Hidden unless "faculty or staff and supervisor change" is checked
dB field = old_supervisor

New Supervisor
Hidden unless "faculty or staff and supervisor change" is checked
dB field = new_supervisor

---------------------------------------------------------------

Staff, Termination and Voluntary are selected
Voluntary/Involuntary (Voluntary/Involuntary)
Hidden unless "staff and termination" is checked
dB field = voluntary_involuntary_termination

Voluntary Reason for Leaving (Select List)
Hidden unless "staff, termination and "voluntary" is checked
dB field = staff_leaving_voluntary_types

Involuntary Reason for Leaving (Select List)
Hidden unless "staff, termination and "voluntary" is checked
dB field = staff_leaving_involuntary_types

Last Day
Hidden unless "staff and termination" is checked
dB field = last_day_date

Remaining vacation days accrued
Hidden unless "staff and termination" is checked
dB field = vacation_days_accrued

Property to be returned
Hidden unless "staff and termination" is checked
dB field = returned_property

Eligible for rehire (Yes/No)
Hidden unless "staff and termination" is checked
dB field = eligible_rehire

---------------------------------------------------------------

Faculty, Termination and Voluntary are selected

Voluntary/Involuntary (Voluntary/Involuntary)
Hidden unless "staff and termination" is checked
dB field = voluntary_involuntary_termination

Voluntary Reason for Leaving (Select List)
Hidden unless "faculty, termination and "voluntary" is checked
dB field = faculty_leaving_voluntary_types

Involuntary Reason for Leaving (Select List)
Hidden unless "faculty, termination and "voluntary" is checked
dB field = faculty_leaving_involuntary_types

Last Day
Hidden unless "faculty and termination" is checked
dB field = last_day_date

Remaining vacation days accrured
Hidden unless "faculty and termination" is checked
dB field = vacation_days_accrued

Property to be returned
Hidden unless "faculty and termination" is checked
dB field = returned_property

Eligible for rehire (Yes/No)
Hidden unless "faculty and termination" is checked
dB field = eligible_rehire

---------------------------------------------------------------

Staff and Status Change are selected

Status Type (Full-Time/Part-Time)
Hidden unless "staff and status change" is checked
dB field = status_type

New Supervisor
Hidden unless "staff and status change" is checked
dB field = status_change_effective_date

---------------------------------------------------------------

Position/Title Change  are selected

Old Position/Title
Hidden unless "faculty or staff and position change" is checked
dB field = old_position

New Position/Title
Hidden unless "faculty or staff and position change" is checked
dB field = new_position

Position Effective Date
Hidden unless "faculty or staff and position change" is checked
dB field = position_effective_date

Additional Supervisory Role
Hidden unless "faculty or staff and position change" is checked
dB field = additional_supervisor_role

Who do you supervise
Hidden unless Additional Supervisory Role checked "Yes"
dB field = direct_reports

---------------------------------------------------------------

Faculty or Staff and Leave of Absence  are selected
Date out on Leave
Hidden unless "faculty or staff and leave of absence" is checked
dB field = leave_of_absence_date

Expected Date of Return
Hidden unless "faculty or staff and leave of absence" is checked
dB field = expected_return_date

Reason for Leave
Hidden unless "faculty or staff and leave of absence" is checked
dB field = leave_of_absence_reason

---------------------------------------------------------------

Faculty and Sabbatical  are selected
Semester
Hidden unless "faculty and sabbatical" is checked
dB field = sabbatical_types

Academic Year
Hidden unless "faculty and sabbatical" is checked
dB field = academic_year

