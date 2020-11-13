import fire


def init(filename="domain.py"):
    class_name = input("Name: ")
    class_name = class_name.title()

    user_types = input("Types (separate by space): ")
    types = [typ.title() for typ in user_types.split(" ")]

    user_predicates = input("Predicated (separate by space): ")
    predicates = [pred.lower() for pred in user_predicates.split(" ")]

    user_actions = input("Actions (separate by space): ")
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
    @predicate
    def {predicate}(self):
        \"\"\"Complete the method signature\"\"\"
""" for predicate in predicates])

    section_action = "\n".join([\
f"""\
    @action
    def {action}(self):
        \"\"\"This should be a pass\"\"\"
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


if __name__ == "__main__":
    fire.Fire(init)
