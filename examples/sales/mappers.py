from crmify.mappers import FieldMapper


class UserProfileFieldMapper(FieldMapper):
    field_mapping = {
        'auth__first_name': 'first_name',
        'auth__last_name': 'last_name',
        'auth__email': 'email',
        'address': 'street_address',
        'city': 'city',
        'state': 'state'
    }