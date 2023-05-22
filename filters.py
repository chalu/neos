"""Provide filters for querying approaches and limit the results.

The `create_filters` function produces a collection of objects that is used by
the `query` method to generate a stream of `CloseApproach` objects that match
all of the desired criteria. The arguments to `create_filters` are provided by
the main module and originate from the user's command-line options.

This function can be thought to return a collection of instances of subclasses
of `AttributeFilter` - a 1-argument callable (on a `CloseApproach`) constructed
from a comparator (from the `operator` module), a reference value, and a class
method `get` that subclasses can override to fetch an attribute of
interest from the supplied `CloseApproach`.

The `limit` function simply limits the maximum number of values produced by an
iterator.

You'll edit this file in Tasks 3a and 3c.
"""
import operator as op


class UnsupportedCriterionError(NotImplementedError):
    """A filter criterion is unsupported."""


class AttributeFilter:
    """A general superclass for filters on comparable attributes.

    An `AttributeFilter` represents the search criteria pattern
    comparing some attribute of a close approach (or its attached NEO)
    to a fixed value. It essentially functions as a callable predicate
    for whether a `CloseApproach` object satisfies the encoded
    criterion.

    It is constructed with a comparator operator and a reference value,
    and calling the filter (with __call__) executes `get(approach) OP
    value` (in infix notation).

    Concrete subclasses can override the `get` classmethod to provide
    custom behavior to fetch a desired attribute from the given
    `CloseApproach`.
    """

    def __init__(self, opr, value):
        """Construct a new filter from a predicate and a fixed value.

        The reference value will be supplied as the second (right-hand
        side) argument to the operator function. For example, an
        `AttributeFilter` with `op=operator.le` and `value=10` will,
        when called on an approach, evaluate `some_attribute <= 10`.

        :param op: A 2-argument predicate comparator (such as `operator.le`).
        :param value: The reference value to compare against.
        """
        self.opr = opr
        self.value = value

    def __call__(self, approach):
        """Invoke `self(approach)`."""
        return self.opr(self.prop(approach), self.value)

    @classmethod
    def prop(cls, approach):
        """Get an attribute of interest from a close approach.

        Concrete subclasses must override this method to get an
        attribute of interest from the supplied `CloseApproach`.

        :param approach: A `CloseApproach` on which to evaluate this filter.
        :return: The value of an attribute of interest. See `self.value`.
        """
        raise UnsupportedCriterionError

    def info(self):
        """Provide hints about this filter.

        Ideally the filter class name should be sufficient
        """
        return "A filter for NEOS and Approaches"

    def __repr__(self):
        """Well formatted string representation."""
        return f"{self.__class__.__name__}(op=operator.{self.opr.__name__}, " \
               f"value={self.value})"

# ==============================================
# Start filters that apply to NEOs
# ==============================================


class FilterByDiameter(AttributeFilter):
    """Filter NEO by diameter."""

    @classmethod
    def prop(cls, approach):
        """Get the `diameter` attribute from a NEO."""
        return approach.neo.diameter


class FilterByHazardous(AttributeFilter):
    """Filter NEO by if hazardous or not."""

    @classmethod
    def prop(cls, approach):
        """Get the `hazardous` attribute from a NEO."""
        return approach.neo.hazardous

# ==============================================
# Start filters that apply to Approaches
# ==============================================

# date, distance, and velocity


class FilterByVelocity(AttributeFilter):
    """Filter Approache by velocity."""

    @classmethod
    def prop(cls, approach):
        """Get the `velocity` attribute from a close approach."""
        return approach.velocity


class FilterByDistance(AttributeFilter):
    """Filter Approache by distance."""

    @classmethod
    def prop(cls, approach):
        """Get the `distance` attribute from a close approach."""
        return approach.distance


class FilterByDate(AttributeFilter):
    """Filter Approache by date."""

    @classmethod
    def prop(cls, approach):
        """Get `date` from the `time` attribute from a close approach."""
        return approach.time.date()

# ==============================================
# End filters
# ==============================================


def create_filters(
        date=None, start_date=None, end_date=None,
        distance_min=None, distance_max=None,
        velocity_min=None, velocity_max=None,
        diameter_min=None, diameter_max=None,
        hazardous=None
):
    """Create a collection of filters from user-specified criteria.

    Each argument is provided by the main module with a value from the
    user's input at the command line. Each one corresponds to a
    different type of filter. For example, the `--date` option
    corresponds to the `date` argument, and represents a filter that
    selects close approaches that occurred on exactly that given date.
    Similarly, the `--min-distance` option corresponds to the
    `distance_min` argument, and represents a filter that selects close
    approaches whose nominal approach distance is at least that far away
    from Earth. Each option is `None` if not specified at the command
    line (in particular, this means that the `--not-hazardous` flag
    results in `hazardous=False`, not to be confused with
    `hazardous=None`).

    The return value must be compatible with the `query` method of
    `NEODatabase` because the main module directly passes this result to
    that method. For now, consider this as a collection of
    `AttributeFilter`s.

    :param date: A `date` on which a `CloseApproach` occurs.
    :param start_date: A `date` on or after which a `CloseApproach` occurs.
    :param end_date: A `date` on or before which a `CloseApproach` occurs.
    :param distance_max: A maximum nominal distance for a `CloseApproach`.
    :param velocity_min: A minimum relative velocity for a `CloseApproach`.
    :param velocity_max: A maximum relative velocity for a `CloseApproach`.
    :param diameter_min: A minimum diameter of the NEO of a `CloseApproach`.
    :param diameter_max: A maximum diameter of the NEO of a `CloseApproach`.
    :param hazardous: If the NEO of a `CloseApproach` is potentially hazardous.
    :return: A collection of filters for use with `query`.
    """
    filters = list()

    if diameter_min is not None:
        filters.append(FilterByDiameter(op.ge, float(diameter_min)))

    if diameter_max is not None:
        filters.append(FilterByDiameter(op.le, float(diameter_max)))

    if hazardous is not None:
        filters.append(FilterByHazardous(op.eq, bool(hazardous)))

    if velocity_min is not None:
        filters.append(FilterByVelocity(op.ge, float(velocity_min)))

    if velocity_max is not None:
        filters.append(FilterByVelocity(op.le, float(velocity_max)))

    if distance_min is not None:
        filters.append(FilterByDistance(op.ge, float(distance_min)))

    if distance_max is not None:
        filters.append(FilterByDistance(op.le, float(distance_max)))

    if date is not None:
        filters.append(FilterByDate(op.eq, float(date)))

    if start_date is not None:
        filters.append(FilterByDate(op.ge, float(start_date)))

    if end_date is not None:
        filters.append(FilterByDate(op.le, float(end_date)))

    return tuple(filters)


def limit(iterator, cap=None):
    """Produce a limited stream of values from an iterator.

    If `cap` is 0 or None, don't limit the iterator at all.

    :param iterator: An iterator of values.
    :param cap: The maximum number of values to produce.
    :yield: The first (at most) `cap` values from the iterator.
    """
    # Produce at most `cap` values from the given iterator.
    cap = len(iterator) if cap is None or cap == 0 else cap
    return iterator[:cap]
