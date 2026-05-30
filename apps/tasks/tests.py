import pytest
from apps.tasks.models import Task
from apps.projects.models import Membership, Project


@pytest.mark.django_db
def test_member_can_create_task(client, owner, member):

    client.force_authenticate(user=owner)

    response = client.post("/api/v1/projects/", {
        "title": "Project",
        "description": "Test"
    })

    project_id = response.data["id"]

    Membership.objects.create(
        project_id=project_id,
        user=member,
        role=Membership.RoleChoices.member
    )

    client.force_authenticate(user=member)

    response = client.post(
        f"/api/v1/projects/{project_id}/tasks/",
        {
            "title": "Task 1",
            "description": "Task desc",
            "priority": "medium",
            "status": "todo"
        }
    )

    assert response.status_code == 201
    assert Task.objects.count() == 1
    

@pytest.mark.django_db
def test_admin_can_update_task(client, owner, admin):

    client.force_authenticate(user=owner)

    project = client.post("/api/v1/projects/", {
        "title": "Project",
        "description": "Test"
    }).data

    project_id = project["id"]

    Membership.objects.create(
        project_id=project_id,
        user=admin,
        role=Membership.RoleChoices.admin
    )

    task = Task.objects.create(
        title="Old",
        description="Old desc",
        project_id=project_id
    )

    client.force_authenticate(user=admin)

    response = client.patch(
        f"/api/v1/projects/{project_id}/tasks/{task.id}/",
        {"title": "Updated"}
    )

    assert response.status_code == 200
    assert response.data["title"] == "Updated"
    
    
@pytest.mark.django_db
def test_owner_can_delete_task(client, owner):

    client.force_authenticate(user=owner)

    project = client.post("/api/v1/projects/", {
        "title": "Project",
        "description": "Test"
    }).data

    project_id = project["id"]

    task = Task.objects.create(
        title="Task",
        description="Test",
        project_id=project_id
    )

    response = client.delete(
        f"/api/v1/projects/{project_id}/tasks/{task.id}/"
    )

    assert response.status_code == 204
    assert Task.objects.count() == 0