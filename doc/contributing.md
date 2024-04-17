# Introduction to Contributing

We welcome anyone to contribute to this project, even if you are new to open-source. There are two ways to contribute to
this project. The first way is to use the dataset annotation tools `fgdat` provided by the project to build your own
dataset. The second way is to maintain the `fgdat` code or to create new annotation tools.

## Build Your Own Dataset

If you have built your own dataset using `fgdat` and wish for it to be used by more people, then releasing it on this
project is a good option.

### Annotation Workflow

A complete data set annotation and publication process includes 4 steps:  
1.Fork the *FormalGeo-Datasets*.  
2.Under the `projects\` of the project, create your own project and collaborate within your team to annotate the
dataset.  
3.Submit pull requests to *FormalGeo-Datasets*.  
4.Projects that meet the **Project Submission Guidelines** will be merged into *FormalGeo-Datasets*.

### Project Submission Guidelines

You can look at the other projects under `projects/` to get a general idea of the structure of a project.  
A standardized dataset release project is as follows:

    project_name/
    ├── gdl/
    │   ├── doc/
    │   │   └── ...
    │   ├── predicate_GDL.json
    │   └── theorem_GDL.json
    ├── problems/
    │   ├── 1.json
    │   └── ...
    ├── diagrams/
    │   ├── 1.png
    │   └── ...
    ├── expanded/
    │   ├── 1.json
    │   └── ...
    ├── files/
    │   └── ...
    ├── info.json
    ├── LICENSE
    └── README.md

Project will be packaged into `dataset_name-dataset_version.tar.7z` and published to `FormalGeo-Datasets/released/`,
which is also where users will download your dataset. Submissions containing files or folders other than the
aforementioned ones will be rejected. You should delete irrelevant files in `project_name/` before submitting a pull
request.

#### gdl/

coming soon...

#### problems/

coming soon...

#### diagrams/

coming soon...

#### expanded/

coming soon...

#### files/

This folder can contain any other files you wish to add, such as theorem information for accelerated searching like
`t_msg.json`, dataset statistics, etc. The total size of the files should not exceed 10MB.

#### info.json

coming soon...

#### LICENSE

coming soon...

#### README.md

coming soon...

## Develop Dataset Annotation Tools

coming soon...