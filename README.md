# django-djpersonnel
Apps for management of personnel and workflows

## PAF workflow

![alt text](https://raw.githubusercontent.com/carthage-college/django-djpersonnel/master/djpersonnel/assets/workflow.jpg)

# Meeting Notes
Workflow:
Ability for supervisor to complete the form electronically

Form will be routed to supervisors VP for approval (When there is information in the compensation box)

Form will be routed to CFO for approval (The CFO is skipped if there is no compensation)

Any new hires or changes in bonus or compensation must also be approved by the CFO 

Form will be routed to HR and Payroll

Notify Supervisor when process is completed

Access to form is limited to supervisors with the authority to fill them out

Approval through email is preferred solution but may be dictated by best practice

Ability to show progress through approval workflow

Ability for the supervisor to timestamp a capture user of major events (creation, approvals, rejections) 

HR is CCed on all forms approved at the end of approval workflow 

Questions:
1. Does termination w/pto pay to you go to CFO?

2. Since CFO occupies 2 roles, should only one approval be needed when approving changes compensation/money for direct reporting relationships

3. Will a copy of the form need to be in Onbase?

4. Does the requester need to be able to electronically sign the document

5. Should HR be required to check receipt? If yes, then who?
