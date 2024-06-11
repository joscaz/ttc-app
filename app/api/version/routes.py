from flask import jsonify, request
from app import db
from app.api.version.controller import (getVersions, getCurrentVersion, getVersionById,
                                        createVersion)
from app.controller import (api, RequestException, validate_schema_data)
from app.api.version.schema import VersionSchema

@api.route('/versions', methods=['GET'])
def get_versions():
    count, versions = getVersions()
    return jsonify({"Número de versiones": count, "version": versions})

@api.route('/versions/current', methods=['GET'])
def get_current_version():
    version = getCurrentVersion()
    if version:
        return jsonify({"version_actual": version})
    else:
        raise RequestException(message="No current version found", code=404)

@api.route('/versions/<int:id>', methods=['GET'])
def get_version_by_id(id):
    version = getVersionById(id)
    if version:
        return jsonify({"version": version})
    else:
        raise RequestException(message="Version not found", code=404)
    
@api.route('/versions/', methods=['POST'])
def create_version():
    schema = VersionSchema(many=False, partial=True)
    loaded_data = validate_schema_data(schema, request.get_json())
    version = createVersion(loaded_data)
    schema = VersionSchema(many=False, relationships=[])
    result = schema.dump(version)

    return jsonify({"version": result})