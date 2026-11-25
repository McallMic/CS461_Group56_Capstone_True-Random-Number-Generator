# Entropy Estimation and Randomness Validation in a TRNG Pipeline: Background

## Introduction

True Random Number Generators (TRNGs) operate by converting unpredictable physical processes, known as noise sources, into sequences of random bits. In the context of TRNG validation, the important metric is not whether the output appears random, but rather the actual amount of unpredictability (entropy) present. While statistical suites like NIST SP 800-22 or Dieharder can identify blatant failures, they are insufficient for proving entropy, as deterministic generators can also pass these tests [1], [2], [3]. This document provides the necessary background to quantify entropy, following the framework established in NIST SP 800-90B. Under this standard, an entropy source consists of three primary elements: a noise source, health tests, and an optional conditioning component [3].

---

## 1. Entropy Definitions

Entropy measures how uncertain we are about the outcome of a random variable. Suppose a random variable $X$ takes values $x_i$ with probabilities $p_i$. Several definitions of entropy exist, and they answer different questions.

### 1.1 Shannon entropy

$$H_1(X) = -\sum_i p_i \log_2 p_i$$

Shannon entropy represents the average amount of information, measured in bits, per outcome [4], [5]. While this metric is appropriate for applications in data compression and communication, it is insufficient for security contexts, as an average value can obscure the existence of highly probable outcomes. For instance, consider a distribution where one value has probability 0.5 and the other half of the probability mass is spread over $2^{100}$ values. It has a Shannon entropy of about 51 bits. However, the system remains much more vulnerable than the entropy estimate would indicate, as an attacker could correctly predict the output on the first attempt with 50% probability.

### 1.2 Min-entropy

$$H_\infty(X) = -\log_2 \left( \max_i p_i \right)$$

In contrast, min-entropy is determined solely by the most probable outcome. It quantifies the difficulty of predicting the output on the first attempt, representing the worst-case scenario from a security perspective [3]. For any distribution, $H_\infty \le H_1$, with equality only for the uniform distribution. In the example above, $H_\infty = 1$ bit. **SP 800-90B uses min-entropy throughout** [3].

### 1.3 Rényi entropy and collision entropy

Shannon entropy and min-entropy are both special cases of Rényi entropy of order $\alpha$ [6]:

$$H_\alpha(X) = \frac{1}{1-\alpha} \log_2 \sum_i p_i^\alpha$$

Shannon entropy is the limit as $\alpha \to 1$, and min-entropy is the limit as $\alpha \to \infty$. The case $\alpha = 2$ is the *collision entropy*, $H_2 = -\log_2 \sum_i p_i^2$. It is a measure of uncertainty in a random variable tied to the probability that two independent samples drawn from the same distribution will match. The ordering is $H_\infty \le H_2 \le H_1$.

### 1.4 Full entropy

A bitstring of length $n$ is considered to possess *full entropy* when its min-entropy is approximately $n$ bits, so that every one of the $2^n$ values is close to equally likely. The formal definition provided by NIST permits a marginal deviation from perfect uniformity [7], [8]. This property is a prerequisite for various security applications, notably the seeding of deterministic random bit generators (DRBGs), which necessitate either full-entropy inputs or for a stated number of bits of min-entropy.

### 1.5 Entropy rate for sequences

Rather than producing a single random variable, a noise source yields a continuous sequence of samples. If the samples are **independent and identically distributed (IID)**, the aggregate entropy scales linearly with the number of samples $n$. However, physical noise sources typically exhibit dependencies between samples, including correlation, drift, or periodic components. In such cases, the appropriate metric is the *entropy rate*, defined as the conditional entropy of the subsequent sample given the history of all preceding samples [5]. Ignoring dependence makes us overestimate entropy, so non-IID sources need more careful estimation (Section 3).

---

## 2. Noise Source Model

### 2.1 What a noise source is

The noise source is the part of the TRNG where the nondeterminism comes from. It usually has two parts [3]:

- **An analog noise process.** Examples include thermal noise in a resistor, shot noise, timing jitter in free-running ring oscillators, metastability in latches, and quantum effects such as photon arrival times or beam-splitter paths.
- **A digitization step.** This turns the analog behavior into discrete *raw samples*. For example: sampling a high-frequency jittery source with a slower reference clock or employing a comparator to measure voltage fluctuations relative to a threshold.

SP 800-90B distinguishes **physical** noise sources, which use dedicated hardware, from **non-physical** ones, which use system events such as interrupt timing or disk seek times [3].

### 2.2 Why a model matters

