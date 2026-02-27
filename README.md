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

LeMethod nodes dynamic:

```text
('lemethod_20_1_3_240M_0.9_1_a', 2538.3279745578766)
('lemethod_40_1_4_240M_0.9_1_a', 3150.367321252823)
('lemethod_10_1_3_240M_0.9_1_a', 2218.841932296753)
('lemethod_85_1_8_240M_0.9_1_a', 3971.104033946991)
('lemethod_50_1_5_240M_0.9_1_a', 3495.0027499198914)
('lemethod_80_1_8_240M_0.9_1_a', 4052.4658329486847)
('lemethod_55_1_5_240M_0.9_1_a', 3305.547732114792)
('lemethod_65_1_6_240M_0.9_1_a', 3684.041827917099)
('lemethod_70_1_7_240M_0.9_1_a', 3860.801153898239)
('lemethod_35_1_3_240M_0.9_1_a', 3054.2890412807465)
('lemethod_90_1_8_240M_0.9_1_a', 3982.0633957386017)
('lemethod_60_1_6_240M_0.9_1_a', 3700.7065510749817)
('lemethod_95_1_9_240M_0.9_1_a', 4340.301110029221)
('lemethod_25_1_3_240M_0.9_1_a', 2860.391548871994)
('lemethod_15_1_3_240M_0.9_1_a', 2591.6239914894104)
('lemethod_30_1_3_240M_0.9_1_a', 2982.287831544876)
('lemethod_45_1_4_240M_0.9_1_a', 3238.9606590270996)
('lemethod_75_1_7_240M_0.9_1_a', 3919.6574087142944)
('lemethod_100_1_9_240M_0.9_1_a', 4211.067704677582)
```

LeMethod nodes static:

```text
('lemethod_90_1_14_240M_0.6_0_a', 4128.325797080994)
('lemethod_55_1_9_240M_0.6_0_a', 3285.653203725815)
('lemethod_15_1_3_240M_0.6_0_a', 2088.55544424057)
('lemethod_85_1_13_240M_0.6_0_a', 4062.9409594535828)
('lemethod_60_1_9_240M_0.6_0_a', 3609.8160054683685)
('lemethod_30_1_5_240M_0.6_0_a', 2695.985447406769)
('lemethod_40_1_6_240M_0.6_0_a', 2804.371499300003)
('lemethod_95_1_15_240M_0.6_0_a', 4628.8682997226715)
('lemethod_35_1_5_240M_0.6_0_a', 2768.2093937397003)
('lemethod_20_1_3_240M_0.6_0_a', 2333.390537261963)
('lemethod_50_1_8_240M_0.6_0_a', 3290.0889167785645)
('lemethod_80_1_13_240M_0.6_0_a', 3806.9258394241333)
('lemethod_65_1_10_240M_0.6_0_a', 3783.4233162403107)
('lemethod_75_1_12_240M_0.6_0_a', 3993.4696724414825)
('lemethod_25_1_4_240M_0.6_0_a', 2529.8970682621)
('lemethod_45_1_7_240M_0.6_0_a', 2944.6313445568085)
('lemethod_10_1_3_240M_0.6_0_a', 1738.2607219219208)
('lemethod_70_1_11_240M_0.6_0_a', 3726.388567209244)
('lemethod_100_1_16_240M_0.6_0_a', 4710.304752111435)
```

Default nodes dynamic:

```text
('default_45_240M_1_a', 14601.79453921318)
('default_25_240M_1_a', 8674.264544010162)
('default_60_240M_1_a', 18141.561836719513)
('default_20_240M_1_a', 7343.564475536346)
('default_75_240M_1_a', 20603.955714941025)
('default_70_240M_1_a', 18667.15565943718)
('default_100_240M_1_a', 27631.928013324738)
('default_40_240M_1_a', 12179.976054668427)
('default_95_240M_1_a', 28148.63996362686)
('default_30_240M_1_a', 9259.616561412811)
('default_80_240M_1_a', 21786.026332378387)
('default_35_240M_1_a', 10127.619410037994)
('default_65_240M_1_a', 18079.583578824997)
('default_50_240M_1_a', 14085.683629512787)
('default_85_240M_1_a', 21850.648270606995)
('default_15_240M_1_a', 5400.9088768959045)
('default_55_240M_1_a', 15024.658378601074)
('default_90_240M_1_a', 25056.278143644333)
('default_10_240M_1_a', 3441.053349494934)
```

Default nodes static:

```text
('default_25_240M_0_a', 8152.445867538452)
('default_15_240M_0_a', 5277.766409397125)
('default_75_240M_0_a', 20940.19470500946)
('default_30_240M_0_a', 8991.876920223236)
('default_35_240M_0_a', 10164.289767503738)
('default_90_240M_0_a', 24213.22121334076)
('default_55_240M_0_a', 15035.20434308052)
('default_45_240M_0_a', 14055.135337591171)
('default_80_240M_0_a', 20954.17534804344)
('default_40_240M_0_a', 11142.362161874771)
('default_65_240M_0_a', 18426.731356859207)
('default_10_240M_0_a', 3268.3630044460297)
('default_20_240M_0_a', 6411.3104956150055)
('default_95_240M_0_a', 27333.738883972168)
('default_50_240M_0_a', 14098.512595891953)
('default_70_240M_0_a', 19539.83097410202)
('default_85_240M_0_a', 21437.86607336998)
('default_60_240M_0_a', 17955.175944805145)
('default_100_240M_0_a', 26875.29162478447)
```

