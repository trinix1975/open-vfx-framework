# Contributing

Thank you for your interest in the Open VFX Framework. We hope to make everybody's life easier in the VFX community.

If you have questions about this project, please reach to [Francois Duchesneau]

## Studios Involvement
The tools development can be done free of charge by volunteers but we encourage businesses to use their staff or hire freelancers to add features to the toolkit and make it available to the public.

Studios can gain from this partnership by using a pipeline that can now be easily maintained and updated by anyone who is familiar with the Open VFX Toolkit.

## DCC Software Involvement
Digital content creation software companies can also use the framework to create their own features and ship it with their commercial products. For example a 3D software could include an asset loader or a publisher.

## Add/Update Features & Bugs

If you'd like to add/update a feature or fix a bug, please [fork the OpenVFX](https://docs.github.com/en/get-started/quickstart/fork-a-repo) and [create a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).

## Coding Convention

### Functions, variables etc

Functions, methods, variables, modules and packages use [snake case](https://en.wikipedia.org/wiki/Snake_case)

    Eg. my_function

### Class and Exceptions
Classes and exceptions use the [pascal case (upper camel case)](https://en.wikipedia.org/wiki/Camel_case).

    Eg. MyClass

### Prefer methods over properties
We recommend to use methods as much as possible over properties. The method name should not be prefixed by get_ when retrieving data. However it should be prefixed by set_ when setting the data.

```
For example:

my_object.tag()
my_object.set_tag()
```

The advantage is that users of the framework will be able to anticipate the format no matter what.

### Yaml over json
Use yaml over json as much as possible for consistency.

## Design and development process

### Build in layers
Always first develop tools so they can be used as Python code first when possible. Ideally use classes to organize the code but at a minimum individual functions should be placed in modules and packages.

Then build GUI on top of that Python code. Different studios may need to have their own interface for consistency sake and it's better if they can at least all use the common Python code.




