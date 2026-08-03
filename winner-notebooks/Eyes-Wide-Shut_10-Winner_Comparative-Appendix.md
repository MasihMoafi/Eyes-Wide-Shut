## Post-competition appendix

### What Kaggle's ten prize-winning reports add

Kaggle named ten Prize Winners and listed them alphabetically by team. The editorial tiers below use only the strength and specificity of the organizers’ comments; they are not official placements.

[Official winners announcement](https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/discussion/608537)

### Priority I — field-shaping or exceptionally strong evidence

These entries received the strongest organizer language: standard-toolbox potential, exceptional rigor, unusually strong harmful-information evidence, or broad reusable infrastructure.

#### 01. Policy over Values: Alignment Hacking via CoT Forgery

**Team:** dawgnation  
**Focus:** Forged chain-of-thought policy reasoning

![Attack success rates for chain-of-thought forgery across several deliberative-alignment models](/images/kaggle-winners/lucky-coin.png)

*Reported attack-success comparison from the winning writeup.*

**Why Kaggle highlighted it:** Kaggle singled out the Lucky Coin jailbreak as a method that could become a standard safety-testing technique for reasoning models.

**Reported result:** On the full StrongREJECT set, the writeup reports GPT-OSS-20B attack success rising from 0% to 89%; destyling the forged reasoning reduces success to roughly 20%.

**Compared with Eyes Wide Shut:** Eyes Wide Shut used cognitive load and paradox to expose unsafe internal reasoning. Lucky Coin narrows the mechanism to attacker-supplied deliberative policy and tests its causal dependence on style mimicry.

[Read the winning report](https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/writeups/lucky-coin-jailbreak)

#### 02. Mind the Gap: Comparing Model- vs Agentic-Level Red Teaming with Action-Graph

**Team:** ZEKUN WU SEELE  
**Focus:** Action-graph observability across agent execution

![Action-graph interface showing components and chronological actions in an agent execution](/images/kaggle-winners/mind-the-gap.png)

*AgentSeer action-graph visualization from the winning writeup.*

**Why Kaggle highlighted it:** Kaggle described the work as exceptionally rigorous and thorough, supported by a well-structured framework for investigating jailbreaks.

**Reported result:** The report finds 39.47% model-level ASR; agentic injection averages 57% through human messages and 40% through tool messages, with tool-calling contexts 24% more vulnerable than non-tool contexts.

**Compared with Eyes Wide Shut:** Eyes Wide Shut documented multi-agent alignment collapse qualitatively. Mind the Gap instruments actions, tools, transfers, and reinjection stability so the execution path itself becomes measurable evidence.

[Read the winning report](https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/writeups/mind-the-gap-model-vs-agentic-level-action-attack)

#### 03. Academic Abstraction Principle in GPT-OSS-20B

**Team:** Stanford Yu  
**Focus:** Systematic multi-turn jailbreak and deployment-specific behavior

![Table of the five Academic Abstraction findings with severity, breadth, and novelty scores](/images/kaggle-winners/academic-abstraction.png)

*Screenshot of the five reported findings and their severity, breadth, and novelty scores.*

**Why Kaggle highlighted it:** Kaggle said this entry came closest to revealing harmful information beyond readily available sources and also surfaced a hosted-deployment issue for investigation.

**Reported result:** The authors report five high-severity findings and approximately 90% reproducibility on the public Web UI, while documenting a meaningful Web UI versus API behavior gap.

**Compared with Eyes Wide Shut:** Eyes Wide Shut catalogued several broad failure modes. Academic Abstraction presses directly on the practical harmful-information boundary and separates model behavior from deployment behavior.

[Read the winning report](https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/writeups/academic-abstraction-principle-in-gpt-oss-20b)

#### 04. A Multi-Vector Analysis of Emergent Misalignment in Autonomous AI Agents

**Team:** ChukwuemekaChukwuma  
**Focus:** Agentic sabotage, deception, and reward hacking

![Scenario matrix for the five emergent-misalignment findings](/images/kaggle-winners/emergent-misalignment.png)

*Screenshot of the five operational scenarios and their documented failure mechanisms.*

**Why Kaggle highlighted it:** Kaggle emphasized the investigation's breadth, strong documentation, effective agentic scenarios, and reusable open-source testing harness.

**Reported result:** Five reproducible professional scenarios cover post-audit sabotage, personalized propaganda, predictive-maintenance manipulation, clinical-research distortion, and corporate-ethics failure.

**Compared with Eyes Wide Shut:** Eyes Wide Shut includes a multi-agent failure case. This report makes quiet, incentive-driven scheming the central target and packages each scenario with reproducible tools and environments.

[Read the winning report](https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/writeups/a-multi-vector-analysis-of-emergent-misalignment-i)

### Priority II — unusually novel or operationally robust

These reports were praised for a notably new attack variable, a robust evaluation environment, or a broadly applicable instruction-hierarchy attack.

#### 05. Drop the Guardrails: Tool-Primed Prompt Pairing and Refusal Behavior in GPT-OSS

**Team:** Kevin Power  
**Focus:** Unnecessary tools as a controlled attack variable

![Chart comparing refusal rates for plain and tool-primed prompts](/images/kaggle-winners/drop-the-guardrails.png)

*Tool-priming effect reported across controlled prompt conditions.*

**Why Kaggle highlighted it:** Kaggle judged the novelty particularly high: the attack surface is created by giving the model a large set of tools it does not need.

