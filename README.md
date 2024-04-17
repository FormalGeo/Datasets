# Datasets

[![Version](https://img.shields.io/badge/Version-0.0.1-brightgreen)](https://github.com/FormalGeo/Datasets)
[![License](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)
[![Survey](https://img.shields.io/badge/Survey-FormalGeo-blue)](https://github.com/FormalGeo/FormalGeo)

Dataset Annotation Tools and Dataset Release for formal Euclidean plane geometry problems. This project is based on
the Geometry Formalization Theory and utilizes FormalGeo as its problem solver.  
More information about FormalGeo will be found in [homepage](https://formalgeo.github.io/). FormalGeo is in its early
stages and brimming with potential. We welcome anyone to join us in this exciting endeavor.

## Usage

All published datasets can be found in the `./released`. [Formalgeo](https://github.com/FormalGeo/FormalGeo) provides a
dataset download and management tool, and we recommend using Formalgeo to download the datasets.

Install Formalgeo using pip:

    $ pip install formalgeo

Run python and download datasets:

    >>> from formalgeo.data import download_dataset
    >>> download_dataset(dataset_name="formalgeo7k_v1", datasets_path="your_datasets_storage_path")

Use datasets:

    >>> from formalgeo.data import DatasetLoader
    >>> dl = DatasetLoader(dataset_name="formalgeo7k_v1", datasets_path="your_datasets_storage_path")
    >>> print(dl.get_problem(pid=1))

## Released Datasets

### formalgeo7k

**Latest Version:** v1  
**Release Datetime:** 2023-11-08 13:01:26  
**Description:** 6,981 (expand to 133,818 through data augmentation) SAT-level geometry problems with complete natural
language description, geometric shapes, formal language annotations, and theorem sequences annotations.

### formalgeo-imo

**Latest Version:** v1  
**Release Datetime:** 2023-11-26 19:21:26  
**Description:** We have attempted to annotate 18 (expand to 2,627) IMO-level geometric problems, sourced from carefully
selected International Olympiads, Chinese Olympiads, and others. During the annotation process, we discovered that
IMO-level problems require more efficient construction algorithms and a more comprehensive formalization system. A
larger and more comprehensive dataset will be published after these problems are solved.

## Contributing

You can contribute additional automation scripts that facilitate dataset annotation, or use the scripts from this
project to build your own dataset.  
We welcome contributions from anyone, even if you are new to open source. Please read
our [Introduction to Contributing](./doc/contributing.md) page.

### Documentation

Everything is at [doc](./doc/doc.md). Usage of the annotation tool can be found in the [tests](./tests)
and [projects](./projects).

### Installation

This project uses [pyproject.toml](https://packaging.python.org/en/latest/specifications/declaring-project-metadata) to
store project metadata. The command `pip install -e .` reads file `pyproject.toml`, automatically installs project
dependencies, and installs the current project in an editable mode into the environment's library for convenient
project development and testing.

    $ git clone --depth 1 https://github.com/FormalGeo/Datasets.git
    $ cd Datasets
    $ conda create -n <your_env_name> python=3.10
    $ conda activate <your_env_name>
    $ pip install -e .

### Bugs

Our bug reporting platform is available at [here](https://github.com/FormalGeo/Datasets/issues). We encourage
you to report any issues you encounter. Or even better, fork our repository on GitHub and submit a pull request.

## Citation

If you wish to reference **a specific dataset**, please read the `README` file in the published dataset or contact the
dataset's author.  
If you are referencing code within the project, please use:
> Xiaokai, Zhang., Na, Zhu., Yiming, He., Jia, Zou., ... & Tuo, Leng. (2023). FormalGeo: The First Step Toward
> Human-like IMO-level Geometric Automated Reasoning. arXiv preprint arXiv:2310.18021.

A BibTeX entry for LaTeX users is:
> @misc{arxiv2023formalgeo,  
> title={FormalGeo: The First Step Toward Human-like IMO-level Geometric Automated Reasoning},  
> author={Xiaokai Zhang and Na Zhu and Yiming He and Jia Zou and Qike Huang and Xiaoxiao Jin and Yanjun Guo and Chenyang
> Mao and Zhe Zhu and Dengfeng Yue and Fangzhen Zhu and Yang Li and Yifan Wang and Yiwen Huang and Runan Wang and Cheng
> Qin and Zhenbing Zeng and Shaorong Xie and Xiangfeng Luo and Tuo Leng},  
> year={2023},  
> eprint={2310.18021},  
> archivePrefix={arXiv},  
> primaryClass={cs.AI}  
> }