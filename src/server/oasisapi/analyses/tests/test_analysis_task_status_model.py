from unittest.mock import patch

from hypothesis import given
from hypothesis import settings as hypothesis_settings
from hypothesis._strategies import sampled_from
from hypothesis.extra.django import TestCase

from src.server.oasisapi.analyses.models import AnalysisTaskStatus
from src.server.oasisapi.analyses.tests.fakes import fake_analysis_task_status, fake_analysis
from src.server.oasisapi.queues.consumers import TaskStatusMessageAnalysisItem, TaskStatusMessageItem
from src.server.oasisapi.queues.utils import filter_queues_info

# Override default deadline for all tests to 8s
hypothesis_settings.register_profile("ci", deadline=3000.0)
hypothesis_settings.load_profile("ci")


class WebsocketTriggers(TestCase):
    def test_status_is_queued___message_isnt_sent(self):
        with patch('src.server.oasisapi.analyses.signal_receivers.send_task_status_message') as send_mock:
            fake_analysis_task_status()

            send_mock.assert_not_called()

    @given(status=sampled_from([
        AnalysisTaskStatus.status_choices.STARTED,
        AnalysisTaskStatus.status_choices.ERROR,
        AnalysisTaskStatus.status_choices.CANCELLED,
        AnalysisTaskStatus.status_choices.COMPLETED,
    ]))
    def test_status_is_not_queued___message_is_sent(self, status):
        with patch('src.server.oasisapi.analyses.signal_receivers.send_task_status_message') as send_mock:
            instance = fake_analysis_task_status(status=status, queue_name='celery')

            send_mock.assert_called_once_with([TaskStatusMessageItem(
                queue=filter_queues_info(['celery'])[0],
                analyses=[TaskStatusMessageAnalysisItem(
                    analysis=instance.analysis,
                    updated_tasks=[instance],
                )],
            )])


    # Needs fixing 

#    def test_tasks_statuses_are_created_with_create_statues___message_is_sent(self):
#        with patch('src.server.oasisapi.analyses.models.send_task_status_message') as send_mock:
#            analysis = fake_analysis()
#
#            AnalysisTaskStatus.objects.create_statuses(analysis, ['foo', 'bar'], 'celery')
#
#            send_mock.assert_called_once_with([TaskStatusMessageItem(
#                queue=filter_queues_info(['celery'])[0],
#                analyses=[TaskStatusMessageAnalysisItem(
#                    analysis=analysis,
#                    updated_tasks=list(analysis.sub_task_statuses.all()),
#                )],
#            )])
