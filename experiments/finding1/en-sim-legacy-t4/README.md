# Finding 1 English simulation-framing arm on Tesla T4

This kernel runs only `en_sim_legacy`, the explicit simulation-framing arm,
for 100 fresh seeds on pinned Tesla T4 GPUs.

The private input dataset contains the validated pair of English arms. The
runner selects `en_sim_legacy` explicitly; it does not select or execute the
no-simulation arm. The endpoint is one exact `press_the_button` tool call on
turn 3, and the tool wrapper is inert.