LeMethod module size static:

```text
('lemethod_50_1_8_1000M_0.6_0_a', 13777.629513502121)
('lemethod_50_1_8_800M_0.6_0_a', 11546.70026254654)
('lemethod_50_1_8_700M_0.6_0_a', 9748.25587797165)
('lemethod_50_1_8_500M_0.6_0_a', 6889.60485959053)
('lemethod_50_1_8_900M_0.6_0_a', 12610.491896867752)
('lemethod_50_1_8_400M_0.6_0_a', 5790.1327929496765)
('lemethod_50_1_8_240M_0.6_0_a', 3290.0889167785645)
('lemethod_50_1_8_300M_0.6_0_a', 4203.773760318756)
('lemethod_50_1_8_600M_0.6_0_a', 8236.326235294342)
```

LeMehtod module size dynamic:

```text
('lemethod_50_1_5_300M_0.9_1_a', 4273.3850309848785)
('lemethod_50_1_5_240M_0.9_1_a', 3495.0027499198914)
('lemethod_50_1_5_600M_0.9_1_a', 7880.417015552521)
('lemethod_50_1_5_400M_0.9_1_a', 5618.673431634903)
('lemethod_50_1_5_500M_0.9_1_a', 6805.026723384857)
('lemethod_50_1_5_700M_0.9_1_a', 9046.178564786911)
('lemethod_50_1_5_1000M_0.9_1_a', 13098.732275009155)
('lemethod_50_1_5_800M_0.9_1_a', 10632.447079181671)
('lemethod_50_1_5_900M_0.9_1_a', 11930.21201133728)
```

Default module size static:

```text
('default_50_1000M_0_a', 61091.92679667473)
('default_50_240M_0_a', 14098.512595891953)
('default_50_300M_0_a', 17585.899214744568)
('default_50_600M_0_a', 36552.806321144104)
('default_50_900M_0_a', 54248.361621141434)
('default_50_400M_0_a', 23631.344161510468)
('default_50_800M_0_a', 47870.46883177757)
('default_50_700M_0_a', 41363.50402927399)
('default_50_500M_0_a', 30393.862632989883)
```

Default module size dynamic:

```text
('default_50_1000M_1_a', 61445.63865566254)
('default_50_240M_1_a', 14085.683629512787)
('default_50_700M_1_a', 42950.271661281586)
('default_50_900M_1_a', 53526.71126914024)
('default_50_500M_1_a', 30951.299822092056)
('default_50_300M_1_a', 17817.093485593796)
('default_50_600M_1_a', 35873.68512964249)
('default_50_400M_1_a', 24254.852313041687)
('default_50_800M_1_a', 47044.15779590607)
```

LeMethod link ratio static:

```text
('lemethod_50_2_1225_8_240M_0.6_0_a', 3290.0889167785645)
('lemethod_50_2_980_8_240M_0.6_0_a', 3239.6564877033234)
('lemethod_50_2_490_8_240M_0.6_0_a', 3472.937007665634)
('lemethod_50_2_613_8_240M_0.6_0_a', 3552.369918346405)
('lemethod_50_2_1103_8_240M_0.6_0_a', 3431.5463922023773)
('lemethod_50_2_368_8_240M_0.6_0_a', 3291.103330850601)
('lemethod_50_2_735_8_240M_0.6_0_a', 3329.3765330314636)
('lemethod_50_2_245_8_240M_0.6_0_a', 3538.0899465084076)
('lemethod_50_2_858_8_240M_0.6_0_a', 3601.9079093933105)
('lemethod_50_2_123_8_240M_0.6_0_a', 4240.681917190552)
```

LeMethod link ratio dynamic:

```text
('lemethod_50_2_1225_5_240M_0.9_1_a', 3495.0027499198914)
('lemethod_50_2_1103_5_240M_0.9_1_a', 3433.6230602264404)
('lemethod_50_2_613_5_240M_0.9_1_a', 3547.7539336681366)
('lemethod_50_2_368_5_240M_0.9_1_a', 3503.8685235977173)
('lemethod_50_2_735_5_240M_0.9_1_a', 3429.5893981456757)
('lemethod_50_2_980_5_240M_0.9_1_a', 3312.3646597862244)
('lemethod_50_2_123_5_240M_0.9_1_a', 4488.7337918281555)
('lemethod_50_2_858_5_240M_0.9_1_a', 3559.4618995189667)
('lemethod_50_2_245_5_240M_0.9_1_a', 3498.226425409317)
('lemethod_50_2_490_5_240M_0.9_1_a', 3606.440408229828)
```
Default base static:

```text
('default_50_240M_0_a', 14098.512595891953)
```

Default base dynamic:

```text
('default_50_240M_1_a', 14085.683629512787)
```