Statistical estimators can only see the data they are given. They cannot tell real randomness from complex deterministic behavior. A **stochastic model** addresses this limitation. It is a mathematical description of the physical process that predicts the distribution of the raw samples, or at minimum, establishes a lower bound on their entropy.

Ring-oscillator TRNGs serve as a representative example of this approach. In these systems, models typically characterize the accumulated phase jitter as a random walk, where the jitter variance increases approximately linearly with the accumulation time. By analyzing the jitter-to-period ratio in conjunction with the sampling interval, a lower bound on the entropy per sampled bit can be derived. Furthermore, the stochastic model identifies potential vulnerabilities, such as global deterministic noise. In this example, this deterministic pattern could be caused by power-supply coupling, locking between oscillators, and sensitivity to temperature and voltage.

### 2.3 Key modeling assumptions to check

- **Independence:** Are samples independent, or does one sample affect the next?
- **Stationarity:** Does the distribution stay the same over time and across operating conditions?
- **Source of randomness:** Does the claimed randomness come from a truly nondeterministic process and not from an external signal someone could control?
- **Failure modes:** How can the source fail, and would the health tests detect each failure? (Section 4).

### 2.4 When entropy should be measured

Entropy estimation must be performed on the raw, unconditioned samples directly from the digitizer. Conditioning can make biased or correlated data *look* uniform without adding any entropy. Testing after conditioning would therefore hide the real behavior of the source.

---

## 3. Entropy Estimation (NIST SP 800-90B)

SP 800-90B gives a procedure for estimating the min-entropy per sample of a noise source from recorded data [3].

### 3.1 Data collection

The data collection must meet the following requirements:

- **Sequential data:** at least 1,000,000 consecutive raw samples from one run of the noise source.
- **Restart data:** 1,000 restarts of the source, with 1,000 samples recorded after each restart, arranged as a $1000 \times 1000$ matrix [3].


### 3.2 Choosing a track: IID or non-IID

An evaluation must be made for whether the data can be treated as IID.

If a source's data is claimed as IID, it should be checked via **permutation tests**. A set of test statistics (excursion, runs, number of increases/decreases, covariance, compression ratio, and others) is computed for the original data and for the 10,000 shuffled versions. If the data really is IID, shuffling should not change the statistics in any systematic way. Therefore, any original statistic that holds an extreme rank relative to the shuffled distributions is evidence against the data's IID claim [3].
Additional investigation is performed via chi-square tests for independence, along with a longest-repeated-substring test [3].

If the data is verifiably IID, the **IID procedure** is used. Otherwise the **non-IID procedure** is used. Most physical sources end up utilizing the latter due to inherent small correlations.

### 3.3 The IID procedure

For IID data, the **Most Common Value (MCV)** estimate is all that is necessary. The estimate is calculated as follows:
 Let $\hat p$ be the proportion of the most common value in $L$ samples. A 99% upper confidence bound is

$$p_u = \min\left(1,\ \hat p + 2.576\sqrt{\frac{\hat p(1-\hat p)}{L-1}}\right), \qquad H = -\log_2 p_u.$$

Using the upper bound on $p$ makes the entropy estimate conservative [3].

### 3.4 The non-IID procedure

For non-IID data, SP 800-90B runs ten estimators and takes the **minimum** [3]. Each estimator is designed to catch a different kind of weakness:

| Estimator | Idea |
|---|---|
| Most Common Value | Bias toward one value. |
| Collision | Average time until a repeated value appears; related to collision entropy. |
| Markov | Models the data as a first-order Markov chain and finds the most likely long sequence. |
| Compression | Based on Maurer's universal test: how well can the data be compressed? [9] |
| t-Tuple | Frequency of the most common length-$t$ substrings. |
| Longest Repeated Substring (LRS) | Probability of long repeated patterns. |
| MultiMCW prediction | Predicts the next sample as the most common value in several sliding windows. |
| Lag prediction | Predicts the next sample from a sample a fixed number of steps back. |
| MultiMMC prediction | Predicts with Markov models of several orders. |
| LZ78Y prediction | Predicts using a dictionary of previously seen patterns. |

The **prediction estimators** are based on the principle that if any simple predictor can guess the next sample better than chance, the source has less entropy than it would seem from rudimentary analysis. They are a gauge for both the overall prediction accuracy and the longest run of correct predictions, and use whichever implies lower entropy.

This approach of taking the minimum is intentionally conservative. Empirical studies indicate that various estimators may exhibit bias, either underestimating or overestimating entropy depending on the underlying distribution. Consequently, the selection of the most appropriate estimator for a specific noise source remains a subject of active research.


### 3.5 Limits of statistical estimation

