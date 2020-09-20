from collections import UserString
from typing import Tuple


class Domain:

    predicates = []

    def generate_domain_pddl(self, filename="domain.pddl"):
        hder = self._generate_header()
        reqs = self._generate_requirements()
        typs = self._generate_types()
        prds = self._generate_predicates()

        pddl = "\n".join([hder, reqs, typs, prds])
        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(pddl))

    def generate_problem_pddl(self):
        pass

    def _generate_header(self):
        return "(define (domain grid_world )"

    def _generate_types(self):
        types = "\n".join([
            attr.lower()
            for attr in dir(self)
            if not attr.startswith("_") and
            not hasattr(getattr(self, attr), "typ") and
            attr not in ["generate_domain_pddl", "generate_requirements"]
        ])
        return "\n".join(["(:types", types, ")"])

    def _generate_requirements(self):
        return "(:requirements :strips :typing)"

    def _generate_predicates(self):
        predicates = "\n".join([
            f"({fn} ?{param} - {typ.__name__.lower()})"
            for fn in self.predicates
            for param, typ in getattr(self, fn).__annotations__.items()
        ])
        return "\n".join(["(:predicates", predicates, ")"])


def action(fn) -> Tuple[bool]:
    """Must return a tuple of precond and effect"""
    setattr(fn, "typ", "action")
    return fn


def predicate(fn) -> bool:
    setattr(fn, "typ", "predicate")
    return fn


def create_type(name, Base=None):
    if Base:
        return type(name, (Base,), {})
    else:
        return type(name, (UserString,), {})
