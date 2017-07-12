import connexion
from esm.controllers import _version_ok
from esm.models.catalog import Catalog
from esm.models.empty import Empty
from esm.models.service_type import ServiceType
from esm.models.manifest import Manifest
# from datetime import date, datetime
# from typing import List, Dict
# from six import iteritems
# from ..util import deserialize_date, deserialize_datetime

from adapters.datasource import STORE as store


def catalog():
    """
    Gets services registered within the broker
    \&quot;The first endpoint that a broker must implement is the service catalog. The client will initially fetch
    this endpoint from all brokers and make adjustments to the user-facing service catalog stored in the a
    client database. \\n\&quot;

    :rtype: Catalog
    """
    # get all services from the service collection

    ok, message, code = _version_ok()

    if not ok:
        return message, code
    else:
        services = store.get_service()
        return Catalog(services=services), 200


def register_service(service):
    """
    Registers the service with the catalog.
    \&quot;Service providers need a means to register their service with a service broker. This provides this
    functionality. Also using PUT a service provider can update their registration. Note that this requires the
    complete content and will REPLACE the existing service information registered with the broker.\&quot;
    :param service: the service description to register
    :type service: dict | bytes

    :rtype: Empty
    """
    ok, message, code = _version_ok()
    if not ok:
        return message, code
    else:
        if connexion.request.is_json:  # TODO and if it is not?!
            service = ServiceType.from_dict(connexion.request.get_json())
        store.add_service(service=service)
        return Empty()


def store_manifest(manifest_id, manifest):
    """
    takes deployment description of a software service and associates with a service and plan
    takes deployment description of a software service and associates with a service and plan that is already
    registered in the service catalog.
    :param manifest_id: The manifest_id of a manifest to be associated with a plan of a servicetype.
    :type manifest_id: str
    :param manifest: the manifest to store
    :type manifest: dict | bytes

    :rtype: ServiceResponse
    """
    ok, message, code = _version_ok()
    if not ok:
        return message, code
    else:
        if connexion.request.is_json:  # TODO and if it is not?!
            manifest = Manifest.from_dict(connexion.request.get_json())
        manifest.id = manifest_id
        store.add_manifest(manifest)

        return Empty()
