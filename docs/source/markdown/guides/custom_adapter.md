# How to write a custom adapter
Adapters are used by the pipeline to make interfaces more modular, currently 
there are three types of adapters which are used:

## IO-Adapter
The IO-Adapter is concerned with getting user input to the pipeline and the 
individual step. It creates a uniform input interface.

To create a custom adapter, you need to create two classes, one which 
extends `BaseIo` and one which extends `BaseIoAdapter`.

The purpose of `BaseIo` is to create a uniform input interface, while 
`BaseIoAdapter` is concerned with creating scoped instances of `BaseIo`.

## Logging-Adapter
The Logger-Adapter is focused on capturing and managing logs within the
pipeline and its individual steps. It establishes a standardized logging
interface.

To develop a custom logger adapter, you must design two classes: one that
extends `BaseLogger` and another that extends `BaseLoggerAdapter`.

The primary role of `BaseLogger` is to define a uniform logging interface,
while `BaseLoggerAdapter` is responsible for generating scoped instances of 
`BaseLogger`.

## Storage-Adapter
The Storage-Adapter manages everything that has to do with storing temporary 
files, storing long term config or storing previous pipelines for executing 
again.

Similarly to the Logger and Io adapters, you need to create a class 
extending `BaseStore` and one extending `BaseStoreAdapter`.

`BaseStore` is creating the necessary interface to store files in a 
step-based scoped manner while `BaseStoreAdapter` is the factory for 
creating such scoped stores.