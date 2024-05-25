import plodlib
from typing import Union, Any, Annotated

from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, RedirectResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# if it turns out to be necessary add caching here. so far performance is fine without it.

@app.get("/")
def not_implemented():
    """Not implemented. Only a brief message is returned."""
    return """Nothing here. Try /id/pompeii or /id/pompeii.ttl , or maybe /geojson/pompeii . See /docs for documentation. One quick note: 
    In general, you can pass either simple ids ('pompeii') or urns ('urn:p-lod:id:pompeii') to the API."""

class CustomTTLResponse(Response):
    media_type = "text/turtle"
    def render(self, content: Any) -> bytes:
        return content

@app.get('/id/{p_lod_id}.ttl', response_class=CustomTTLResponse)
def get_ttl(p_lod_id: str):
    """Return an RDF representation of a P-LOD ID serialized as Turtle and with mimetype set to text/turtle."""
    rdf_data = plodlib.PLODResource(p_lod_id.replace('urn:p-lod:id:','')).rdf_describe()
    response = Response(content=rdf_data, media_type="text/turtle")
    return response


@app.get("/id/{p_lod_id}")
def information_about_an_id(p_lod_id: str, q: Union[str, None] = None, accept: Annotated[str | None, Header()] = None):
    """Return an array of dictionaries describing a P-LOD ID. The key of each dictionary is the predicate, and the value is the object.
    
    The format of the returned JSON is under development and may change.
    """   

    if accept == 'text/turtle':
        return RedirectResponse(url=f'/id/{p_lod_id}.ttl')

    r = plodlib.PLODResource(p_lod_id.replace('urn:p-lod:id:',''))

    return [{row.name:row['o']} for i,row in r._id_df.iterrows()]


@app.get("/as-object/{p_lod_id}")
def get_as_object(p_lod_id: str):
    """JSON array of uses of the P-LOD ID as an object in an RDF triple.

    The format of the returned JSON is under development and may change. A focus of current development is consistency across API calls.
    """

    return plodlib.PLODResource(p_lod_id.replace('urn:p-lod:id:','')).as_object()


@app.get("/as-predicate/{p_lod_id}")
def get_as_predicate(p_lod_id: str):
    """JSON array of uses of the P-LOD ID as a predicate in an RDF triple.

    The format of the returned JSON is under development and may change. A focus of current development is consistency across API calls.
    """

    return plodlib.PLODResource(p_lod_id.replace('urn:p-lod:id:','')).as_predicate()


@app.get("/conceptual-ancestors/{p_lod_id}")
def get_conceptual_ancestors(p_lod_id: str):
    """Return a json array of dictionaries that indicate the conceptual ancestors of a P-LOD ID.
    
    The format of the returned JSON is under development and may change. A focus of current development is consistency across API calls.
    """

    return plodlib.PLODResource(p_lod_id.replace('urn:p-lod:id:','')).conceptual_ancestors()


@app.get("/conceptual-children/{p_lod_id}")
def get_conceptual_children(p_lod_id: str):
    """Return a json array of dictionaries that indicate the direct conceptual children of a P-LOD ID. It does not include all descendants.
    
    The format of the returned JSON is under development and may change. A focus of current development is consistency across API calls.
    """

    return plodlib.PLODResource(p_lod_id.replace('urn:p-lod:id:','')).conceptual_children()

@app.get("/conceptual-descendants/{p_lod_id}")
def get_conceptual_descendants(p_lod_id: str):
    """Return a json array of dictionaries that indicate the conceptual descendants of a P-LOD ID.
    
    The format of the returned JSON is under development and may change. A focus of current development is consistency across API calls.
    """

    return plodlib.PLODResource(p_lod_id.replace('urn:p-lod:id:','')).conceptual_descendants()

