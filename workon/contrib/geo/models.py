# encoding: utf-8
import re
import datetime
import random
import math

from django.conf import settings
from django.db import models
from django.utils.html import strip_tags
from django.utils.text import slugify
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.template.defaultfilters import linebreaksbr
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

import workon.models
import workon.fields
import workon.utils


class GeoLocated(models.Model):

    class Meta:
        abstract = True

    geo_address = models.CharField(u'Adresse géolocalisée', max_length=254, blank=True, null=True)
    geo_latitude = models.FloatField(u'lat', blank=True, null=True)
    geo_longitude = models.FloatField(u'lon', blank=True, null=True)
    geo_formatted_address = models.CharField(u'Adresse géocodée & formatée', max_length=254, blank=True, null=True)
    geo_street_number = models.CharField(u'address_components > street_number', max_length=254, blank=True, null=True)
    geo_route = models.CharField(u'address_components > route', max_length=254, blank=True, null=True)
    geo_locality = models.CharField(u'address_components > locality', max_length=254, blank=True, null=True)
    geo_administrative_area_level_1 = models.CharField(u'address_components > administrative_area_level_1', max_length=254, blank=True, null=True)
    geo_administrative_area_level_2 = models.CharField(u'address_components > administrative_area_level_2', max_length=254, blank=True, null=True)
    geo_administrative_area_level_3 = models.CharField(u'address_components > administrative_area_level_3', max_length=254, blank=True, null=True)
    geo_country = models.CharField(u'address_components > country', max_length=254, blank=True, null=True)
    geo_postal_code = models.CharField(u'address_components > postal_code', max_length=254, blank=True, null=True)
    geo_place_id = models.CharField(u'place_id', max_length=254, blank=True, null=True)
    geo_type = models.CharField(u'type', max_length=254, blank=True, null=True)
    # geo_gmaps_results = workon.fields.JSONField(u'Geodata', default={}, blank=True, null=True)

    def geocode(self, force=False, *args, **kwargs):

        if self.geo_address:
            if not force:
                need_geocoding = not (self.geo_latitude and self.geo_longitude)
                if not need_geocoding and self.pk:
                    old_geo_address = self._default_manager.get(pk=self.pk).geo_address
                    if self.geo_address != old_geo_address:
                        need_geocoding = True
            else:
                need_geocoding = True

            if need_geocoding:
                data = workon.utils.geocode(self.geo_address)
                self.geo_latitude = data.get('lat')
                self.geo_longitude = data.get('lng')
                self.geo_formatted_address = data.get('formatted_address')
                for component in data.get('address_components', []):

                    if "street_number" in component.get('types', []):
                        self.geo_street_number = component.get('long_name')
                    if "route" in component.get('types', []):
                        self.geo_route = component.get('long_name')
                    if "locality" in component.get('types', []):
                        self.geo_locality = component.get('long_name')
                    if "administrative_area_level_1" in component.get('types', []):
                        self.geo_administrative_area_level_1 = component.get('long_name')
                    if "administrative_area_level_2" in component.get('types', []):
                        self.geo_administrative_area_level_2 = component.get('long_name')
                    if "administrative_area_level_3" in component.get('types', []):
                        self.geo_administrative_area_level_3 = component.get('long_name')
                    if "country" in component.get('types', []):
                        self.geo_country = component.get('long_name')
                    if "postal_code" in component.get('types', []):
                        self.geo_postal_code = component.get('long_name')
                self.geo_place_id = data.get('place_id')
                self.geo_type = data.get('types', [None])[0]
        else:
            self.geo_gmaps_results = None
            self.geo_latitude = None
            self.geo_longitude = None
            self.geo_formatted_address = None
            self.geo_street_number = None
            self.geo_route = None
            self.geo_locality =None
            self.geo_administrative_area_level_1 = None
            self.geo_administrative_area_level_2 = None
            self.geo_administrative_area_level_3 = None
            self.geo_country = None
            self.geo_postal_code = None
            self.geo_place_id = None
            self.geo_type = None

    def get_geo_locality(self):
        if self.geo_locality:
            return self.geo_locality
        if self.geo_administrative_area_level_2:
            return self.geo_administrative_area_level_2
        if self.geo_administrative_area_level_1:
            return self.geo_administrative_area_level_1
        # if self.geo_gmaps_results:
        #     components = self.geo_gmaps_results.get('address_components', [])
        #     for component in components:
        #         if "locality" in component.get('types', []):
        #             return component.get('short_name')
        #         if "administrative_area_level_2" in component.get('types', []):
        #             return component.get('short_name')
        #         if "administrative_area_level_1" in component.get('types', []):
        #             return component.get('short_name')
        return ""

    def get_geo_full_locality(self):
        if self.geo_formatted_address:
            return mark_safe(self.geo_formatted_address.replace(',','<br />'))
        return None


    def get_geo_location_json(self):
        return {
            "address": self.geo_address,
            "latitude": self.geo_latitude,
            "longitude": self.geo_longitude,
            "formatted_address": self.geo_formatted_address,
            "type": self.geo_type,
            "country": self.geo_country,
            "postal_code": self.geo_postal_code
        }

    def get_geo_distance_from(self, lat2, long2):
        lat1 = self.geo_latitude
        long1 = self.geo_longitude
        if not lat1 or not long1 or not lat2 or not long2:
            return -1
        # Convert latitude and longitude to
        # spherical coordinates in radians.
        degrees_to_radians = math.pi / 180.0

        # phi = 90 - latitude
        phi1 = (90.0 - lat1) * degrees_to_radians
        phi2 = (90.0 - lat2) * degrees_to_radians

        # theta = longitude
        theta1 = long1 * degrees_to_radians
        theta2 = long2 * degrees_to_radians

        # Compute spherical distance from spherical coordinates.

        # For two locations in spherical coordinates
        # (1, theta, phi) and (1, theta, phi)
        # cosine( arc length ) =
        # sin phi sin phi' cos(theta-theta') + cos phi cos phi'
        # distance = rho * arc length

        cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) +
               math.cos(phi1) * math.cos(phi2))
        arc = math.acos(cos)

        # Remember to multiply arc by the radius of the earth
        # in your favorite set of units to get length.
        return float(round(arc * 6371 * 1000))