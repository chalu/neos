"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""

from datetime import timezone, datetime
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object,
    such as its primary designation (required, unique), IAU name (optional),
    diameter in kilometers (optional - sometimes unknown), and whether
    it's marked as potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments
        supplied to the constructor.
        """
        name = info['name']
        if name is None or '' == name.strip():
            name = None
        else:
            name = name.strip()

        diameter = info['diameter']
        if diameter is None or diameter == '':
            diameter = float('nan')
        else:
            diameter = float(diameter)

        hazardous = info['hazardous']
        if hazardous == 'Y':
            hazardous = True
        elif hazardous is None or hazardous == '' or hazardous == 'N':
            hazardous = False

        designation = info['designation']
        if designation is None or designation.strip() == '':
            designation = None
        else:
            designation = designation.strip()

        self.name = name
        self.hazardous = hazardous
        self.diameter = diameter
        self.designation = designation

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def pdes(self):
        """Get the primary designation of this NEO for easy reference."""
        return self.designation

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        # Use self.designation and self.name to build a fullname.
        fname = f"{self.designation}"
        if self.name is not None:
            fname = f"{fname} {self.name}"
        return fname

    def approached_as(self, approaches):
        """Record approaches made by this NEO."""
        for apprch in approaches:
            self.approaches.append(apprch)
            apprch.neo = self

    def ascsv(self):
        """Get the data for this NEO for CSV output."""
        return [
            self.designation,
            self.name or '',
            self.diameter,
            self.hazardous or False
        ]

    def asjson(self):
        """Get the data for this NEO for JSON output."""
        return {
            'name': self.name or '',
            'diameter_km': self.diameter,
            'designation': self.designation,
            'potentially_hazardous': self.hazardous or False
        }

    def __str__(self):
        """Return `str(self)`."""
        # Use this object's attributes to return a human-readable string.
        # The project instructions include one possibility.
        # Peek at the __repr__ for examples of advanced formatting.
        return f"NEO {self.fullname}"

    def __repr__(self):
        """Return a computer-readable string of this object."""
        return f"NEO(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's
    close approach to Earth, such as the date and time (in UTC) of closest
    approach, the nominal approach distance in astronomical units, and the
    relative approach velocity in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of keyword args supplied to the constructor.
        """
        # Assign information from the argument onto attributes
        # named `_designation`, `time`, `distance`, and `velocity`.
        # You should coerce these values to their appropriate data type
        # and handle any edge cases.
        # The `cd_to_datetime` function will be useful.
        self.distance = 0.0
        self.velocity = 0.0

        time = info['time']
        if time is not None:
            self.time = cd_to_datetime(time)

        designation = info['designation']
        if designation is not None:
            self._designation = designation.strip()

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def neopdes(self):
        """Get the primary designation of the NEO involved."""
        return self._designation

    @property
    def caused_by(self):
        """Get the NEO involved in this near approach."""
        return self.neo

    @property
    def time_str(self):
        """Return a formatted representation of this approach's time.

        The value in `self.time` should be a Python `datetime` object.
        While a `datetime` object has a string representation, the
        default representation includes seconds - significant figures
        that don't exist in our input data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations
        and in serialization to CSV and JSON files.
        """
        # Use this object's `.time` attribute and the `datetime_to_str`
        # function to build a formatted representation of the approach's.
        # time. Use self._designation and self.name to build a fullname.
        return f"{datetime_to_str(self.time)}"

    def ascsv(self):
        """Get the data for this approach for CSV output."""
        dt_utc = self.time.replace(tzinfo=timezone.utc)
        record = [
            dt_utc.strftime('%Y-%m-%d %H:%M'),
            self.distance,
            self.velocity
        ]
        record.extend(self.neo.ascsv())
        return record

    def asjson(self):
        """Get the data for this Approach for JSON output."""
        dt_utc = self.time.replace(tzinfo=timezone.utc)
        obj = dict()
        obj['datetime_utc'] = dt_utc.strftime('%Y-%m-%d %H:%M')
        obj['distance_au'] = self.distance
        obj['velocity_km_s'] = self.velocity
        obj['neo'] = self.neo.asjson()
        return obj

    def __str__(self):
        """Return `str(self)`."""
        # Use this object's attributes to return a human-readable string.
        # The project instructions include one possibility.
        # Peek at __repr__method for examples of advanced formatting.
        return f"A CloseApproach for [{self.neo}]"

    def __repr__(self):
        """Return a computer-readable string representation of this object."""
        return f"Approach(time={self.time_str!r}, " \
               f"distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"
