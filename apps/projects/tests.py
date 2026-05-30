import pytest
from apps.projects.models import Project


@pytest.mark.django_db
def test_unauthorized_cannot_get_projects(client):
    response = client.get("/api/v1/projects/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_can_create_project(client, owner):
    client.force_authenticate(user=owner)

    response = client.post("/api/v1/projects/", {
        "title": "Project 1",
        "description": "Test project"
    })

    assert response.status_code == 201
    assert Project.objects.count() == 1
    

import pytest
from apps.projects.models import Project, Membership


@pytest.mark.django_db
def test_member_cannot_change_role(client, owner, member):

    client.force_authenticate(user=owner)

    response = client.post("/api/v1/projects/", {
        "title": "Project",
        "description": "Test"
    })

    project_id = response.data["id"]

    membership = Membership.objects.get(project_id=project_id, user=owner)

    Membership.objects.create(
        project_id=project_id,
        user=member,
        role=Membership.RoleChoices.member
    )

    client.force_authenticate(user=member)

    response = client.patch(
        f"/api/v1/projects/{project_id}/membership/{membership.id}/",
        {"role": "admin"}
    )

    assert response.status_code == 403