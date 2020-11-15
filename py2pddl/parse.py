import importlib
from pathlib import Path
import fire

def parse(infile: str,
          domain="domain",
          problem="problem"):
    """Parse a Python module that contains both a Domain and Problem class
    definitions

    Args:
        infile (str): Name of Python file containing both the Domain
            and Problem class definitions.
        domain (str, optional): Base name of domain PDDL file.
            Defaults to "domain".
        problem (str, optional): Base name of problem PDDL file.
            Defaults to "problem".
    """
    # Import module
    p = Path(infile)

    spec = importlib.util.spec_from_file_location(p.stem, str(p.resolve()))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    #importlib.reload(module)  # there might be a better way for this

    problem_name = [attr for attr in dir(module)
                    if attr.endswith("Problem")][0]
    Problem = getattr(module, problem_name)

    p = Problem()
    p.generate_domain_pddl(filename=domain)
    p.generate_problem_pddl(filename=problem)


if __name__ == "__main__":
    fire.Fire(parse)
