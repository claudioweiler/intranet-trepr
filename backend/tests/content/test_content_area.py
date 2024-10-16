from AccessControl import Unauthorized
from plone import api
from plone.dexterity.fti import DexterityFTI
from trepr.intranet.content.area import Area
from zope.component import createObject
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

import pytest


CONTENT_TYPE = "Area"


@pytest.fixture
def area_payload() -> dict:
    """Return a payload to create a new area."""
    return {
        "type": "Area",
        "id": "ti",
        "title": "Tecnologia da Informação",
        "description": ("Área responsável por TI"),
        "email": "ti@tre-pr.jus.br",
        "telefone": "(41) 3210.1234",
    }


class TestArea:
    @pytest.fixture(autouse=True)
    def _setup(self, get_fti, portal):
        self.fti = get_fti(CONTENT_TYPE)
        self.portal = portal

    def test_fti(self):
        assert isinstance(self.fti, DexterityFTI)

    def test_factory(self):
        factory = self.fti.factory
        obj = createObject(factory)
        assert obj is not None
        assert isinstance(obj, Area)

    @pytest.mark.parametrize(
        "behavior",
        [
            "plone.basic",
            "plone.namefromtitle",
            "plone.shortname",
            "plone.excludefromnavigation",
            "plone.versioning",
            "trepr.intranet.behavior.contato",
            "trepr.intranet.behavior.endereco",
            "volto.blocks",
            "plone.constraintypes",
            "volto.preview_image",
        ],
    )
    def test_has_behavior(self, get_behaviors, behavior):
        assert behavior in get_behaviors(CONTENT_TYPE)

    @pytest.mark.parametrize(
        "role",
        [
            "Manager",
            "Site Administrator",
        ],
    )
    def test_can_create(self, area_payload, role):
        with api.env.adopt_roles(role):
            content = api.content.create(container=self.portal, **area_payload)
        assert content.portal_type == CONTENT_TYPE
        assert isinstance(content, Area)

    @pytest.mark.parametrize(
        "role",
        [
            "Editor",
            "Reviewer",
            "Contributor",
            "Reader",
        ],
    )
    def test_cant_create(self, area_payload, role):
        with pytest.raises(Unauthorized):
            with api.env.adopt_roles(role):
                api.content.create(container=self.portal, **area_payload)

    def test_subscriber_added_with_description_value(self, area_payload):
        container = self.portal
        with api.env.adopt_roles(["Manager"]):
            area = api.content.create(
                container=container,
                **area_payload,
            )
        assert area.exclude_from_nav is False

    def test_subscriber_added_without_description_value(self, area_payload):
        from copy import deepcopy

        container = self.portal
        with api.env.adopt_roles(["Manager"]):
            payload = deepcopy(area_payload)
            payload["description"] = ""
            area = api.content.create(container=container, **payload)
        assert area.exclude_from_nav is True

    def test_subscriber_modified(self, area_payload):
        container = self.portal
        with api.env.adopt_roles(["Manager"]):
            area = api.content.create(container=container, **area_payload)
        assert area.exclude_from_nav is False
        # Altera a descricao
        area.description = ""
        # Dispara o evento de modificacao
        notify(ObjectModifiedEvent(area))
        # Agora o objeto desaparece da navegação
        assert area.exclude_from_nav is True
