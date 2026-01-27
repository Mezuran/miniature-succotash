import ast

def get_page_config(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
            
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "PAGE_CONFIG":
                        return ast.literal_eval(node.value)
    except Exception:
        pass
    return {}