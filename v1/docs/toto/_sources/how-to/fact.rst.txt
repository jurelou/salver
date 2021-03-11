.. _create_fact:

*******************
Create a fact
*******************

Opulence facts are located in `~/opulence/facts/`.

Facts should be importable from `opulence.facts`

For example:


**GOOD**
::

	from opulence.facts import Person

**BAD**
::

	from opulence.facts.person import Person

You should import your fact in the `~/opulence/facts/__init__.py`


Example fact
------------------------


::

    from opulence.common.fields import StringField
    from opulence.facts.bases import BaseFact


    class Person(BaseFact):
        _name_ = "Email"
        _description_ = "This is a person !"
        _author_ = "Louis"
        _version_ = 1

        def setup(self):
            self.name = StringField(mandatory=True, default="john")
            self.lastname = StringField(mandatory=True, default="snow")

        def get_summary(self):
            return "{} {}".format(self.name.value, self.lastname.value)

.. method:: setup()

    Used for defining a fact's attributes.
    Attributes should be one of the following:

    - `StringField`
    - `IntegerField`
    - `FloatField`


.. method:: get_summary() -> string

    Returns human readable summary for the given fact, this is mainly used for visualisations purposes.
