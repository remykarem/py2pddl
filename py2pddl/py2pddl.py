import inspect
from functools import wraps
from collections import UserString, UserDict

# pylint:disable=invalid-name


def create_type(name, Base=None) -> type:
    if Base:
        Type = type(name, (object,), {"section": "types"})
    else:
        Type = type(
            name,
            (UserString,),
            {
                "section": "types",
                "__repr__": lambda self: f"{name}('{self.data}')"
            })
    return Type


class PDDLString(UserString):
    def __invert__(self):
        if "|" in self.data:
            a, b, c = self.data.split(" | ")
            a, b, c = PDDLString(a), PDDLString(b), PDDLString(c)
            return ~a + " | " + ~b + " | " + ~c
        else:
            return f"(not {self.data})"


class PDDLDict(UserDict):
    def __init__(self, typ, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.typ = typ

    def __getitem__(self, key):
        if key not in self.data:
            raise KeyError(f"Key {key} does not exist for {self.typ}. Did you define the objects correctly?")
        else:
            return self.data[key]


class Domain:

    def init(self):
        pass

    def goal(self):
        pass

    def generate_domain_pddl(self, *, filename="domain"):
        filename = filename + ".pddl"
        hder = Domain._generate_header()
        reqs = Domain._generate_requirements()
        typs = self._generate_types()
        prds = self._generate_predicates()
        acts = self._generate_actions()

        pddl = "\n".join([hder, reqs, typs, prds, acts, ")"])
        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(pddl))
            print(f"Domain PDDL written to {filename}.")

    def generate_problem_pddl(self, *,
                              init: dict = None,
                              goal: dict = None,
                              filename: str = "problem"):
        if init is None:
            init = {}
        if goal is None:
            goal = {}
        filename = filename + ".pddl"

        hder = Domain._generate_header_prob()
        domain = "\t" + "(:domain somedomain)"
        objs = self._generate_objects()
        inits = "\t" + self.init(**init)
        goals = "\t" + self.goal(**goal)

        pddl = join([hder, domain, objs, inits, goals, ")\n"],
                    "\n", and_marker=False)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(pddl))
            print(f"Problem PDDL written to {filename}.")

    @staticmethod
    def _generate_header(name="somedomain"):
        return f"(define\n\t(domain {name})"

    @staticmethod
    def _generate_header_prob(name="someproblem"):
        return f"(define\n\t(problem {name})"

    @staticmethod
    def _generate_requirements():
        return "\t(:requirements :strips :typing)"

    def _generate_types(self):
        types = "\n".join([
            f"\t\t{attr.lower()}"
            for attr in dir(self)
            if hasattr(getattr(self, attr), "section") and
            getattr(self, attr).section == "types" and
            not hasattr(getattr(self, attr), "data")
        ])
        return "\n".join(["\t(:types", types, "\t)"])

    def _generate_predicates(self):
        predicates = "\n".join([
            "\t\t" + fn().split(" | ")[0]
            for fn in self._get("predicate")
        ])
        return "\n".join(["\t(:predicates", predicates, "\t)"])

    def _generate_actions(self):
        actions = "\n".join([
            "\t" + fn()
            for fn in self._get("action")
        ])
        return "\n".join([actions])

    def _generate_objects(self):
        objs = []
        for attr in dir(self):
            if (not attr.startswith("_") and
                    not hasattr(getattr(self, attr), "section") and
                    isinstance(getattr(self, attr), (list, PDDLDict))):

                # Get object
                attr = getattr(self, attr)

                # Parse according to the type
                if isinstance(attr, list):
                    objs_ = " ".join([str(obj) for obj in attr])
                    objs.append(
                        f"\t\t{objs_} - {attr[0].__class__.__name__.lower()}")
                elif isinstance(attr, PDDLDict):
                    # Key is the alias, value is the object
                    objs_ = " ".join([str(obj) for _, obj in attr.items()])
                    objs.append(f"\t\t{objs_} - {attr.typ}")
                else:
                    raise TypeError

        objs = "\n".join(objs)
        return "\n".join(["\t(:objects", objs, "\t)"])

    def _get(self, item):
        user_defined = [attr for attr in dir(self)
                        if hasattr(getattr(self, attr), "section")]
        return [getattr(self, user_dfn) for user_dfn in user_defined
                if getattr(self, user_dfn).section == item]


