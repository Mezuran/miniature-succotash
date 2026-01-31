import ast
import string
import random

def get_page_config(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
            
        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue

            for target in node.targets:
                if not isinstance(target, ast.Name) or target.id != "PAGE_CONFIG":
                    continue

                return ast.literal_eval(node.value)
    except Exception:
        pass
    return {}

def generate_random_string(length):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))