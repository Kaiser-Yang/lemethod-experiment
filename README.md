# lemethod-experiment

## Experiments Design

Before experiment, we will run `LeMethod` and `TSEngine` for
`100` iterations with `32` workers, `240MB` model size
and fixed `SCHEDULE_NUM=1` but with different `GREED_RATE`
for both dynamic and static experiments to get the best `GREED_RATE` for each method.

And we will run `LeMethod` for `100` iterations with `32` workers, `240MB` model size
and fixed `GREED_RATE=1` but with different `SCHEDULE_NUM`
for both dynamic and static experiments to get the best `SCHEDULE_NUM` for `LeMethod`.

After this, we will run `LeMethod` and `TSEngine` with the best `GREED_RATE` and `SCHEDULE_NUM`
in the following experiments.

1. For the star topology, the traditional parameter server architecture, `TSEngine`, and `LeMethod`
   will be compared.
2. For the complete connection topology, `LeMethod` and `TSEngine` will be compared.
3. For the expanded star topology, only `LeMethod` will be tested.

For `1` and `2`, we run the experiments with different numbers of workers
, different model sizes, dynamic and static experiments,
for `100` iterations.

For `3`, we run the experiments with different numbers of workers,
different model sizes, dynamic and static experiments,
and different expansion factors,
for `100` iterations.

## Records Introduction

Every directory in `record` is a record for a single experiment.
Its name looks like this below:

```bash
type_worker_[type]_[schedule]_module_[greed]_dynamic_signature
```

This below is for the meaning of this parameters:

- `type`:
  - `default`
  - `lemethod`
  - `tsengine`
- `worker`: How many workers for this experiment.
- `type`: Only when the type is `lemethod`, there will be this parameter.
  - `0`: star
  - `1`: complete connection
  - `2`: expanded star.
- `schedule`: Only when the type is `lemethod`, there will be this parameter.
  How many worker nodes will participate in one local aggregation scheduling.
- `model`: The size of the machine learning model.
- `greed`: Only when the type is `lemethod` or `tsengine`, there will be this parameter.
  Represents the probability sending to best match and
  `1 - greed` represents the probability sending randomly.
- `dynamic`: Used to simulate the computation time during training.
  - `1`: the workers will wait a random time after pulling.
  - `0`: the workers will push immediately after pulling.
- `signature`: A little letter, represents the experiments' environment.
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

## Scripts Introduction

- `experiment.py`: This is the main experiment process, which will run the experiment. Usage:

```bash
python3 experiment.py WORKER_NUM MODULE_SIZE ITERATION SLEEP_AFTER_PULL
```

- `start_server.sh`: This script is used to start the server for the experiment.
  It will set up some environment variables and then run `experiment.py` as a server. Usage:

```bash
bash start_server.sh NUM_WORKER \
    ENABLE_LEMETHOD ENABLE_TSENGINE \
    LEMETHOD_CONNECTION_TYPE \
    GREED_RATE \
    PS_VERBOSE
```

- `start_worker.sh`: This script is used to start a worker for the experiment.
  It will set up some environment variables and then run `experiment.py` as a worker. Usage:

```bash
bash start_worker.sh NUM_WORKER \
    ENABLE_LEMETHOD ENABLE_TSENGINE \
    LEMETHOD_CONNECTION_TYPE \
    GREED_RATE \
    PS_VERBOSE \
    DMLC_RNAK \
    MODULE_SIZE \
    ITERATION \
    DMLC_NODE_HOST \
    SLEEP_AFTER_PULL
```

- `start_scheduler.sh`: This script is used to start a scheduler for the experiment.
  It will set up some environment variables and then run `experiment.py` as a scheduler. Usage:

```bash
bash start_scheduler.sh NUM_WORKER \
    ENABLE_LEMETHOD ENABLE_TSENGINE
    LEMETHOD_CONNECTION_TYPE \
    GREED_RATE \
    PS_VERBOSE
```

## Pre-experiment

The result of 32 workers of lemethod with different greed rates in static experiments:

```text
('lemethod_32_1_1_240M_0.6_0_d', 2704.3345057964325)
('lemethod_32_1_1_240M_0.5_0_d', 2713.877676963806)
('lemethod_32_1_1_240M_1_0_d', 2720.29834485054)
('lemethod_32_1_1_240M_0.1_0_d', 2723.672041654587)
('lemethod_32_1_1_240M_0.4_0_d', 2727.801529407501)
('lemethod_32_1_1_240M_0.2_0_d', 2748.950067281723)
('lemethod_32_1_1_240M_0.3_0_d', 2756.6114370822906)
('lemethod_32_1_1_240M_0.7_0_d', 2774.665088415146)
('lemethod_32_1_1_240M_0.8_0_d', 2777.117935180664)
('lemethod_32_1_1_240M_0.9_0_d', 2803.403065443039)
```

`0.6` is chosen for static experiments.

The result of 32 workers of lemethod with different greed rates in dynamic experiments:

```text
('lemethod_32_1_1_240M_0.9_1_d', 2985.306182861328)
('lemethod_32_1_1_240M_0.1_1_d', 2986.8037102222443)
('lemethod_32_1_1_240M_0.7_1_d', 2988.8796751499176)
('lemethod_32_1_1_240M_1_1_d', 2995.769952058792)
('lemethod_32_1_1_240M_0.4_1_d', 2996.0755155086517)
('lemethod_32_1_1_240M_0.8_1_d', 2997.0085446834564)
('lemethod_32_1_1_240M_0.6_1_d', 3001.2854228019714)
('lemethod_32_1_1_240M_0.5_1_d', 3005.570837020874)
('lemethod_32_1_1_240M_0.2_1_d', 3033.6022577285767)
('lemethod_32_1_1_240M_0.3_1_d', 3045.4263558387756)
```

