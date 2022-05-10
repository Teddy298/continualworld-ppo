from mrunner.helpers.specification_helper import create_experiments_helper

from mrunner_utils import combine_config_with_defaults
from continualworld.tasks import TASK_SEQS
from itertools import product



name = globals()["script"][:-3]
config = {
    "run_kind": "cl",
    "logger_output": ["tsv", "neptune"],
    "cl_method": None,
    "replay_size": int(2e6),

    # Resetting options
    "reset_buffer_on_task_change": True,
    "reset_critic_on_task_change": False,
    "reset_optimizer_on_task_change": True,
    "reset_actor_on_task_change": True,
    "upload_weights": False,
    "freeze_actor_on_task_change": None,

}
config = combine_config_with_defaults(config)

tasks = TASK_SEQS["CW10"]
pairs = [[first_task, second_task] for first_task in tasks for second_task in tasks]
num_seeds = 10


settings = [
    {
     "freeze_critic_on_task_change": ["core-l3"],
    },
    {
     "freeze_critic_on_task_change": ["core-l2"],
    },
    {
     "freeze_critic_on_task_change": ["core-f3"],
    },
    {
     "freeze_critic_on_task_change": ["core-f2"],
    },
    {
     "freeze_critic_on_task_change": ["core"],
    },
]

# For a given seed, the first half of each of these experiments will be (almost) identical.
# So in a sense repeating the same first half is a waste of computation. Instead, we can run
# each of these experiments with a different seed so that we get a very large sample for the
# first half which should reduce variance in the results.
# Alternatively, we could run the first half only once (i.e. only `num_seeds` runs) and then
# run multiple "second halves" from there by loading the weights and buffers  but this is a bit
# tricky engineering-wise and might potentially introduce some bugs.

params_grid = []
global_seed_idx = 0
for setting in settings:
    for task in pairs:
        for task_seed in range(num_seeds):
            param_dict = setting.copy()
            param_dict["task_list"] = [task]
            param_dict["seed"] = [global_seed_idx]
            params_grid += [param_dict]
            global_seed_idx += 1
print(params_grid[:10], params_grid[-10:])

experiments_list = create_experiments_helper(
    experiment_name=name,
    project_name="pmtest/continual-learning-2",
    script="python3 mrunner_run.py",
    python_path=".",
    tags=[name, "v7"],
    base_config=config,
    params_grid=params_grid,
)

