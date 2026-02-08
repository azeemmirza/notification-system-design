# Notification System Design

A comprehensive exploration of building scalable notification systems with design patterns, SOLID principles, and clean architecture in Python.

This project demonstrates a **flexible, extensible notification system** using core software engineering principles.

This repo contains the implementation referenced in my blog post **[Composition over Inheritance: A Notification System Design](https://azeemmirza.co/blog/composition-over-inheritance-a-notification-system-case-study)** and serves as the accompanying code sample.


## Table of Contents
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [License](#license)


## Architecture

```text
NotificationService
    ├── Router (resolve channel + provider)
    ├── PolicyPipeline (chain-of-responsibility)
    └── Dispatcher (execute delivery)
```

## Quick Start

### Clone the Repository
```bash
git clone <repository-url>
cd notification-system-design
```

### Run All Tests
```bash
python -m unittest discover tests -v
```


## Test Summary

### Overview
- **Total Test Cases:** 37
- **Test Classes:** 6
- **All Tests:** PASSING

### Test Breakdown
- TestNotificationService: 20 tests
- TestDefaultRouter: 5 tests
- TestPolicies: 7 tests
- TestChannels: 3 tests
- TestPolicyPipeline: 4 tests


## Project Features

- **Multiple Channels** - Email, SMS, Push notifications
- **Policy System** - Composable validation, scheduling, retry policies
- **Clean Architecture** - Clear separation of concerns
- **SOLID Principles** - Well-designed, maintainable code
- **Type Hints** - 100% type annotation coverage
- **Comprehensive Tests** - 37 unit tests
- **Zero Dependencies** - Pure Python standard library

## License

MIT License - See LICENSE file for details
