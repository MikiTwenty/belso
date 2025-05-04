# Belso: Better LLMs Structured Outputs

[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://MikiTwenty.github.io/belso/)
[![PyPI version](https://badge.fury.io/py/belso.svg)](https://badge.fury.io/py/belso)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

Belso (Better LLMs Structured Outputs) is a Python library designed to simplify working with structured outputs from Large Language Models (LLMs). It provides a unified interface for defining, validating, translating, and processing structured data across multiple LLM providers.

## Key Features

- **Unified Schema Interface**: define schemas once using Python classes and use them everywhere.
- **Multi-Provider Support**: seamlessly work with outputs from:
  - OpenAI
  - Anthropic
  - Google AI
  - Mistral AI
  - Hugging Face
  - Ollama
  - LangChain
- **Format Translation**: bi-directional conversion between provider formats.
- **Nested Structures**: support for complex nested fields and array types.
- **Validation & Visualization**: tools for validating and inspecting schemas.
- **Serialization**: export/import schemas to/from JSON, XML, and YAML formats.
- **Minimal Dependencies**: lightweight with fast runtime performance.

## Installation

```bash
pip install belso
```

## Quick Start

For a quick start, check out the [examples](examples/) directory.

## Documentation

For more details, please refer to the [official documentation](https://MikiTwenty.github.io/belso/).

## License

This project is licensed under the terms of the [MIT license](LICENSE).
