# FUNCTION return_vocab
def return_vocab(uri):
    if uri in g.VOCABS.keys():
        # get vocab details using appropriate source handler
        vocab = getattr(source, g.VOCABS[uri].source) \
            (uri, request, language=request.values.get("lang")).get_vocabulary()
        return FairVocabularyRenderer(request, vocab).render()
    else:
        return None
# END FUNCTION return_vocab