`0.9` is chosen for dynamic experiments.

The result of 32 workers of lemethod with different schedule numbers in static experiments:

```text
('lemethod_32_1_5_240M_1_0_d', 2579.7233152389526)
('lemethod_32_1_4_240M_1_0_d', 2621.7886576652527)
('lemethod_32_1_3_240M_1_0_d', 2622.1098268032074)
('lemethod_32_1_7_240M_1_0_d', 2683.771742582321)
('lemethod_32_1_6_240M_1_0_d', 2703.45508146286)
('lemethod_32_1_2_240M_1_0_d', 2713.993212223053)
('lemethod_32_1_1_240M_1_0_d', 2720.29834485054)
('lemethod_32_1_8_240M_1_0_d', 2863.6399369239807)
('lemethod_32_1_9_240M_1_0_d', 2881.8238224983215)
('lemethod_32_1_13_240M_1_0_d', 2952.755471944809)
('lemethod_32_1_10_240M_1_0_d', 2979.7679069042206)
('lemethod_32_1_11_240M_1_0_d', 3093.324608564377)
('lemethod_32_1_14_240M_1_0_d', 3176.8998823165894)
('lemethod_32_1_12_240M_1_0_d', 3202.662478208542)
('lemethod_32_1_15_240M_1_0_d', 3420.5809841156006)
('lemethod_32_1_18_240M_1_0_d', 3728.641146183014)
('lemethod_32_1_17_240M_1_0_d', 3797.2028620243073)
('lemethod_32_1_21_240M_1_0_d', 3926.8109736442566)
('lemethod_32_1_19_240M_1_0_d', 3933.729520559311)
('lemethod_32_1_16_240M_1_0_d', 3965.8288114070892)
('lemethod_32_1_22_240M_1_0_d', 4132.412855386734)
('lemethod_32_1_20_240M_1_0_d', 4158.596895456314)
('lemethod_32_1_23_240M_1_0_d', 4281.37526512146)
('lemethod_32_1_24_240M_1_0_d', 4362.851956367493)
('lemethod_32_1_25_240M_1_0_d', 4638.54817199707)
('lemethod_32_1_26_240M_1_0_d', 4707.450743675232)
('lemethod_32_1_27_240M_1_0_d', 4924.71950340271)
('lemethod_32_1_28_240M_1_0_d', 5148.704471826553)
('lemethod_32_1_29_240M_1_0_d', 5317.488800287247)
('lemethod_32_1_30_240M_1_0_d', 5422.872277259827)
('lemethod_32_1_31_240M_1_0_d', 5713.463895559311)
('lemethod_32_1_32_240M_1_0_d', 6004.415000915527)
```

`min(3, 5 / 32)` is chosen for static experiments.

The result of 32 workers of lemethod with different schedule numbers in dynamic experiments:

```text
('lemethod_32_1_3_240M_1_1_d', 2873.249228954315)
('lemethod_32_1_2_240M_1_1_d', 2944.5967903137207)
('lemethod_32_1_5_240M_1_1_d', 2960.741891860962)
('lemethod_32_1_4_240M_1_1_d', 2962.4370877742767)
('lemethod_32_1_6_240M_1_1_d', 2979.526656150818)
('lemethod_32_1_1_240M_1_1_d', 2995.769952058792)
('lemethod_32_1_7_240M_1_1_d', 3198.519252061844)
('lemethod_32_1_8_240M_1_1_d', 3344.986218690872)
('lemethod_32_1_9_240M_1_1_d', 3389.875543117523)
('lemethod_32_1_10_240M_1_1_d', 3524.904333591461)
('lemethod_32_1_11_240M_1_1_d', 3691.7322657108307)
('lemethod_32_1_12_240M_1_1_d', 3706.240339756012)
('lemethod_32_1_13_240M_1_1_d', 3842.9517426490784)
('lemethod_32_1_14_240M_1_1_d', 3978.1325256824493)
('lemethod_32_1_15_240M_1_1_d', 4141.700600862503)
('lemethod_32_1_18_240M_1_1_d', 4373.580430269241)
('lemethod_32_1_19_240M_1_1_d', 4439.73627281189)
('lemethod_32_1_17_240M_1_1_d', 4449.431510686874)
('lemethod_32_1_20_240M_1_1_d', 4574.82826924324)
('lemethod_32_1_22_240M_1_1_d', 4603.289314508438)
('lemethod_32_1_21_240M_1_1_d', 4628.788670301437)
('lemethod_32_1_16_240M_1_1_d', 4661.256333589554)
('lemethod_32_1_23_240M_1_1_d', 4897.624588727951)
('lemethod_32_1_24_240M_1_1_d', 5041.25402712822)
('lemethod_32_1_25_240M_1_1_d', 5259.357847213745)
('lemethod_32_1_26_240M_1_1_d', 5357.3261282444)
('lemethod_32_1_27_240M_1_1_d', 5631.159260511398)
('lemethod_32_1_28_240M_1_1_d', 5750.4645302295685)
('lemethod_32_1_29_240M_1_1_d', 6117.4502120018005)
('lemethod_32_1_30_240M_1_1_d', 6274.9417378902435)
('lemethod_32_1_31_240M_1_1_d', 6727.802109241486)
('lemethod_32_1_32_240M_1_1_d', 6956.787885189056)
```

`min(3, 3 / 32)` is chosen for dynamic experiments.
