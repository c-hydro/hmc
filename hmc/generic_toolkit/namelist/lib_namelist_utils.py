from collections import OrderedDict
from typing import Tuple, List
import re


# method to filter comments from a file stream
def filter_settings(file_stream: str, file_comment: str = '!') -> Tuple[List[str], List[str]]:
    """
    Filter comments from a file stream.
    :param file_stream:
    :param file_comment:
    :return: settings_lines, comments_line
    """
    settings_lines, comments_lines = [], []
    for line in file_stream.split('\n'):
        if line.strip().startswith(file_comment):
            comments_lines.append(line)
        else:
            settings_lines.append(line)

    return settings_lines, comments_lines


# method to group settings
def group_settings(settings_blocks: List[str]) -> dict:
    """
    Group settings.
    :param settings_lines:
    :param group_re:
    :return: group_blocks
    """

    settings_groups = {}
    for settings_block in settings_blocks:
        settings_lines_raw = settings_block.split('\n')

        settings_block_name = settings_lines_raw.pop(0).strip()
        settings_groups[settings_block_name] = {}

        settings_lines_filtered = []
        for line in settings_lines_raw:
            # cleanup string
            line = line.strip()
            if line == "":
                continue
            if line.startswith('!'):
                continue

            try:
                k, v = line.split('=')
                settings_lines_filtered.append(line)
            except ValueError:
                # no = in current line, try to append to previous line
                if settings_lines_filtered[-1].endswith(','):
                    settings_lines_filtered[-1] += line
                else:
                    raise

        for line in settings_lines_filtered:
            # commas at the end of lines seem to be optional
            if line.endswith(','):
                line = line[:-1]

            # inline comments are allowed, but we remove them for now
            if "!" in line:
                line = line.split("!")[0].strip()

            k, v = line.split('=')
            variable_name = k.strip()
            variable_value = v.strip()

            settings_groups[settings_block_name][variable_name] = variable_value

    return settings_groups


# method to parse settings
def parse_settings(settings_groups: dict) -> dict:
    """
    Parse settings.
    :param settings_groups:
    :return: parsed_settings
    """
    parsed_settings = {}
    for group_name, group_dict in settings_groups.items():
        parsed_settings[group_name] = {}
        for k, v in group_dict.items():

            v = v.split(',')

            if len(v) == 1:
                v = v[0].strip()
                if v.startswith("'") and v.endswith("'"):
                    parsed_settings[group_name][k] = v[1:-1]
                elif v.startswith('"') and v.endswith('"'):
                    parsed_settings[group_name][k] = v[1:-1]
                elif v.startswith("'"):
                    parsed_settings[group_name][k] = v[1:]
                elif v.endswith("'"):
                    parsed_settings[group_name][k] = v[:-1]
                elif v.lower() == '.true.':
                    parsed_settings[group_name][k] = True
                elif v.lower() == '.false.':
                    parsed_settings[group_name][k] = False
                else:
                    try:
                        parsed_settings[group_name][k] = int(v)
                    except ValueError:
                        try:
                            parsed_settings[group_name][k] = float(v)
                        except ValueError:
                            parsed_settings[group_name][k] = v

            else:
                try:
                    v_list = [int(i) for i in v]
                    parsed_settings[group_name][k] = v_list
                except ValueError:
                    try:
                        v_list = [float(i) for i in v]
                        parsed_settings[group_name][k] = v_list
                    except ValueError:
                        v_list = []
                        for n, i in enumerate(v):
                            if i.startswith("'") and i.endswith("'"):
                                v_list.append(i[1:-1])
                            elif i.startswith('"') and i.endswith('"'):
                                v_list.append(i[1:-1])
                            elif i.startswith("'"):
                                v_list.append(i[1:])
                            elif i.endswith("'"):
                                v_list.append(i[:-1])
                            elif i.lower() == '.true.':
                                v_list.append(True)
                            elif i.lower() == '.false.':
                                v_list.append(False)
                            else:
                                v_list.append(i)
                        parsed_settings[group_name][k] = v_list

    return parsed_settings