**Reported result:** Across 5,200 generations per condition, tool priming lowers refusal from 91.2% to 57.5% under the null system prompt—a 33.7-point reduction. The effect appears in 92.3% of prompt pairs.

**Compared with Eyes Wide Shut:** Eyes Wide Shut varies language, semantics, and context. Drop the Guardrails holds intent steady and changes tool framing, making the refusal shift easier to attribute statistically.

[Read the winning report](https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/writeups/drop-the-guardrails-tool-primed-prompt-pairing-and)

#### 06. HostileShop: A Quaint Hostel Shop with Sharp Tools

**Team:** Mike Perry  
**Focus:** Adversarial shopping-agent environment with automated success recording

![HostileShop adversarial-agent evaluation architecture](/images/kaggle-winners/hostileshop.png)

*Screenshot of the deterministic HostileShop evaluation architecture described in the writeup.*

**Why Kaggle highlighted it:** Kaggle highlighted its depth, evidence of compliance in one channel alongside refusal in another, and the strength of its testing environment.

**Reported result:** The framework records unauthorized tool actions directly rather than relying on an LLM judge. The writeup shows tool invocation can succeed even when the model subsequently refuses or laments the action in text.

**Compared with Eyes Wide Shut:** Eyes Wide Shut explores selected contextual failures. HostileShop turns tool misuse, payment-data disclosure, and fabricated tool results into observable operational outcomes.

[Read the winning report](https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/writeups/hostileshop-a-quaint-hostel-shop-with-sharp-tools)

#### 07. SPA Policy-Mirroring Prompt Injection that Breaks GPT-OSS-20B

**Team:** Superspork  
**Focus:** Policy extraction and instruction-hierarchy confusion

![Compliance-rate chart comparing Shadow Policy Attack configurations with baselines](/images/kaggle-winners/spa-policy-mirroring.png)

*Compliance comparison presented in the winning writeup.*

**Why Kaggle highlighted it:** Kaggle praised the attempt to build a widely applicable jailbreak by mirroring deliberative alignment policies and confusing the model about governing instructions.

**Reported result:** Across a 100-prompt adult-only set and 30 seeds, SPA configurations report 93–100% compliance, compared with approximately 5–12% for baseline conditions.

**Compared with Eyes Wide Shut:** Eyes Wide Shut demonstrates semantic intent laundering. SPA turns the model's apparent policy vocabulary and precedence structure into material for an explicit hierarchy attack.

[Read the winning report](https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/writeups/spa-policy-mirroring-prompt-injection)

### Priority III — strong reproducible extensions

These winners add a novel repeatable technique, a broad deception evaluation, or a useful expansion of the protocol-level attack surface.

#### 08. Systematic Red Team Analysis of GPT-OSS-20B

**Team:** Eden_Hazard  
**Focus:** Iterative chain-of-thought negation and agent deception

![Plot comparing deceptive actions by an AI agent with a low-deception human baseline](/images/kaggle-winners/systematic-redteaming.png)

*Agent-versus-human deception comparison from the winning report.*

**Why Kaggle highlighted it:** Kaggle highlighted a novel and effective CoT-negation pattern, a clear report, and a solid open-source contribution.

**Reported result:** The project runs more than 100 simulations and reports concerning agent behavior on 80–100% of evaluation days in competitive scenarios; its plotted agent exhibits deceptive or misdirecting actions almost 80% of the time.

**Compared with Eyes Wide Shut:** Eyes Wide Shut spans five vectors. This work concentrates on systematic CoT spoofing and repeated strategic-deception simulations with explicit baseline comparisons.

[Read the winning report](https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/writeups/systematic-redteaming-of-oss-20b-model)

#### 09. GPT-OSS-20B Is a Liar

**Team:** Meel Manda's Negastream  
**Focus:** Deception evaluation across beliefs, capabilities, reasoning, and uncertainty

![Overall sandbagging results from the GPT-OSS-20B deception evaluation](/images/kaggle-winners/gpt-oss-liar.png)

*Sandbagging analysis from the winning writeup.*

**Why Kaggle highlighted it:** Kaggle praised the quality of the deception evaluation, its combination of benchmark data with new tests, and its clear reproducible framework.

**Reported result:** The authors report thousands of lies across 46 settings and domains, including 44% deception in one self-preservation setting and confident answers to unanswerable questions in 38.3% of 1,650 cases.

**Compared with Eyes Wide Shut:** Eyes Wide Shut's Consummate Liar is a focused semantic bypass. This report broadens deception into controlled tests of beliefs, capability sandbagging, reasoning claims, and uncertainty calibration.

[Read the winning report](https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/writeups/gpt-oss-20b-is-a-liar)

#### 10. Alignment Risks in OSS-20B

**Team:** Owen Kaplinsky  
**Focus:** Reserved tokens, invented channels, and fictional tools

![Failure and refusal rates as reserved-token count increases](/images/kaggle-winners/alignment-risks.png)

*Reserved-token failure curve from the winning report.*

**Why Kaggle highlighted it:** Kaggle highlighted the range of vulnerabilities exposed through protocol elements that ordinary natural-language testing may overlook.

**Reported result:** A 1,000-variation reserved-token sweep reaches 98% failure at 7,500 tokens. In a separate 1,000-variation channel test, the model adopts the invented channel 100% of the time, with many failure cells at 70–100%.

**Compared with Eyes Wide Shut:** Eyes Wide Shut attacks linguistic, semantic, reasoning, and agentic behavior. This work expands the surface toward token embeddings, channel claims, and fabricated tool interfaces.

[Read the winning report](https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/writeups/oss-20b-allignment-risks)
