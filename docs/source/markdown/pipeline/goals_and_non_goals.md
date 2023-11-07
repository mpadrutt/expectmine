# Goals & Non-Goals

This processing pipeline was developed as a bachelor thesis. During the 
thesis a set of goals and non-goals was defined. The intention of these 
goals is to provide the best user experience, while still keeping the scope 
of the project manageable.

## Goals
### Leverage core tools
No new tool should be developed to solve a problem other tools like [MZmine3](http://mzmine.github.io)
or [Sirius](https://boecker-lab.github.io/docs.sirius.github.io/) are not 
already solving. Rather a new pipeline should be developed which leverages the
existing solutions and makes them more accessible to users.

### No tool version requirement
During the process of developing, it became apparent that managing the 
interface between multiple major versions of tools is impossible. As a 
result most of the steps have a vague dependency on a major version of a 
library, but apart from that, the only interface is the structure of output 
files such as `.mzml`, `.mgf`or `.tsv` which are less susceptible to 
interface changes.

### Transparency
Make it very clear to the user what exactly is happening while the pipeline 
is running. Make Logging and collecting useful Metadata for the user a core 
feature.

### Future-proofing
Build the system in a way that no major library interface update can break 
the entire system. Similarly, the system is built in a way which makes it 
easy to integrate into other tools later.

## Non-Goals
### Complete library integration
The system is built to quickly create a step using a specific functionality 
which is needed from a library. But it is not intended to integrate all 
functions of processing libraries from the beginning.
