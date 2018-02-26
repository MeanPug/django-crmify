# django-crmify
A django app for quickly integrating a full-featured 3rd party CRM into an application

## Purpose
To begin, the purpose of crmify is **NOT** to be a full featured CRM. It's utility is as a bridge between a Django application
and a 3rd party CRM. Some sample use cases below.
 
*Basic Lead Management*
1. User comes to site and registers for account, this triggers a crmify event to create a lead in Insightly
2. In Insightly, we have a pipeline set up to automatically email new leads
3. When the user clicks a link in the email, it triggers a change in the status of the User in the backend.
4. This status change is automatically synced by django-crmify to Insightly, which updates the Lead from a status of `NotContacted` to `Contacted`.

*Basic Sales Funnel*
1. User comes to site and registers, triggers crmify to create a lead
2. User makes makes a purchase, triggering a Conversion event which syncs to Insightly and updates the Lead from a status of `NotContacted` to `Converted`

## Installation
```
pip install django-crmify
```

## Quick Start
To start using django-crmify, you need to setup some basic configuration parameters. While a number of the parameters will likely need tweaking, the most important settings to get started are: `BACKEND`, `LEAD_MODEL`, and `LEAD_MODEL_FIELDMAPPER`(each of these explained in more detail in the settings [section](#settings) below). Additionally, you will likely need to set the authentication parameters of the CRM backend via environment variables. Here is an example configuration for an integration with the Insightly CRM:`

```python
# Backend auth for insightly is API key based, therefore the backend will be looking for an environment variable CRMIFY_BACKEND_AUTH_API_KEY for auth
CRMIFY = {
  'BACKEND': 'crmify.backends.insightly.InsightlyBackend',
  'LEAD_MODEL': 'myapp.models.UserProfile',
  'LEAD_MODEL_FIELDMAPPER': 'myapp.mappers.UserProfileFieldMapper'
}
```

After setting the `LEAD_MODEL`, it is necessary to run `makemigrations` and then `migrate` to finalize setup.

---

The next step is setting the value of the `LEAD_MODEL_FIELDMAPPER` to a dot-separated path of a `LeadModelFieldMapper` subclass, a simple class responsible for mapping fields from your Lead model onto the internal `crmify.models.Lead` model. For example, the default mapper looks as follows:

```python
class DjangoUserFieldMapper(LeadModelFieldMapper):
    field_mapping = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email',
    }
    fallbacks = {
        'username': 'email'
    }
```

To break this down a bit, the `field_mapping` consists of our model's fields on the left and the internal crmify Lead models' fields on the right. The `fallbacks` field defines the mapping to use in the case that the primary `field_mapping` has no value for a specified Lead field. 

## Settings
| Setting                | Default                                       | Description                               |
| ---------------------- | --------------------------------------------- | ----------------------------------------- |
| BACKEND                | 'crmify.backends.insightly.InsightlyBackend'  | dot separated path to a CRM backend       |
| BACKEND_AUTH           | {}                                            | authentication parameters for the CRM backend. Stored in env vars CRMIFY_BACKEND_AUTH_API_KEY, CRMIFY_BACKEND_AUTH_USERNAME, and CRMIFY_BACKEND_AUTH_PASSWORD |     
| LEAD_MODEL             | 'django.contrib.auth.models.User'             | dot separated path to your applications model you'd like treated as a CRM lead |
| LEAD_MODEL_FIELDMAPPER | 'crmify.mappers.DjangoUserFieldMapper'        | dot separated path to a class defining a mapping between LEAD_MODEL and crmify Lead fields |
| LEAD_STATUS_MODEL      | None                                          | dot separated path to a class subclassing the `crmify.mixins.LeadStatusMixin`. In order to track lead status, this class must implement the `lead_status` method. |
| LEAD_NEW_STATUS        | 'NotContacted'                                | the status to use for new leads           |
| LEAD_CONVERTED_STATUS  | 'Converted'                                   | the status to use for converted leads     |
| LEAD_DEAD_STATUS       | 'Disqualified'                                | the status to use for dead leads          |

## Customization
A CRM backend is simply a class implementing two methods:

```
def sync_lead(self, lead):
   """ sync the given lead to the CRM 
   :param lead: `Lead` object to sync to the CRM
   :return: `str` the ID of the lead in the CRM
   """
   pass

def delete_lead(self, lead_id):
    """ delete the lead with the given ID from the CRM 
    :param lead_id: `str` the ID of the lead in the external CRM
    :return: `bool` True if the lead was deleted, False otherwise
    """
    pass
```

After creating this class, you need only point the `BACKEND` setting to the dot separated path to your CRM backend.
