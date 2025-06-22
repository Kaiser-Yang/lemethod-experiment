# lemethod-experiment

## Record Introduction

Every directory in `record` is a record for a single experiment.
Its name looks like this below:

```bash
type_worker_[type]_[schedule]_module_[greed]_dynamic_signature
```

This below is for the meaning of this parameters:

* `type`: 
    * `default`
    * `lemethod`
    * `tsengine`
* `worker`: How many workers for this experiment.
* `type`: Only when the type is `lemethod`, there will be this parameter. 
    * `0`: star
    * `1`: complete connection
    * `2`: expanded star.
* `schedule`: Only when the type is `lemethod`, there will be this parameter.
How many worker nodes will participate in one local aggregation scheduling.
* `module`: The size of the machine learning model.
* `greed`: Only when the type is `lemethod` or `tsengine`, there will be this parameter.
Represents the probability sending to best match and
`1 - greed` represents the probability sending randomly.
* `dynamic`: Used to simulate the computation time during training.
    * `1`: the workers will wait a random time after pulling.
    * `0`: the workers will push immediately after pulling.
* `signature`: A little letter, represents the experiments' environment.
When two experiments' `signature` is same.
They run on the same environment,
which means that bandwidths are same, and calculation time is same.

In every experiment directory,
there will be `worker_num + 1` files representing the result.
The files named with `worker*` record the time every worker spending
(from push starts till pull finishes every turn).
The file whose name is `iteration` recording the time every turn,
which is calculated by subtracting the maximum time of the previous turn
from the maximum time of this turn.
And the last line represents the sum of the time,
this is calculated through `max(worker*) - min(workers*)`

For example:

```text
# From worker0 of some experiment
1721645775.9568086 1721645801.0086126
1721645802.0248036 1721645821.857895
1721645822.8248894 1721645849.7068932
1721645850.175422 1721645871.8618038

# From iteration of some experiment
24.50381898880005
24.5838520526886
22.39769458770752
21.542893409729004
```

From the above data, we can know that the worker 0 started the first turn pushing
at `1721645775.9568086` and finished the first turn pulling at `1721645801.0086126`.
And the first turn took `24.50381898880005` seconds.

We can subtract the second number of current line from the first number of the next line
to get the calculation time of current turn.
In this case, we can subtract `1721645801.0086126` from `1721645802.0248036`
to get `1.015191`, which is the calculation time of the first turn.
This number is very small, because this experiment is a static experiment,
which means that the workers will not wait a random time after pulling
to simulate the computation time.
