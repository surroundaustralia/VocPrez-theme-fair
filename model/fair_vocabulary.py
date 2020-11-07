from vocprez import __version__
from pyldapi import Renderer
from flask import Response, render_template
from rdflib import Graph, URIRef, Literal, XSD, RDF
from rdflib.namespace import DCTERMS, OWL, SKOS, Namespace
from vocprez.model.profiles import profile_dcat, profile_dd, profile_skos, profile_fair
from vocprez.model.vocabulary import VocabularyRenderer


class FairVocabularyRenderer(VocabularyRenderer):
    def __init__(self, request, vocab, language="en"):
        self.profiles = {
            "dcat": profile_dcat,
            "skos": profile_skos,
            "dd": profile_dd,
            "fair": profile_fair,
        }
        self.vocab = vocab
        self.uri = self.vocab.uri
        self.language = language

        super(VocabularyRenderer, self).__init__(request, vocab.uri, self.profiles, "skos")

    def render(self):
        # try returning alt profile
        response = super().render()
        if response is not None:
            return response
        elif self.profile == "dcat":
            if self.mediatype in Renderer.RDF_SERIALIZER_TYPES_MAP:
                return self._render_dcat_rdf()
            else:
                return self._render_dcat_html()
        elif self.profile == "skos":
            if self.mediatype in Renderer.RDF_SERIALIZER_TYPES_MAP:
                return self._render_skos_rdf()
            else:
                return self._render_dcat_html()  # same as DCAT, for now
        elif self.profile == "dd":
            return self._render_dd_json()
        elif self.profile == "fair":
            if (
                    self.mediatype in Renderer.RDF_MEDIA_TYPES
                    or self.mediatype in Renderer.RDF_SERIALIZER_TYPES_MAP
            ):
                return self._render_fair_rdf()
            else:
                return self._render_fair_html()

    def _render_fair_rdf(self):
        # make a dummy graph
        g = Graph()
        g.bind("skos", SKOS)
        FAIR = Namespace("https://w3id.org/profile/fair")
        g.bind("fair", FAIR)
        v = URIRef(self.vocab.uri)
        g.add((
            v,
            RDF.type,
            SKOS.ConceptScheme
        ))
        g.add((
            v,
            SKOS.prefLabel,
            Literal(self.vocab.title)
        ))



        # serialise in other RDF format
        if self.mediatype in ["application/rdf+json", "application/json"]:
            graph_text = g.serialize(format="json-ld")
        else:
            graph_text = g.serialize(format=self.mediatype)

        return Response(
            graph_text,
            mimetype=self.mediatype,
            headers=self.headers,
        )

    def _render_fair_html(self):
        _template_context = {
            "version": __version__,
            "uri": self.uri,
            "vocab": self.vocab,
            "title": self.vocab.title,
        }

        return Response(
            render_template("vocabulary.html", **_template_context),
            headers=self.headers,
        )
