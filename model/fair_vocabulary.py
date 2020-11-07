from vocprez import __version__
from pyldapi import Renderer
from flask import Response, render_template
from rdflib import Graph, URIRef, Literal, Namespace, BNode
from rdflib.namespace import DCTERMS, SKOS, XSD, RDF, RDFS, PROV
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
        def _make_fair_score(uri, label, f_score, a_score, i_score, r_score):
            # graph setup
            g = Graph()
            g.bind("skos", SKOS)
            FAIR = Namespace("https://w3id.org/profile/fair")
            g.bind("fair", FAIR)
            QUDT = Namespace("http://qudt.org/schema/qudt/")
            g.bind("qudt", QUDT)
            UNIT = Namespace("http://qudt.org/vocab/unit/")
            g.bind("unit", UNIT)

            g.bind("dcterms", DCTERMS)

            # boilerplate
            fair_score = BNode()
            g.add((fair_score, RDF.type, QUDT.Quantity))

            score_f = BNode()
            g.add((fair_score, DCTERMS.hasPart, score_f))
            g.add((score_f, RDF.type, QUDT.QuantityKind))
            g.add((score_f, RDF.type, FAIR.PrincipleScore))
            g.add((score_f, RDFS.label, Literal("Findable Score")))
            g.add((score_f,
                   RDFS.comment,
                   Literal("Metadata and data should be easy to find for both humans and computers")))
            score_a = BNode()
            g.add((fair_score, DCTERMS.hasPart, score_a))
            g.add((score_a, RDF.type, QUDT.QuantityKind))
            g.add((score_a, RDF.type, FAIR.PrincipleScore))
            g.add((score_a, RDFS.label, Literal("Accessable Score")))
            g.add((score_a,
                   RDFS.comment,
                   Literal("Once someone finds the required data, they need to know how the data can be accessed")))
            score_i = BNode()
            g.add((fair_score, DCTERMS.hasPart, score_i))
            g.add((score_i, RDF.type, QUDT.QuantityKind))
            g.add((score_i, RDF.type, FAIR.PrincipleScore))
            g.add((score_i, RDFS.label, Literal("Interoperable Score")))
            g.add((score_i,
                   RDFS.comment,
                   Literal(
                       "The data needs to be easily integrated with other data for analysis, storage, and processing.")
                   ))
            score_r = BNode()
            g.add((fair_score, DCTERMS.hasPart, score_r))
            g.add((score_r, RDF.type, QUDT.QuantityKind))
            g.add((score_r, RDF.type, FAIR.PrincipleScore))
            g.add((score_r, RDFS.label, Literal("Reusable Score")))
            g.add((score_r,
                   RDFS.comment,
                   Literal(
                       "Data should be well-described so they can be reused and replicated in different settings.")))

            quant_f = BNode()
            g.add((score_f, QUDT.hasQuantity, quant_f))
            g.add((quant_f, RDF.type, QUDT.QuantityValue))
            g.add((quant_f, QUDT.unit, UNIT.PERCENT))

            quant_a = BNode()
            g.add((score_a, QUDT.hasQuantity, quant_a))
            g.add((quant_a, RDF.type, QUDT.QuantityValue))
            g.add((quant_a, QUDT.unit, UNIT.PERCENT))

            quant_i = BNode()
            g.add((score_i, QUDT.hasQuantity, quant_i))
            g.add((quant_i, RDF.type, QUDT.QuantityValue))
            g.add((quant_i, QUDT.unit, UNIT.PERCENT))

            quant_r = BNode()
            g.add((score_r, QUDT.hasQuantity, quant_r))
            g.add((quant_r, RDF.type, QUDT.QuantityValue))
            g.add((quant_r, QUDT.unit, UNIT.PERCENT))

            # instance values
            v = URIRef(uri)
            g.add((v, RDFS.label, Literal(label)))
            g.add((v, FAIR.hasFairScore, fair_score))

            g.add((quant_f, QUDT.value, Literal(f_score, datatype=XSD.float)))
            g.add((quant_a, QUDT.value, Literal(a_score, datatype=XSD.float)))
            g.add((quant_i, QUDT.value, Literal(i_score, datatype=XSD.float)))
            g.add((quant_r, QUDT.value, Literal(r_score, datatype=XSD.float)))

            return g, fair_score

        g, f = _make_fair_score(self.vocab.uri, self.vocab.title, "83.5", "78.3", "55.0", "60")

        # FAIR Score method
        g.bind("prov", PROV)
        method = URIRef("https://w3id.org/profile/fair/method/DCAT2")
        g.add((method, RDF.type, PROV.Plan))
        g.add((method, RDFS.label, Literal("DCAT2 FAIR Calculation")))
        LOCI = Namespace("https://linked.data.gov.au/def/loci#")
        g.bind("loci", LOCI)
        g.add((f, LOCI.hadGenerationMethod, method))

        # derived from
        g.add((f, PROV.wasDerivedFrom, URIRef(self.vocab.uri + "?_profile=dcat")))


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
