# Setup

## 1. Clone this repository
```{warning}
This project uses type-unions introduced in python 3.10. Make sure you are using at least python
version 3.10. This can be done by running `python --version`
```

```bash
git clone https://gitlab.renkulab.io/expectmine/processing-pipeline
cd processing-pipeline
```

## 2. Setup environment

::::{tab-set}

:::{tab-item} Windows
:sync: key1

```{note}
As this step relies on Make, which is only available as default through linux-based systems. To still use
the following guide either install make through [choco](https://chocolatey.org/install) or use the
linux sub system and follow the linux guide.
```

```bat
python -m venv env
.\env\Scripts\activate
make deps
make env-vars
```
:::

:::{tab-item} macOS
:sync: key2

```bash
python -m venv env
source env/bin/activate
make deps
make env-vars
```
:::

:::{tab-item} Linux
:sync: key3

```bash
python -m venv env
source env/bin/activate
make deps
make env-vars
```
:::

::::

## 3. Install required libraries

```{note}
You only need to install the libraries which are used by the steps you are 
using.
```
You can go to the [steps](../concepts/steps) section to see which libraries 
are required by the steps you want to use.
