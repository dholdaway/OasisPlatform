import os
import subprocess
import tarfile
from unittest import TestCase
from contextlib import contextmanager

from backports.tempfile import TemporaryDirectory
from celery.exceptions import Retry
from hypothesis import given
from hypothesis import settings as hypothesis_settings
from hypothesis.strategies import text, integers
from mock import patch, Mock, ANY
from pathlib2 import Path

from src.conf.iniconf import SettingsPatcher, settings
from src.model_execution_worker.storage_manager import MissingInputsException
from src.model_execution_worker.tasks import InvalidInputsException, get_oasislmf_config_path


#from oasislmf.utils.status import OASIS_TASK_STATUS
OASIS_TASK_STATUS = {
    'pending': {'id': 'PENDING', 'desc': 'Pending'},
    'running': {'id': 'RUNNING', 'desc': 'Running'},
    'success': {'id': 'SUCCESS', 'desc': 'Success'},
    'failure': {'id': 'FAILURE', 'desc': 'Failure'}
}

# Override default deadline for all tests to 8s
hypothesis_settings.register_profile("ci", deadline=800.0)
hypothesis_settings.load_profile("ci")

## Stub - tests need added 
