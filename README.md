# Generalizing Verifiable Instruction Following

This repo contains IFBench, which is a new, challenging benchmark for precise instruction following. 

## IFBench
IFBench consists of two parts:

- OOD Constraints: 58 new and challenging constraints, with corresponding verification functions. The constraint templates are combined with prompts from a held-out set of WildChat (Zhao et al. 2024).

- Constraint Isolation in 2 turns: The prompt and the constraint are separated over two turns, i.e. the first turn is the user prompt and the model's response to the prompt, and the second turn is the constraint that modifies the initial prompt.

## How to run the evaluation

## Released Datasets
The training and test datasets can be found in this [collection](https://huggingface.co/collections/allenai/ifbench-683f590687f61b512558cdf1).
The test dataset is: https://huggingface.co/datasets/allenai/IFBench_test .
The IF-RLVR train dataset is: https://huggingface.co/datasets/allenai/IF_multi_constraints_upto5 .

## RLVR for Precise Instruction Following
We also release RLVR 

## Licensing

This codebase is licensed under Apache 2.0 as given in [LICENSE](./LICENSE).


## Acknowledgements

Parts of IFBench are built upon and extend [IFEval](https://github.com/google-research/google-research/tree/master/instruction_following_eval) (Zhou et al. 2023) and we would like to thank them for their great work!


## Citation

If you used this repository or our models, please cite our work:

```bibtex
@misc{pyatkin2025generalizing,
   title={Generalizing Verifiable Instruction Following}, 
   author={Valentina Pyatkin and Saumya Malik and Victoria Graf and Hamish Ivison and Shengyi Huang and Pradeep Dasigi and Nathan Lambert and Hannaneh Hajishirzi},
   year={2025},
   eprint={TODO},
   archivePrefix={arXiv},
   primaryClass={cs.CL}
}
