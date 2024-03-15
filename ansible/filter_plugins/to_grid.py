from ansible.errors import AnsibleFilterError
# from ansible.module_utils._text import to_text
# from ansible.utils.display import Display

# display = Display()

def normalize_to_list1(value, default_values={}, primary_key='name'):
    normalized_list = []
    
    if value is None:
        return []

    # Make normalized grid from 
    # - scalar
    if isinstance(value, (str, int, float)):
        normalized_list.append({primary_key: value})
    
    # - list of ...
    elif isinstance(value, list):
        for item in value:
            # ... scalars
            if isinstance(item, (str, int, float)):
                normalized_list.append({primary_key: item})
            # ... dicts
            elif isinstance(item, dict):
                normalized_list.append(item)
            else:
                raise AnsibleFilterError('List items must be scalar values or dictionaries.')
    
    # - dict of dicts
    elif isinstance(value, dict):
        for key, subdict in value.items():
            if subdict is None:
                subdict = {}
            if not isinstance(subdict, dict):
                raise AnsibleFilterError('All items in the dictionary must be dictionaries, or None.')
            if primary_key in subdict and key != subdict[primary_key]:
                raise AnsibleFilterError(f"Conflict between dictionary key '{key}' and its primary key value '{primary_key}': '{subdict[primary_key]}'.")
            normalized_list.append({**subdict, primary_key: key})

    else:
        raise AnsibleFilterError('Input must be a scalar value, list of scalar values, list of dictionaries, or a dictionary of dictionaries.')
    
    names = set()
    for subdict in normalized_list:
        # Check and append default values
        for default_key, default_value in default_values.items():
                subdict.setdefault(default_key, default_value)
            
        # Check if primary key exists
        if primary_key not in subdict:
            raise AnsibleFilterError('At least on primary key is missing')
        
        # Check duplicity primary key
        if subdict[primary_key] in names:
            raise AnsibleFilterError(f"Duplicate primary key '{primary_key}: {subdict[primary_key]}' is found.")
        
        names.add(subdict[primary_key])
    
    return normalized_list

class FilterModule(object):
    def filters(self):
        return {
            'to_grid': normalize_to_list1
        }
