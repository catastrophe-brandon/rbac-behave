# Using Behave (Gherkin) to Test RBAC Service

The goal of this POC is to demonstrate how one would use Behave to take a BDD
approach to testing the API provided by the RBAC service. Existing tests take a 
primarily procedural approach to building testing automation. 

## Why??

Our current approach has the following drawbacks:
1. Typically by the time a feature is being tested/automated, it has already gone through the development pipeline and 
been chucked over the fence. By this time it is typically too late to consider the experience of the user. Any 
corrections made at this point are typically functional in nature and will not address the user experience of the API consumer.
2. When it comes to defining the capabilities of our APIs, this is often left to primarily technical users. While this 
may be adequate, it leaves us blind to the sometimes myopic view of the engineers that have been staring at the problem for far too long.

With a BDD approach, we may have the following benefits:

1. A "spec first" or "behavior first" approach to defining new functionality.
2. An easily-shared definition (the feature file) that can be reviewed by both technical and non-technical stakeholders.

## Shortcomings

Behave feels somewhat incomplete; it lacks polish around the edges when compared to other languages that support 
Gherkin, such as Java.

## Side Benefits

* Behave is supported in PyCharm Professional edition and partially supported in VSCode.