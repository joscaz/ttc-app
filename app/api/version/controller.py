from app import db
from app.api.version.model import Version
from app.api.version.schema import VersionSchema

def createVersion(data):
  version = Version(**data)    
  db.session.add(version)
  db.session.commit()
  return version

def getVersions():
    versions = Version.query.all()
    version_schema = VersionSchema(many=True)
    all_versions = version_schema.dump(versions)
    count = Version.query.count()
    return count, all_versions

def getCurrentVersion():
    version = Version.query.order_by(Version.created_at.desc()).first() 
    version_schema = VersionSchema(many=False)
    return version_schema.dump(version) if version else None

def getVersionById(id):
    version = Version.query.get(id)
    version_schema = VersionSchema(many=False)
    return version_schema.dump(version) if version else None