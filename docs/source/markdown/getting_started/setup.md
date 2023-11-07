# Setup

## 1. Clone this repository

```bash
git clone https://gitlab.renkulab.io/expectmine/processing-pipeline
cd processing-pipeline
```

## 2. Setup environment

::::{tab-set}

:::{tab-item} Windows
:sync: key1

```{note}
As this step relies on Make, you either have to install [Make for Windows](https://gnuwin32.sourceforge.net/packages/make.htm)
or do this step manually by running `pip install --upgrade -r requirements.txt`
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
```
:::

:::{tab-item} Linux
:sync: key3

```bash
python -m venv env
source env/bin/activate
make deps
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
