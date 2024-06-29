# lemethod-experiment
## Record Introduction
Every directory in `record` is a record for a single experiment. Its name looks like this below:

`<type>_<worker_num>_[connection_type]_[schedule_num]_<module_size>_[greed_rate]_<dynamic>_<signature>`

This below is for the meaning of this parameters:
* `type`: can be `default`, `lemethod` and `tsengine`.
* `worker_num`: represents how many workers this experiment.
* `connection_type`: only when the type is `lemethod`, there will be this parameter, represents the connection type: `0` for star, `1` for full connection, `2` for expanded star.
* `schedule_num`: only when the type is `lemethod`, there will be this parameter, represents the least number of nodes which will participate in one scheduling.
* `module_size`: the size of the machine learning model size.
* `greed_rate`: only when the type is `lemethod` or `tsengine`, there will be this parameter, `1 - greed_rate` represents the probability sending randomly.
* `dynamic`: represnets that if the workers will wait after pulling parameters. When is `1`, the workers will wait a random time to simulate the computation time during training.
* `signature`: a little letter, represents the experiments' environment. When two experiments' `signature` is same. They run on the same environment, which means that bandwidths change same, calculation time changes same.

In every experiment directory, there will be `worker_num + 1` files representing the result. The files named with `worker*` record the time every worker spending (from push starts till pull finishes every turn). The file whose name is `iteration` recording the time every turn, it is calculated by subtracting the maximum time of the previous turn from the maximum time of this turn. And the last line represents the sum of the time, this is calculated through `max(worker*) - min(workers*)`
