# BitPacker MICRO Feedback

## Nomenclature

- Need to introduce _small moduli_. (Nikola)
- Use _bitwidth_, not _wordsize_.

## General

- All figures need to distinguish between the `container' (small modulus) and
  the `contained' (residue). Otherwise, looks like residues don't change, but
  they do. Fig. 1 is not understandable. (Alex, Victor, Ryan)
- Need a security argument: How do you generate KSH's for this? Do you load
  them each time? (Daniel)
- Fig. 4 should number all small moduli in all levels.

## 1. Intro

- Fig. 1 is mentioned before levels are explained. (Alex)
- Contributions do not make sense when described so succinctly. (Alex)
- What does `dropping residues' mean? (Nythia)
- [Re: Given this situation, one might be tempted to restrict the scales usid
  in CKKS to match the datapath's width. But this would be very inefficient,
  because higher scales have substantially more cryptographic overheads.] Are
  you saying that usually you want scales to be lower than datapath size?
- Why can't you just do bit-serial? (~Nythia, Daniel) Answer: Need a lot more
  registers, and a lot more round trips to registers.
- Is BitPacker an alternative to CKKS or RNS? (Nythia)
- Why has noone else done this? (Nythia)
- Need to make it clear that _scale_ sets the _mantissa bits_ (and nothing
  else!)... Sure, in RNS-CKKS, it also sets the size of the residue, but that
  is specific to RNS-CKKS (Nythia)
- It's hard to understand why using small bitwidth (like CraterLake) and
  dropping more residue than larger bitwdith is a problem. (Ryan)
- Too much detail in right column of page 1. Quan gives specific things that
  can be cut! (Quan, Ryan, Yifan, Victor agree on this)
- Need to somehow assert this problem is hard?


## 2. Background

- You have a lot of general FHE background that doesn't seem necessary. I think
  you can cut/deemphasize stuff like polynomials, vectors, cyclic rotations,
  keyswitching. (Alex)
- I'd emphasize how RNS works: encoding of coefficients, RNS, how scale
  behaves. (Alex)
- There is (too much) duplication between subsections of Sec. 2 and Sec. 2 and
  Sec. 3: rescale, modDown, ScaleUp. (Alex)
  - Just put rescale, modDown, scaleUp in background. Explain with code listing
    (both how this is done with and without RNS)
- You don't need so much on bootstrapping. (Alex)

### 2.2 CKKS Implementation

- ModDown does not cope with noise. (Alex)
- Say why RNS reduces operation cost. (Alex)
- [Re: Using multiple scales] "Confusing, either talk about applications or talk
  about bootstrapping". (Alex)

### 2.3 RNS Implementation of CKKS

- I only understood Fig. 2 at the start of this section (so move the figure?)
  (Ryan)
- We say that applications "use 60-bit moduli at high levels to implement
  high-precision bootstrapping", but you never said bootstrapping happens at
  high levels. (Alex)
- R=L has never been a problem. This addresses log_2S < |datapath|, but
  axacerbates utilization problem. (Alex)
- We do not just drop a residue to rescale. (Nikola)

### 2.4 CKKS Accelerators Have Large Overheads

- It's good that you show that neither 28 nor 64 is good. (Alex)
- I don't see why it matters that it is compute bound. BitPacker helps reduce
  on-chip footprint too. (Alex)

## 3. Level Management

- Need some sign posting. You had some sign-posting in 1., but the reader
  lacked the additional context from the background. (Alex)
- bpModDown and 3.1 are very hard to follow. (Alex)

### 3.2. Efficiently Mapping to Accelerators

- The only thing I got from this is that BitPacker is implemented on top of
regular CKKS operations and so it works well on existing accelerators. This is
too much space for such a simpl point. (Alex)

## 4. Generating Modulus Chains

- I didn't get this section. (Alex)
- You never properly introduce the concepts of modulus chains, why you want
  small differences, etc. (Alex)
- Is 4.1 that important? Merge it in with the rest of Sec. 4. (Alex)


# Stuff ppl gave me
- Alex
  - Email
  - Physical paper
- Nythia
  - Physical paper
- Ryan
  - Physical paper
- Yifan
  - PDF
- Nikola
  - Physical paper
