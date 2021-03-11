.. _my-reference-label:

*******************
Collectors
*******************

What is a collector
==========================

Collectors are classes which generate intelligence from facts.
Collectors allow us to create links between facts (i.e. from an email address find a user's facebook account, from a telephone number find a user's name)

An opulence of collectors have already been developped by the community, opulence provides a central platform to manage them all !

For opulence, a collector can be seen as a class which takes one or more :class:`fact` as input, and will return some more. See :ref:`facts`.

opulence comes with some pre-made collectors, you may want to add your own collectors, see  :ref:`Extending collectors`.


Collector's helpers
==========================

In order to simplify the integration of new collectors into opulence, some helpers have been made in order to make your life easier.



.. list-table:: Collectors
   :widths: 25 50
   :header-rows: 1

   * - Collector type
     - When to use
   * - ScriptCollector
     - Usefull for executable files (binaries, python scripts, batch files ...)
   * - PyPiCollector
     - Used for importing a python package (installable through the pip command)
   * - NakedCollector
     - Depending on your specific needs


Naked
---------------

::

	from opulence.facts.person import Person
	from opulence.collectors import BaseCollector

	class example(BaseCollector):
	    ###############
	    # Plugin attributes
	    ###############
	    _name_ = "example"
	    _description_ = "This is an example naked collector"
	    _author_ = "??"
	    _version_ = 0.42
	    _dependencies_ = []

	    ###############
	    # Collector attributes
	    ###############
	    _allowed_input_ = (Person)

	    def launch(self, facts):
	    	pass

.. attribute:: _name_

	String representating the collector display name.

	.. note::
		This is only used for display purposes. Duplicates names are allowed

.. attribute:: _description_

	String containing the collector aim

.. attribute:: _author_

	Author's name

.. attribute:: _version_

	Version of the collector

.. attribute:: _dependencies_

	Collectors can contain a list of dependencies.
	See :ref:`dependencies` for the available dependencies.

.. attribute:: _allowed_input_


	Represents the types of input the collector can accept.
	It must be a :class:`fact` type or a list of :class:`fact` types.
	(i.e :class:`Person` or :class:`[Person, Email, Telephone]`)

	Each time the collector will be executed, one of the :class:`_allowed_input_` will be provided as an argument.

	.. note::
		You may need multiple facts at once. You can use the :class:`Composite` class.

		:class:`Composite` allows you to join multiple facts together. If you need both an email address and a telephone number, you can use the following :class:`Composite` : :class:`Composite(Email, Telephone)`


Scripts
------------------

::

	from opulence.facts.person import Person
	from opulence.collectors.scripts import ScriptCollector

	class exampleScript(ScriptCollector):
	    ###############
	    # Plugin attributes
	    ###############
	    _name_ = "example"
	    _description_ = "This is an example script collector"
	    _author_ = "Author Name"
	    _version_ = 0.42
	    _dependencies_ = []

	    ###############
	    # Collector attributes
	    ###############
	    _allowed_input_ = (Person)

	    ###############
	    # Script attributes
	    ###############
	    _script_path_ = "echo"
	    _script_arguments_ = ["Hello", "$Person.firstname$"]

	    def parse_result(self, result):
	        pass


.. attribute:: _script_path_

	Mandatory string containing the executable path. This command will be automatically executed with the :class:`_script_arguments_` parameters.

	It can be a relative path (i.e. :class:`"ls"` or :class:`"../ls"`) or an absolute path (i.e. :class:`"/bin/ls"`)

.. attribute:: _script_arguments_

	Mandatory array containing the arguments to provide to the :class:`_script_path_`. Scripts argument might be a string (one single argument): :class:`"Hello"`, a list : :class:`["Hello", "world"]`, a tuple : :class:`("Hello", "world")`

	Arguments can contain special variables called sigil. (a "little sign" supposedly having magical power).

	Special characters starts and ends by "$" (e.g. :class:`$Person$` or :class:`$Person.firstname$`).

	The purpose of those special arguments is to provide to the executable file the correct parameters.

	.. warning::
		Special arguments should contains a :class:`Fact`, or a :class:`Fact.attribute` provided in the :class:`_allowed_input_` attribute.


	.. note::
		You can provide an empty special argument : :class:`$$`, the core engine will try to guess the correct arguments.
		This can be a great shortcut if you have only one :class:`_allowed_input_`, otherwise, it might not work perfectly

Python packages
------------------------

::

	from opulence.facts.person import Person
	from opulence.collectors.pypi import PypiCollector

	class examplePypi(PypiCollector):
	    ###############
	    # Plugin attributes
	    ###############
	    _name_ = "example"
	    _description_ = "This is an example pypi collector"
	    _author_ = "??"
	    _version_ = 0.42
	    _dependencies_ = []

	    ###############
	    # Collector attributes
	    ###############
	    _allowed_input_ = (Person)

	    ###############
	    # PyPi attributes
	    ###############
	    _package_name_ = "requests"

	    def exec(self, facts):
	        r = self.package.get("http://example.com")

.. attribute:: _package_name_

	Mandatory string attribute containing the python package to load.
	The package will be available under the :class:`package` attribute once loaded.
