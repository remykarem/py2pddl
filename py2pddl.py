from pathlib import Path
import importlib
from collections import UserString
from abc import ABCMeta
from typing import Tuple
import inspect


class PDDLString(UserString):
    def __invert__(self):
        if "|" in self.data:
            a, b, c = self.data.split(" | ")
            a, b, c = PDDLString(a), PDDLString(b), PDDLString(c)
            return ~a + " | " + ~b + " | " + ~c
        else:
            return f"(not {self.data})"


class Domain:

    def init(self):
        pass

    def goal(self):
        pass

    def generate_domain_pddl(self, filename="domain.pddl"):
        hder = Domain._generate_header()
        reqs = Domain._generate_requirements()
        typs = self._generate_types()
        prds = self._generate_predicates()
        acts = self._generate_actions()

        pddl = "\n".join([hder, reqs, typs, prds, acts, ")"])
        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(pddl))

    def generate_problem_pddl(self, filename="problem.pddl"):
        hder = Domain._generate_header_prob()
        domain = "\t" + "(:domain somedomain)"
        objs = self._generate_objects()
        inits = "\t" + self.init()
        goals = "\t" + self.goal()

        pddl = join([hder, domain, objs, inits, goals, ")\n"],
                    "\n", and_marker=False)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(pddl))

    @staticmethod
    def _generate_header(name="grid_world"):
        return f"(define\n\t(domain {name})"

    @staticmethod
    def _generate_header_prob(name="grid_world"):
        return f"(define\n\t(problem {name})"

    @staticmethod
    def _generate_requirements():
        return "\t(:requirements :strips :typing)"

    def _generate_objects(self):
        objs = []
        for attr in dir(self):
            if (hasattr(getattr(self, attr), "typ") and
                getattr(self, attr).typ == "type" and
                    hasattr(getattr(self, attr), "data") or isinstance(getattr(self, attr), list)):
                attr = getattr(self, attr)
                if isinstance(attr, list):
                    objs_ = " ".join([str(obj) for obj in attr])
                    objs.append(
                        f"\t\t{objs_} - {attr[0].__class__.__name__.lower()}")
                else:
                    objs.append(
                        f"\t\t{attr} - {attr.__class__.__name__.lower()}")

        objs = "\n".join(objs)
        # objs = "\n".join([
        #     f"\t\t{attr.lower()}"
        #     for attr in dir(self)
        #     if (hasattr(getattr(self, attr), "typ") and
        #     getattr(self, attr).typ == "type" and
        #     hasattr(getattr(self, attr), "data") or isinstance(getattr(self, attr), list))
        # ])
        return "\n".join(["\t(:objects", objs, "\t)"])

    def _generate_types(self):
        types = "\n".join([
            f"\t\t{attr.lower()}"
            for attr in dir(self)
            if hasattr(getattr(self, attr), "typ") and
            getattr(self, attr).typ == "type" and
            not hasattr(getattr(self, attr), "data")
        ])
        return "\n".join(["\t(:types", types, "\t)"])

    def _generate_predicates(self):
        predicates = "\n".join([
            "\t\t" + fn().split(" | ")[0]
            for fn in self._get("predicate")
        ])
        return "\n".join(["\t(:predicates", predicates, "\t)"])

    def _get(self, item):
        user_defined = [attr for attr in dir(self)
                        if hasattr(getattr(self, attr), "typ")]
        return [getattr(self, user_dfn) for user_dfn in user_defined
                if getattr(self, user_dfn).typ == item]

    def _generate_actions(self):
        actions = "\n".join([
            "\t" + fn()
            for fn in self._get("action")
        ])
        return "\n".join([actions])


def action(func) -> str:
    """Must return a tuple of precond and effect"""

    def wrapper(*args, **kwargs):
        # Invoke function to invoke Python's argument checking
        precond, effect = func(*args, **kwargs)

        action_name = f"(:action {func.__name__}"

        _, *varnames = func.__code__.co_varnames
        varnames = varnames[:func.__code__.co_argcount-1]

        params = [f"?{a} - {b[1].__name__.lower()}"
                  for a, b in zip(varnames, func.__annotations__.items())]
        params = " ".join(params)
        params = f"\t\t:parameters ({params})"

        if not isinstance(precond, list):
            precond = [precond]
        precond = [str(p.split(" | ")[1]) for p in precond]
        precond = "\t\t:precondition " + join(precond, " ")

        if not isinstance(effect, list):
            effect = [effect]
        effect = [str(e.split(" | ")[1]) for e in effect]
        effect = "\t\t:effect " + join(effect, " ")

        action = [action_name, params, precond, effect, "\t)"]
        action = join(action, "\n", False)

        return action

    setattr(wrapper, "typ", "action")

    return wrapper


def predicate(func) -> str:

    def wrapper(*args, **kwargs):
        """PDDL"""
        # Invoke function to invoke Python's argument checking
        func(*args, **kwargs)

        _, *varnames = func.__code__.co_varnames

        params = [f"?{varname} - {annotation[1].__name__.lower()}"
                  for varname, annotation in zip(varnames, func.__annotations__.items())]
        params = " ".join(params)
        params = f"({func.__name__} {params})"

        _, *args = args

        params1 = [f"?{arg}" for arg in args]
        params1 = " ".join(params1)
        params1 = f"({func.__name__} {params1})"

        args = [str(arg) for arg in args]

        return PDDLString(params) + " | " + PDDLString(params1) + " | " + PDDLString("(" + " ".join([func.__name__, *args]) + ")")

    setattr(wrapper, "typ", "predicate")

    return wrapper


def goal(func) -> str:

    def wrapper(*args, **kwargs):
        goal = func(*args, **kwargs)
        goal = [str(g.split(" | ")[2]) for g in goal]
        goal = f"(:goal {join(goal)})"

        return PDDLString(goal)

    setattr(wrapper, "typ", "goal")
    return wrapper


def init(func) -> str:

    def wrapper(*args, **kwargs):
        init = func(*args, **kwargs)
        init = [str(g.split(" | ")[2]) for g in init]
        init = f"(:init {join(init, and_marker=False)})"

        return PDDLString(init)

    setattr(wrapper, "typ", "init")
    return wrapper


def join(li, sep=" ", and_marker=True) -> str:
    li = [str(l) for l in li]

    if len(li) == 1:
        return li[0]
    else:
        if and_marker:
            return "(and " + sep.join(li) + ")"
        else:
            return sep.join(li)


def create_type(name, Base=None):
    if Base:
        return type(name, (Base,), {"typ": "type"})
    else:
        return type(name, (UserString,), {"typ": "type"})


def parse(filename):
    p = Path(filename)
    module = importlib.import_module(p.stem)

    domain_name = [attr for attr in dir(module)
                    if attr.endswith("Domain") and attr != "Domain"][0]
    problem_name = [attr for attr in dir(module)
                    if attr.endswith("Problem")][0]
    Problem = getattr(module, domain_name)
    Domain = getattr(module, problem_name)
    domain = Domain()
    problem = Problem()
    problem.generate_domain_pddl()
    problem.generate_problem_pddl()
