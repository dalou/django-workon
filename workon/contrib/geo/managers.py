# encoding: utf-8

from django.db import models
from django.db.models import Q
from django.utils.datastructures import OrderedDict

from geopy import units, distance


class BaseLocationManager(models.Manager):
    """
    Manager location aware
    """

    def _format_params(self, latitude=0, longitude=0, distance_range=0):
        # handle the distance_range using the `Distance` class
        if isinstance(distance_range, distance.Distance):
            distance_range = distance_range.kilometers
        return map(float, (latitude or 0, longitude or 0, distance_range or 0))

    def nearby(self, latitude, longitude, proximity):
        """
        Return all object which distance to specified coordinates
        is less than proximity given in kilometers
        """
        # Great circle distance formula
        gcd = """
              6371 * acos(
               cos(radians(%s)) * cos(radians(geo_latitude))
               * cos(radians(geo_longitude) - radians(%s)) +
               sin(radians(%s)) * sin(radians(geo_latitude))
              )
              """
        gcd_lt = "{} < %s".format(gcd)
        return self.get_queryset()\
                   .exclude(geo_latitude=None)\
                   .exclude(geo_longitude=None)\
                   .extra(
                       select={'distance': gcd},
                       select_params=[latitude, longitude, latitude],
                       where=[gcd_lt],
                       params=[latitude, longitude, latitude, proximity],
                       order_by=['distance']
                   )


    def near(self, latitude=None, longitude=None, distance_range=None, skip_box_approximation=False):
        """
        @param float latitude
        @param float longitude
        @param float distance_range in kilometers | Distance instance
        """
        query_set = super(BaseLocationManager, self).get_queryset()

        if not (latitude and longitude and distance_range):
            return query_set.none()

        if not skip_box_approximation:
            lat, lon, dis = self._format_params(latitude, longitude, distance_range)

            # approximate the area where to search for places
            rough_distance = units.degrees(arcminutes=units.nautical(kilometers=dis)) * 2
            query_set = query_set.filter(
                geo_latitude__range=(
                    lat - rough_distance,
                    lat + rough_distance
                ),
                geo_longitude__range=(
                    lon - rough_distance,
                    lon + rough_distance
                )
            )
        return query_set


class TwoQueryLocationManager(BaseLocationManager):

    def near(self, *args, **kwargs):
        queryset = super(TwoQueryLocationManager, self).near(*args, **kwargs)
        lat, lon, dis = self._format_params(kwargs.get('latitude', 0), kwargs.get('longitude', 0), kwargs.get('distance_range', 0))
        locations = []
        for location in queryset:
          if location.latitude and location.longitude:
            exact_distance = distance.distance(
                (lat, lon),
                (location.latitude, location.longitude)
            ).kilometers

            if exact_distance <= dis:
              locations.append(location)
        queryset = queryset.filter(id__in=[l.id for l in locations])
        return queryset


class HaversineLocationManager(BaseLocationManager):

    def near(self, *args, **kwargs):
        queryset = super(HaversineLocationManager, self).near(*args, **kwargs)
        lat, lon, dis = self._format_params(kwargs.get('latitude', 0), kwargs.get('longitude', 0), kwargs.get('distance_range', 0))
        queryset = queryset.extra(
                select=OrderedDict([('distance', 'geodistance(%s, %s, geo_latitude, geo_longitude)')]),
                select_params=(lat, lon),
                where=('geodistance(%s, %s, geo_latitude, geo_longitude) <= %s',),
                params=(lat, lon, dis)
            )
        return queryset


class OnlyHaversineLocationManager(HaversineLocationManager):

    def near(self, *args, **kwargs):
        kwargs['skip_box_approximation'] = True
        queryset = super(OnlyHaversineLocationManager, self).near(*args, **kwargs)
        return queryset
