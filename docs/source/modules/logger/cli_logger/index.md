# Cli logger

The Cli loger serves as the default logger for the pipeline. It is a small 
wrapper around [logging](https://docs.python.org/3/howto/logging.html) which 
is adds console and file output and scopes the output to each individual step.

## Usage
To create a new Cli Logger instance, simply provide two values. One with the 
minimal loglevel that should be logged, the second one is a boolean, 
indicating weather the logfile should be written, or you just want to log to 
the console.


```python
from src.logger.base_logger import LogLevel

from src.logger.loggers.cli_logger import CliLogger
from src.logger.adapters.cli_logger_adapter import CliLoggerAdapter

logger = CliLogger(LogLevel.ALL, write_logfile=True)
adapter = CliLoggerAdapter(LogLevel.ALL, write_logfile=True)
```   


## Further Info
```{toctree}
---
maxdepth: 3
---
cli_logger.rst
cli_logger_adapter
```