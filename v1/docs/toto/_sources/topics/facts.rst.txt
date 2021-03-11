
.. _facts:

*******************
Facts
*******************

What is a fact
==========================
A fact is something that is known to have happened or to exist, something for which proof exists.

Facts are used to describe types of information. Basically, it is a Python plugin which defines an information flange.

---------

opulence commes with some pre-made Facts, you may want to add your own Facts. :ref:`Extending facts`


Here are some examples of common tasks performed with facts using the Person fact:

Working with facts:
==========================

Declaring a fact:
-----------------

Facts are created using one or more keyworded arguments to the constructor

::

    >>> from opulence.facts.person import Person
    >>> person = Person(firstname="Alain", lastname="Deloin")

Check if a fact is valid
-----------------------
In order to verify if a fact contains the necessary data you can use the following method:

::

    >>> person = Person(firstname="Alain", lastname="Deloin")
    >>> print(person.is_valid())
    True

Extending facts
==========================

Facts are declared using a simple class definition syntax. Here is an example

::

	from opulence.facts import BaseFact

	class Person(BaseFact):
		_name_ = "Person"
		_description_ = "This is a Person !"
		_author_ = "author name"
		_version_ = "0.1"

		_mandatory_fields_ = ("lastname", "firstname")

The most important attribute is :class:`_mandatory_fields_` . This attribute will contain all the mandatory fields.
All thoses fields will be required upon the class instantiation
