[![CI](https://github.com/Relm-Arrowny/p99Bluesky/actions/workflows/ci.yml/badge.svg)](https://github.com/Relm-Arrowny/p99Bluesky/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/Relm-Arrowny/p99Bluesky/branch/main/graph/badge.svg)](https://codecov.io/gh/Relm-Arrowny/p99Bluesky)
[![PyPI](https://img.shields.io/pypi/v/p99Bluesky.svg)](https://pypi.org/project/p99Bluesky)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# P99Bluesky

This module provides a complete offline environment for beamline p99. It includes everything you need to get started, such as Bluesky plans for defining experiments, Ophyd-asynio for controlling hardware devices, and Blueapi for interacting with Bluesky programmatically. Additionally, it comes bundled with all the necessary modules to run p99 within an IPython terminal.


Source          | <https://github.com/Relm-Arrowny/p99Bluesky>
:---:           | :---:
PyPI            | `pip install p99Bluesky`
Documentation   | <https://relm-arrowny.github.io/p99Bluesky>
Releases        | <https://github.com/Relm-Arrowny/p99Bluesky/releases>

This repository can also serve as a configuration source for a p99 instance of BlueAPI. It offers both planFunctions and deviceFunctions, streamlining the setup process.

``` yaml
    env:
      sources:
        - kind: planFunctions
          module: P99Bluesky.plans
        - kind: deviceFunctions
          module: p99Bluesky.beamlines.p99 
```

<!-- README only content. Anything below this line won't be included in index.md -->

See https://relm-arrowny.github.io/p99Bluesky for more detailed documentation.
