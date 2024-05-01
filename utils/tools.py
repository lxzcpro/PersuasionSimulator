from bson import json_util
import json

def jsonify(obj):
    """
    Convert MongoDB object to JSON
    """
    return json.loads(json_util.dumps(obj))