def action(*Types):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            # Subheader
            action_name = f"(:action {func.__name__}"

            # We don't need the self for the rest of this code
            _, *params = list(inspect.signature(func).parameters.items())
            _, *varnames = func.__code__.co_varnames
            varnames = varnames[:func.__code__.co_argcount-1]

            # Call the function to get the return values to be used
            # in the later part of this function
            dummy_args = [Type(varname)
                          for Type, varname in zip(Types, varnames)]
            all_args = list(args) + dummy_args

            precond, effect = func(*all_args)

            # The first type is self; we'll ignore that
            _, *args = args

            # Check types
            # Ignore if it's NoneType (to define the domain)
            for Class, arg in zip(Types, args):
                if not isinstance(arg, (Class, type(None))):
                    raise TypeError(f"Expected {Class.__name__} for action '{action_name}' "
                                    f"but got {type(arg).__name__}")

            # Parameters
            repre = [f"?{a} - {b.__name__.lower()}"
                     for a, b in zip(varnames, Types)]
            repre = " ".join(repre)
            repre = f"\t\t:parameters ({repre})"

            # Precond
            if not isinstance(precond, list):
                precond = [precond]
            precond = [str(p.split(" | ")[1]) for p in precond]
            precond = "\t\t:precondition " + join(precond, " ")

            # Effect
            if not isinstance(effect, list):
                effect = [effect]
            effect = [str(e.split(" | ")[1]) for e in effect]
            effect = "\t\t:effect " + join(effect, " ")

            # Final
            actn = [action_name, repre, precond, effect, "\t)"]
            actn = join(actn, "\n", False)

            return actn

        setattr(wrapper, "section", "action")
        return wrapper

    return decorator


def predicate(*Types) -> str:

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            # Invoke function to invoke Python's argument checking
            # We don't actually need it
            # func(*args, **kwargs)

            func_name = func.__name__

            # The first type is self; we'll ignore that
            _, *params = list(inspect.signature(func).parameters.items())
            _, *args = args

            # Check types
            # Ignore if it's NoneType (to define the domain)
            for Class, arg in zip(Types, args):
                if not isinstance(arg, (Class, type(None))):
                    raise TypeError(f"Expected type {Class.__name__} for predicate '{func_name}' "
                                    f"but found {type(arg).__name__}")

            # Representation 1 (in :predicates)
            _, *params = list(inspect.signature(func).parameters.items())
            repr1 = []
            for param, Class in zip(params, Types):
                param_name, _ = param
                repr1.append(f"?{param_name} - {Class.__name__.lower()}")
            repr1 = " ".join(repr1)
            repr1 = f"({func_name} {repr1})"

            # Representation 2 (in :action :precondition/:effect)
            repr2 = [f"?{str(arg)}" for arg in args]
            repr2 = " ".join(repr2)
            repr2 = f"({func_name} {repr2})"

            # Representation 3 (in :init and :goal)
            args = [str(arg) for arg in args]
            params3 = "(" + " ".join([func_name, *args]) + ")"

            return PDDLString(repr1) + " | " + PDDLString(repr2) + " | " + PDDLString(params3)

        setattr(wrapper, "section", "predicate")
        return wrapper

    return decorator


def goal(func) -> str:
    @wraps(func)
    def wrapper(*args, **kwargs):
        goals = func(*args, **kwargs)
        if not isinstance(goals, list):
            raise TypeError("Return type of `goal` method must be a list")

        goals = [str(g.split(" | ")[2]) for g in goals]
        goals = f"(:goal {join(goals)})"
        return PDDLString(goals)
    setattr(wrapper, "section", "goal")
    return wrapper


def init(func) -> str:
    @wraps(func)
    def wrapper(*args, **kwargs):
        inits = func(*args, **kwargs)
        if not isinstance(inits, list):
            raise TypeError("Return type of `init` method must be a list")

        inits = [str(g.split(" | ")[2]) for g in inits]
        inits = f"(:init {join(inits, and_marker=False)})"
        return PDDLString(inits)
    setattr(wrapper, "section", "init")
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


def create_objs(Class,
                it,
                prefix_key=None,
                prefix_value=None) -> dict:
    class_name = Class.__name__.lower()

    if prefix_value is None:
        prefix_value = class_name

    if prefix_key is None:
        obj_dict = PDDLDict(
            class_name,
            {i: Class(f"{prefix_value}{str(i)}") for i in it})
    else:
        obj_dict = PDDLDict(
            class_name,
            {f"{prefix_key}{str(obj)}": Class(prefix_value+str(obj)) for obj in it})

    return obj_dict