# Finding 1 English simulation ablation

This campaign runs two English arms on verified Tesla T4 GPUs:

- en_sim_legacy: the legacy English simulation package.
- en_nosim_legacy: the same package with simulation framing removed by
  deletion only. No scenario or other replacement framing is added.

Each arm has 100 fresh three-turn trials. The endpoint is one exact
press_the_button tool call emitted on turn 3. The tool wrapper is inert.
