from trepr.intranet import PACKAGE_NAME
from zope.schema.vocabulary import SimpleVocabulary

import pytest


class TestVocabEstados:
    name = f"{PACKAGE_NAME}.vocabulary.estados"

    @pytest.fixture(autouse=True)
    def _vocab(self, get_vocabulary, portal):
        self.vocab = get_vocabulary(self.name, portal)

    def test_vocabulary(self):
        assert self.vocab is not None
        assert isinstance(self.vocab, SimpleVocabulary)

    @pytest.mark.parametrize(
        "token,title",
        [
            ["AC", "Acre"],
            ["AL", "Alagoas"],
            ["AP", "Amapá"],
            ["AM", "Amazonas"],
            ["BA", "Bahia"],
            ["CE", "Ceará"],
            ["DF", "Distrito Federal"],
            ["ES", "Espírito Santo"],
            ["GO", "Goiás"],
            ["MA", "Maranhão"],
            ["MT", "Mato Grosso"],
            ["MS", "Mato Grosso do Sul"],
            ["MG", "Minas Gerais"],
            ["PA", "Pará"],
            ["PB", "Paraíba"],
            ["PR", "Paraná"],
            ["PE", "Pernambuco"],
            ["PI", "Piauí"],
            ["RJ", "Rio de Janeiro"],
            ["RN", "Rio Grande do Norte"],
            ["RS", "Rio Grande do Sul"],
            ["RO", "Rondônia"],
            ["RR", "Roraima"],
            ["SC", "Santa Catarina"],
            ["SP", "São Paulo"],
            ["SE", "Sergipe"],
            ["TO", "Tocantins"],
        ],
    )
    def test_token(self, token, title):
        assert token in [x for x in self.vocab.by_token]
        assert title == self.vocab.getTermByToken(token).title
