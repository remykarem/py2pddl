from pathlib import Path
import fire

def init(filename):
    """
    Args:
        filename (str): name of file ending with `.py`
    """
    path = Path(filename)
    if path.exists():
        raise FileExistsError("This file already exists. Use a different filename.")

    # Name
    class_name = input("Name: ")
    class_name = sanitise(class_name)
    class_name = class_name[0].upper() + class_name[1:]

    # Types
    user_types = input("Types (separated by space): ")
    user_types = sanitise(user_types)
    types = [typ.title() for typ in user_types.split(" ")]

    # Predicates
    user_predicates = input("Predicates (separated by space): ")
    user_predicates = sanitise(user_predicates)
    predicates = [pred.lower() for pred in user_predicates.split(" ")]

    # Actions
    user_actions = input("Actions (separated by space): ")
    user_actions = sanitise(user_actions)
    actions = [action.lower() for action in user_actions.split(" ")]

    domain_header = \
f"""\
from py2pddl import Domain, create_type
from py2pddl import predicate, action, goal, init


class {class_name}Domain(Domain):
"""

    section_types = "".join([\
f"""\
    {typ} = create_type("{typ}")
""" for typ in types])

    section_predicate = "\n".join([\
f"""\
    @predicate(...)
    def {predicate}(self):
        \"\"\"Complete the method signature and specify
        the respective types in the decorator\"\"\"
""" for predicate in predicates])

    section_action = "\n".join([\
f"""\
    @action(...)
    def {action}(self):
        precond: list = None  # to fill in
        effect: list = None  # to fill in
        return precond, effect
""" for action in actions])

    problem_header = \
f"""
class {class_name}Problem({class_name}Domain):
"""

    section_object = \
"""\
    def __init__(self):
        super().__init__()
        \"\"\"To fill in\"\"\"
"""

    section_init = \
"""\
    @init
    def init(self) -> list:
        # To fill in
        # Return type is a list
        return None
"""

    section_goal = \
"""\
    @goal
    def goal(self) -> list:
        # To fill in
        # Return type is a list
        return None
"""

    template = domain_header + "\n" + section_types + "\n" + \
        section_predicate + "\n" + section_action + \
        "\n" + problem_header + "\n" + section_object + \
        "\n" + section_init + "\n" + section_goal

    with open(filename, "w", encoding="utf-8") as f:
        f.write(template)
        print(f"File written to {filename}")


def sanitise(text):
    return text.strip().replace("-", "_")


if __name__ == "__main__":
    fire.Fire(init)
