.. _create_collector:

*******************
Create a collector
*******************

Opulence facts are located in `~/opulence/collectors/`.


Dependencies
====================

API keys
====================


Rate limits
====================
TODO

Script based collector
====================



::

        from opulence.collectors.bases import ScriptCollector
        from opulence.common.plugins.dependencies import BinaryDependency
        from opulence.facts import Person


        class Example(ScriptCollector):
            ###############
            # Plugin attributes
            ###############
            _name_ = "example script"
            _description_ = "Example script collector"
            _author_ = "Louis"
            _version_ = 1
            _dependencies_ = [BinaryDependency("echo")]

            ###############
            # Collector attributes
            ###############
            _allowed_input_ = Person

            ###############
            # Script attributes
            ###############
            _script_path_ = "echo"
            _script_arguments_ = ["Hello", "$Person.firstname$"]

            def parse_result(self, result):
                return result


Python based collector
====================

Web based collector
====================
