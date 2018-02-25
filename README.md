# django-crmify
A django app for quickly integrating a full-featured 3rd party CRM into an application

## Purpose
To begin, the purpose of crmify is **NOT** to be a full featured CRM. It's utility is as a bridge between a Django application
and a 3rd party CRM. 

## Example Workflows
For the examples below, assume our setup is with the Insightly CRM.
 
*Basic Lead Management*
1. User comes to site and registers for account, this triggers a crmify event to create a lead in Insightly
2. User unregisters account, this sets the lead status to the value of `settings.BACKEND_OPTIONS.LEAD_DEAD_STATUS`

*Basic Sales Funnel*
1. User comes to site and registers, triggers crmify to create a lead
2. User makes a purchase, this sets the lead status to the value of `settings.BACKEND_OPTIONS.LEAD_CONVERTED_STATUS`