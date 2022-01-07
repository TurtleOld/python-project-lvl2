import json
import yaml

TYPE_JSON = '.json'
TYPE_YML_OR_YAML = ('.yml', '.yaml')

VALUE_DELETED = 'deleted'
VALUE_ADDED = 'added'
VALUE_CHANGED = 'changed'
VALUE_UNCHANGED = 'unchanged'
VALUE_CHILD = 'child'


def determining_file_format(file_path):
    if file_path.endswith(TYPE_JSON):
        format_file = json.load(open(file_path))
        return format_file
    if file_path.endswith(TYPE_YML_OR_YAML):
        format_file = yaml.safe_load(open(file_path))
        return format_file


def creating_difference_segment(status, key, value1, value2=None, child=None):
    collected_data = {
        'status': status,
        'key': key,
        'value1': value1,
        'value2': value2,
        'child': child
    }
    return collected_data


def creating_difference(file_path1, file_path2):
    keys1 = file_path1.keys()
    keys2 = file_path2.keys()
    keys = keys1 | keys2
    list_result = []

    for key in sorted(keys):
        if key not in file_path1:
            collected_data = creating_difference_segment(VALUE_ADDED,
                                                         key,
                                                         file_path2[key])
        elif key not in file_path2:
            collected_data = creating_difference_segment(VALUE_DELETED,
                                                         key,
                                                         file_path1[key])
        elif file_path1[key] == file_path2[key]:
            collected_data = creating_difference_segment(VALUE_UNCHANGED,
                                                         key,
                                                         file_path1[key])
        elif isinstance(file_path1[key], dict) and isinstance(file_path2[key],
                                                              dict):
            collected_data = creating_difference_segment(
                VALUE_CHILD,
                key,
                value1=None,
                child=creating_difference(file_path1[key], file_path2[key]
                                          )
            )
        else:
            collected_data = creating_difference_segment(VALUE_CHANGED, key,
                                                         value1=file_path1[key],
                                                         value2=file_path2[key])
        list_result.append(collected_data)

    return list_result


def get_status(collected_data):
    return collected_data.get('status')


def get_key(collected_data):
    return collected_data.get('key')


def get_value(collected_data):
    value = (collected_data.get('value1'), collected_data.get('value2'))
    return value


def get_child(collected_data):
    return collected_data.get('child', None)