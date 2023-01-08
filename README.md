# Open VFX Framework

Python framework used as a foundation to build different universal pipeline tools collectively known as the Open VFX Toolkit. The framework allows the tools to operate on different folder structures adopted by each studio.

Each studio use a yaml configuration file to define what are their location for different path types.

## Background

For decades every studio has developed their own pipeline tools. And even worse, sometimes studios run for a while without having such tools.

Most of the time the tools requirements are the same but because folder structures for projects vary per studio, very few off-the-shelf tools have been created to work across studios.

This project aims at providing a framework that can be configured per studio to adapt to custom folder structures.

## Concept

### Context
At the base of the Open VFX framework is the notion of context. The context is nothing more than where a tool operates. In simpler terms, most of the time it means what a user is working on.

What defines a context is simply the collection of all required components that separate this context from another. The simplest example would be a project context that requires only a project name to tell it apart from another project.

However, for a shot context, it could not use only the shot number to define the context because the same shot number can exist for different projects. It still needs the project component along with potentially an episode and a sequence components to uniquely define it.

Those components are referred to path fragments or just fragments in the Open VFX framework.

### Location Model
A location model is a template that defines a type of path on the network. The structure is just like a normal path except that the varying portions per context are defined as a tag representing the context component name. For example the path /prod/jobs/MyProject could use /prod/jobs/\<proj> as a project location model with \<proj> representing any project name in the folder structure.

## Features

### Translator Layer
Part of the Open VFX framework can be thought of as a path translator. Tools talk to a translator layer to request a path derived from a location model and a context.

### Context Extractor
Similarly to how a path can be generated from a location model and a context, a context can also be extracted from a path and a location model within the framework.

However the tools built on top of the framework never interact with a path in particular. It only gets paths dynamically from the translator based on the configuration per studio.

## Library
In addition to provide a framework, the package includeS standard custom modules that prove to be useful among multiple tools created for the Open VFX Toolkit.

## Installation And Configuration

Please read [INSTALL.md](./INSTALL.md) for more details.

## Examples

The [samples](./samples) folder contains a few Python scripts that demonstrate a simple usage of the Open VFX Framework.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **[Francois Duchesneau](https://github.com/trinix1975)**

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details
