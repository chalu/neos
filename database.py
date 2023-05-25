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

    def __init__(self, neos, approaches, use_map=False):
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
        self.use_map = use_map

        # What additional auxiliary data structures will be useful?
        # Link together the NEOs and their close approaches.
        print("\nLinking NEOs and their approaches ...")
        count = 0
        if self.use_map:
            for neopdes in self._approaches:
                neo = neos[neopdes]
                if neo is not None:
                    apprchs = self._approaches[neopdes]
                    neo.approached_as(apprchs)
                    count += len(apprchs)

        else:
            for apprch in self._approaches:
                for neo in self._neos:
                    if neo.pdes == apprch.neopdes:
                        neo.approached_as([apprch])
                        count += 1

        print(f"\nDone! Linked {count} Appraoches\n\n")

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
        if self.use_map:
            for pdes in self._neos:
                neo = self._neos[pdes]
                if pdes == designation:
                    found = neo
                    break
        else:
            for neo in self._neos:
                if neo.pdes == designation:
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
        if self.use_map:
            for pdes in self._neos:
                neo = self._neos[pdes]
                if neo.name is None or neo.name == '':
                    continue
                if neo.name == name:
                    found = neo
                    break

        else:
            for neo in self._neos:
                if neo.name is None or neo.name == '':
                    continue

                if neo.name == name:
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
        if self.use_map:
            for neopdes in self._approaches:
                elligible = True
                approaches = self._approaches[neopdes]
                for apprch in approaches:
                    for fltr in filters:
                        if not fltr(apprch):
                            elligible = False
                            break
                    # if any filter failed, then we don't have a match!
                    if elligible:
                        yield apprch
        else:
            for apprch in self._approaches:
                elligible = True
                for fltr in filters:
                    if not fltr(apprch):
                        elligible = False
                        break

                # if any filter failed, then we don't have a match!
                if elligible:
                    yield apprch
