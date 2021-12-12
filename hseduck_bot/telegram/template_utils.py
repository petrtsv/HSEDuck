import os.path
from typing import Dict, Any, Optional

from hseduck_bot import config


def get_text(template_name: str, template_args: Optional[Dict[str, Any]] = None):
    template_path = os.path.join(*template_name.split(".")) + ".txt"
    with open(os.path.join(config.TG_TEMPLATES_FOLDER, template_path), 'r') as f:
        template_text = f.read()
    if template_args is not None:
        for k in template_args:
            template_text = template_text.replace("$$$%s$$$" % k.upper(), str(template_args[k]))
    return template_text


def make_bold(text: str):
    return get_text("bold", {'text': text})


def wrong_format_message(command: str):
    try:
        right_format = get_text("formats.%s" % (command,))
    except  (OSError, IOError):
        right_format = "undefined"
    return get_text('wrong_format', {'correct': right_format})
