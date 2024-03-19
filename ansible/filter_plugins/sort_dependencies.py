from ansible.errors import AnsibleFilterError

def sort_dependencies(items):
    def topological_sort(source):
        """Performs topological sorting of elements based on their dependencies."""
        pending = [(item, set(item.get('depend_to', []))) for item in source]  # (item, set of dependencies)
        emitted = []
        while pending:
            next_pending = []
            next_emitted = []
            for entry in pending:
                item, dependencies = entry
                dependencies.difference_update(emitted)  # remove dependencies already emitted
                if dependencies:  # if there are still dependencies
                    next_pending.append(entry)
                else:  # no dependencies
                    yield item
                    next_emitted.append(item.get('name'))  # name of the emitted element
            if not next_emitted:
                raise AnsibleFilterError('Circular dependency or non-existing dependencies detected')
            emitted.extend(next_emitted)
            pending = next_pending

    return list(topological_sort(items))

class FilterModule(object):
    ''' Ansible custom filter plugin '''
    def filters(self):
        return {
            'sort_dependencies': sort_dependencies
        }
