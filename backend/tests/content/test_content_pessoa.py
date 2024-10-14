from AccessControl import Unauthorized
from plone import api
from plone.dexterity.fti import DexterityFTI
from trepr.intranet.content.pessoa import Pessoa
from zope.component import createObject

import pytest


CONTENT_TYPE = "Pessoa"


@pytest.fixture
def pessoa_payload() -> dict:
    """Return a payload to create a new pessoa."""
    return {
        "type": "Pessoa",
        "id": "1234",
        "title": "None da silva",
        "description": ("Servidor do TRE-PR"),
        "email": "none@tre-pr.jus.br",
        "telefone": "4132101234",
    }


@pytest.fixture()
def content(portal, payload) -> Pessoa:
    with api.env.adopt_roles(["Manager"]):
        content = api.content.create(container=portal, **payload)
    return content


class TestPessoa:
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
        assert isinstance(obj, Pessoa)

    @pytest.mark.parametrize(
        "behavior",
        [
            "plone.basic",
            "plone.namefromtitle",
            "plone.shortname",
            "plone.leadimage",
            "plone.excludefromnavigation",
            "plone.versioning",
            "trepr.intranet.behavior.contato",
            "trepr.intranet.behavior.endereco",
            "plone.constraintypes",
        ],
    )
    def test_has_behavior(self, get_behaviors, behavior):
        assert behavior in get_behaviors(CONTENT_TYPE)

    @pytest.mark.parametrize(
        "role",
        [
            "Manager",
            "Site Administrator",
            "Editor",
            "Contributor",
        ],
    )
    def test_can_create(self, pessoa_payload, role):
        with api.env.adopt_roles(role):
            content = api.content.create(container=self.portal, **pessoa_payload)
        assert content.portal_type == CONTENT_TYPE
        assert isinstance(content, Pessoa)

    @pytest.mark.parametrize(
        "role",
        [
            "Reviewer",
            "Reader",
        ],
    )
    def test_cant_create(self, pessoa_payload, role):
        with pytest.raises(Unauthorized):
            with api.env.adopt_roles(role):
                api.content.create(container=self.portal, **pessoa_payload)
