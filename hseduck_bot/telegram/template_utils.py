import os.path
from typing import Dict, Any, Optional

from hseduck_bot import config


def get_text(template_name: str, template_args: Optional[Dict[str, Any]] = None):
    with open(os.path.join(config.TG_TEMPLATES_FOLDER, template_name + ".txt"), 'r') as f:
        template_text = f.read()
    if template_args is not None:
        for k in template_args:
            template_text = template_text.replace("$$$%s$$$" % k.upper(), str(template_args[k]))
    return template_text