Estimators can only find patterns they were designed to look for. A source can have hidden structure, such as a cryptographic generator pretending to be a noise source, and still get a high estimate. This is why stochastic models are emphasized for physical sources.

---

## 4. Health Tests

Entropy estimation occurs as a single procedure in a controlled environment. To check that a noise source continues to meet its estimated entropy level, health tests run **continuously in the deployed device**. Their job is to detect when the noise source has failed or degraded, for example through component aging or exposure to extreme temperatures.

### 4.1 Types of health tests

SP 800-90B describes three types of health test [3]:

- **Start-up tests:** run on power-up, before any output is used. They must cover at least 1,024 consecutive samples.
- **Continuous tests:** run on every raw sample during normal operation.
- **On-demand tests:** run when an application or operator requests them.

When a test fails, the entropy source must report an error and stop producing output that is treated as random. Some designs allow a set number of intermittent failures before declaring a permanent error.

### 4.2 False positive rate

The tests are designed around a chosen false positive probability $\alpha$, which represents the chance that a *healthy* source triggers an alarm. SP 800-90B recommends $2^{-20} \le \alpha \le 2^{-40}$ [3]. A smaller $\alpha$ means fewer false alarms but a slower response to actual failures.

### 4.3 Repetition Count Test (RCT)

The RCT is designed to detect a source that gets **stuck** on one value. It counts how many times in a row the same sample has appeared. Given a source has min-entropy $H$ per sample, the probability of any specific value occuring is at most $2^{-H}$. So $C$ identical samples in a row happen with probability at most $2^{-H(C-1)}$. Therefore the threshold for triggering an RCT alarm is defined as:

$$C = 1 + \left\lceil \frac{-\log_2 \alpha}{H} \right\rceil$$

An alarm is raised if a value repeats $C$ or more times in a row. For example, with $H = 1$ bit/sample and $\alpha = 2^{-20}$, the cutoff is $C = 21$.

### 4.4 Adaptive Proportion Test (APT)

While the RCT detects a source that is stuck on one value, the APT detects a **large loss of entropy** that does not show up as a stuck output, such as the emergence of a strong bias. The test utilizes a window of size $W$, where $W = 1024$ for binary sources and $W = 512$ for non-binary sources, and counts how often the first sample in the window occurs. The cutoff threshold $C$ is determined as the minimum count that a healthy source would reach with probability at most $\alpha$, taken from the binomial distribution:

$$C = 1 + \text{CRITBINOM}(W,\ 2^{-H},\ 1 - \alpha)$$

(CRITBINOM is a function from Microsoft Excel that gives the binomial inverse CDF. This specific function is cited only due to its use by SP 800-90B. Any equivalent function, such as *binoinv* in MATLAB, would apply)


## References

[1] A. Rukhin et al., "A Statistical Test Suite for Random and Pseudorandom Number Generators for Cryptographic Applications," NIST SP 800-22 Rev. 1a, 2010. https://doi.org/10.6028/NIST.SP.800-22r1a

[2] R. G. Brown, D. Eddelbuettel, and D. Bauer, "Dieharder: A Random Number Test Suite." https://webhome.phy.duke.edu/~rgb/General/dieharder.php

[3] M. S. Turan, E. Barker, J. Kelsey, K. A. McKay, M. L. Baish, and M. Boyle, "Recommendation for the Entropy Sources Used for Random Bit Generation," NIST SP 800-90B, Jan. 2018. https://doi.org/10.6028/NIST.SP.800-90B

[4] C. E. Shannon, "A Mathematical Theory of Communication," *Bell System Technical Journal*, vol. 27, pp. 379–423, 623–656, 1948.

[5] T. M. Cover and J. A. Thomas, *Elements of Information Theory*, 2nd ed. Wiley, 2006.

[6] A. Rényi, "On Measures of Entropy and Information," in *Proc. 4th Berkeley Symposium on Mathematical Statistics and Probability*, vol. 1, pp. 547–561, 1961.

[7] D. Buller, A. Kaufer, A. Roginsky, and M. S. Turan, "Discussion on the Full Entropy Assumption of the SP 800-90 Series," NIST IR 8427, Apr. 2023. https://doi.org/10.6028/NIST.IR.8427

[8] E. Barker, J. Kelsey, K. McKay, A. Roginsky, and M. S. Turan, "Recommendation for Random Bit Generator (RBG) Constructions," NIST SP 800-90C, Sep. 2025. https://doi.org/10.6028/NIST.SP.800-90C

[9] U. M. Maurer, "A Universal Statistical Test for Random Bit Generators," *Journal of Cryptology*, vol. 5, no. 2, pp. 89–105, 1992.
