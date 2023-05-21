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
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
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
        self.diameter =  diameter
        self.designation = None if info['designation'] is None else info['designation'].strip()

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    # @property
    # def name(self):
    #     """Get the name of this NEO for easy reference"""
    #     return self.name
    
    # @name.setter
    # def name(self, nme):
    #     """Set the name of this NEO for easy reference"""
    #     self.name = nme

    @property
    def desig(self):
        """Get the primary designation of this NEO for easy reference"""
        return self.designation
    
    # @designation.setter
    # def designation(self, desig):
    #     """Set the primary designation of this NEO for easy reference"""
    #     self.designation = desig
    
    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        # Use self.designation and self.name to build a fullname for this object.
        return f"{self.designation} {self.name}"
    
    def approached_as(self, approach):
        """Record an approach made by this NEO"""
        self.approaches.append(approach)
        approach.neo = self

    def __str__(self):
        """Return `str(self)`."""
        # TODO: Use this object's attributes to return a human-readable string representation.
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        return f"A NearEarthObject {self.fullname}"

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
    # TODO: How can you, and should you, change the arguments to this constructor?
    # If you make changes, be sure to update the comments in this file.
    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        # Assign information from the arguments passed to the constructor
        # onto attributes named `_designation`, `time`, `distance`, and `velocity`.
        # You should coerce these values to their appropriate data type and handle any edge cases.
        # The `cd_to_datetime` function will be useful.
        self.distance = 0.0
        self.velocity = 0.0
        self.time = None if info['time'] is None else cd_to_datetime(info['time'])
        self.designation = None if info['designation'] is None else info['designation'].strip()
        

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def desig(self):
        """Get the primary designation of the NEO involved in this near approach"""
        return self.designation
    
    # @designation.setter
    # def designation(self, desig):
    #     """Set the primary designation of the NEO involved in this near approach"""
    #     self.designation = desig
    
    @property
    def caused_by(self):
        """Get the NEO involved in this near approach"""
        return self.neo
    
    # @neo.setter
    # def neo(self, a_neo):
    #     self.neo = a_neo

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        # Use this object's `.time` attribute and the `datetime_to_str` function to
        # build a formatted representation of the approach time.
        # Use self.designation and self.name to build a fullname for this object.
        return f"{datetime_to_str(self.time)}"

    def __str__(self):
        """Return `str(self)`."""
        # Use this object's attributes to return a human-readable string representation.
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        return f"A CloseApproach for [{self.neo}]"

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"