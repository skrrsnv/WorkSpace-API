import pytest
from apps.tasks.models import Task
from apps.projects.models import Membership
from apps.activity_logs.models import ActivityLog


@pytest.mark.django_db
def test_activity_log_created(client, owner, member):

    client.force_authenticate(user=owner)

    project = client.post("/api/v1/projects/", {
        "title": "Project",
        "description": "Test"
    }).data

    project_id = project["id"]

    Membership.objects.create(
        project_id=project_id,
        user=member,
        role=Membership.RoleChoices.member
    )

    client.force_authenticate(user=member)

    logs_before = ActivityLog.objects.count()

    client.post(
        f"/api/v1/projects/{project_id}/tasks/",
        {
            "title": "Task",
            "description": "Task desc",
            "priority": "low",
            "status": "todo"
        }
    )

    logs_after = ActivityLog.objects.count()

    assert logs_after == logs_before + 1