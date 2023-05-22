"""A database encapsulating collections of NEOs and their approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""


class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """

    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections
        of NEOs and approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and approaches to link them
        together - after it's done, the `.approaches` attribute of each NEO has
        a collection of that NEO's approaches, and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches

        # What additional auxiliary data structures will be useful?

        # Link together the NEOs and their close approaches.
        for neo in self._neos:
            designation = neo.desig

            if designation is None or designation == '':
                continue

            for apprch in self._approaches:
                if apprch.desig is None or apprch.desig == '':
                    continue

                if apprch.desig.lower() == designation.lower():
                    neo.approached_as(apprch)

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NEO` with the desired primary designation, or `None`.
        """
        # Fetch an NEO by its primary designation.
        if designation is None or designation == '':
            return None

        found = None
        for neo in self._neos:
            if neo.desig is None or neo.desig == '':
                continue

            if neo.desig.lower() == designation.lower():
                found = neo
                break

        return found

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        # Fetch an NEO by its name.
        if name is None or name == '':
            return None

        found = None
        for neo in self._neos:
            if neo.name is None or neo.name == '':
                continue

            if neo.name.lower() == name.lower():
                found = neo
                break

        return found

    def query(self, filters=()):
        """Query close approaches to generate those that match given filters.

        This generates a stream of `CloseApproach` that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` are generated in internal order, which isn't
        guaranteed to be sorted meaningfully, although often sorted by time.

        :param filters: A collection of filters capturing user criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        # Generate `CloseApproach` objects that match all of the filters.
        for approach in self._approaches:
            elligible = True
            for check in filters:
                elligible = check(approach)
                if elligible is False:
                    break

            # any filter failed
            if elligible is False:
                continue

            yield approach