@app.get("/depicted-where/{p_lod_id}")
def id_is_depicted_where(p_lod_id: str, level_of_detail: str = 'feature'):
    """Return json arrays that list the spatial units where a concept (or other?) is depicted.
    
    Examples: /depicted_where/ariadne , /depicted_where/urn:p-lod:id:ariadne
    
    The format of the returned JSON is under development and may change. A focus of current development is consistency across API calls."""

    return plodlib.PLODResource(p_lod_id.replace('urn:p-lod:id:','')).depicted_where(level_of_detail=level_of_detail)

@app.get('/depicts-concepts/{p_lod_id}')
def id_depicts_concepts(p_lod_id: str):
    """Return json arrays that list the concepts depicted by artwork in a spatial unit.
    
    The format of the returned JSON is under development and may change. A focus of current development is consistency across API calls."""

    return plodlib.PLODResource(p_lod_id.replace('urn:p-lod:id:','')).depicts_concepts()

@app.get('/images/{p_lod_id}')
def gather_images(p_lod_id: str):
    """Returns an array of json dictionaries, each of which describes an image relevant to the P-LOD identifier. This is meant as a general purpose tool to gather many images.
    
    The format of the returned JSON is under development and may change. A focus of current development is consistency across API calls.
    
    Each dictionary has a urn key that identifies the image."""

    return plodlib.PLODResource(p_lod_id.replace('urn:p-lod:id:','')).gather_images()

@app.get('/geojson/{p_lod_id}')
def get_geojson(p_lod_id):
  """Return a GeoJSON representation of a P-LOD ID.
  
  It should be possible to use the GeoJSON directly."""

  return plodlib.PLODResource(p_lod_id.replace('urn:p-lod:id:','')).geojson

@app.get('/instances-of/{p_lod_id}')
def get_instances_of(p_lod_id):
  """Return a json array of dictionaries that indicate the instances of a P-LOD ID.
  
  The format of the returned JSON is under development and may change. A focus of current development is consistency across API calls.
  """

  return plodlib.PLODResource(p_lod_id.replace('urn:p-lod:id:','')).instances_of()


@app.get('/see-also/{p_lod_id}.ttl', response_class=CustomTTLResponse)
def get_see_also_ttl(p_lod_id):
  """Return an RDF representation of the seeAlso links for a P-LOD ID serialized as Turtle and with mimetype set to text/turtle.
  
  The triples are rendered with rdfs:seeAlso as the predicate and the original triple with P-LOD predicate is also returned."""
  rdf_data = plodlib.PLODResource(p_lod_id.replace('urn:p-lod:id:','')).see_also()
  response = Response(content=rdf_data, media_type="text/turtle")
  return response


@app.get('/spatial-ancestors/{p_lod_id}')
def get_spatial_ancestors(p_lod_id):
  """Return a json array of dictionaries that indicate the spatial ancestors of a P-LOD ID.
  
  The format of the returned JSON is under development and may change. A focus of current development is consistency across API calls.
  
  Each dictionary currently has a urn, label, type, and geojson key.

  For the time being, the first element in the array is the P-LOD ID itself. The last element is Pompeii. Including both everytime is inefficient and this may change.
  """

  return plodlib.PLODResource(p_lod_id.replace('urn:p-lod:id:','')).spatial_ancestors()

@app.get('/spatial-children/{p_lod_id}')
def get_spatial_children(p_lod_id, rdf_type: str = 'all', exclude_rdf_type: str = ''):
  """Return a json array of dictionaries that indicate the direct spatial children of a P-LOD ID. It does not include all descendants.
  
  The format of the returned JSON is under development and may change. A focus of current development is consistency across API calls.
  
  
  For the time being, the first element in the array is the P-LOD ID itself. The last element is Pompeii. Including both every time is inefficient and this may change.
  """

  return plodlib.PLODResource(p_lod_id.replace('urn:p-lod:id:','')).spatial_children(rdf_type=rdf_type, exclude_rdf_type=exclude_rdf_type)