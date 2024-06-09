import pytest
from app import db
from app.api.version.model import Version
from app.api.version.schema import VersionSchema

def test_version_schema_load(client):
    version_data = {
        'id_version': 1,
        'numero_version': '1.0',
        'github_url': 'github.com/joscaz/ttc_app.git'
    }

    schema = VersionSchema()
    version = schema.load(version_data)
    assert version.id_version == version_data['id_version']
    assert version.numero_version == version_data['numero_version']
    assert version.github_url == version_data['github_url']

def test_version_schema_dump(client):
    version = version(
        id_version=1,
        numero_version='1.0',
        github_url='github.com/joscaz/ttc_app.git'
    )

    db.session.add(version)
    db.session.commit()

    schema = VersionSchema()
    version_dict = schema.dump(version)

    assert version_dict['id_version'] == version.id_version
    assert version_dict['numero_version'] == version.numero_version
    assert version_dict['github_url'] == version.github_url