from mrunner.helpers.specification_helper import create_experiments_helper

from continualworld.tasks import TASK_SEQS
from mrunner_utils import combine_config_with_defaults

name = globals()["script"][:-3]
config = {
    "run_kind": "cl",
    "logger_output": ["tsv", "neptune"],
}
config = combine_config_with_defaults(config)

params_grid = {
    "seed": list(range(1)),
    "task": ["CW5"], #task
}

experiments_list = create_experiments_helper(
    experiment_name=name,
    project_name="arczi21/continualworld",
    script="python3 mrunner_run.py",
    python_path=".",
    tags=[name, "v6", "sac"],
    base_config=config,
    params_grid=params_grid,
)
