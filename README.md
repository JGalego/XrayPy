# XrayPy [![Build Status][travis-image]][travis-url]

## Overview

> Wrapper for <a href="https://marketplace.atlassian.com/plugins/com.xpandit.plugins.xray/server/overview">Xray</a>&#39;s REST API

<img src="https://github.com/JGalego/XrayPy/blob/master/images/Xray.jpeg?raw=true" width="200"/>

## Installation

```sh
$ python setup.py install
```

## Supported Actions

* Get Project Info (/rest/api/2/project)
* Get Issue Info (/rest/api/2/issue)
* Get Test Run Info (rest/raven/1.0/api/testrun)
* Create Xray Issues (/rest/api/2/issue)
    * Test
    * Test Set
    * Test Plan
    * Test Execution
* Save Test Run (/rest/raven/1.0/import/execution)
* Add Evidence to Test Run (/rest/raven/1.0/api/testrun/<TEST_RUN_ID>/attachment)
* Import Test Results to JIRA
    * JSON Format (/rest/raven/1.0/import/execution)
    * JUnit XML (/rest/raven/1.0/import/execution/junit)
* Export test results from JIRA (/rest/raven/1.0/testruns)
* Run JQL queries (/rest/api/2/search)

## References

* <a href="https://confluence.xpand-addons.com/display/XRAY/REST+API">Xray's REST API</a>
* <a href="https://developer.atlassian.com/server/jira/platform/rest-apis/">JIRA's REST API</a>

## License

MIT License © [João Galego]()

[travis-image]: https://travis-ci.org/JGalego/XrayPy.svg?branch=master
[travis-url]: https://travis-ci.org/JGalego/XrayPy