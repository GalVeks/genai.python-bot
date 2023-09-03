#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "d26c8e02-e02d-4901-9b00-435f84d6b4e2")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "yr68Q~8YsT_PYvADc3t.N4O7DFpqW-A~-xm7Vb-2")
