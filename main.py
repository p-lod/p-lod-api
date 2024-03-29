import plodlib
from typing import Union

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return "Nothing here. Try /id/pompeii ."

@app.get("/id/{p_lod_id}")
def read_id(p_lod_id: str, q: Union[str, None] = None):
    """Return an array of dictionaries describing a P-LOD ID. The key of each dictionary is the predicate, and the value is the object.
    
    The format of the returned JSON is under development and may change.
    """
    
    r = plodlib.PLODResource(p_lod_id.replace('urn:p-lod:id:',''))

    return [{row.name:row['o']} for i,row in r._id_df.iterrows()]

@app.get("/depicted_where/{p_lod_id}")
def read_depicted_where(p_lod_id: str):
    """Return json arrays that list the spaital units where a concept (or other?) is depicted.
    
    Examples: /depicted_where/ariadne , /depicted_where/urn:p-lod:id:ariadne
    
    The format of the returned JSON is under development and may change. A focus of current development is consistency across API calls."""

    return plodlib.PLODResource(p_lod_id.replace('urn:p-lod:id:','')).depicted_where()

@app.get('/depicts_concepts/{p_lod_id}')
def read_depicts_concepts(p_lod_id: str):
    """Return json arrays that list the concepts depicted by artwork in a spatial unit.
    
    The format of the returned JSON is under development and may change. A focus of current development is consistency across API calls."""

    return plodlib.PLODResource(p_lod_id.replace('urn:p-lod:id:','')).depicts_concepts()



@app.get('/geojson/{p_lod_id}')
def read_geojson(p_lod_id):
  """Return a GeoJSON representation of a P-LOD ID.
  
  It should be possible to use the GeoJSON directly."""

  return plodlib.PLODResource(p_lod_id.replace('urn:p-lod:id:','')).geojson

