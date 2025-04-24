Examples
========

Here are some examples of how to use belso in different scenarios.

Basic Schema Example
--------------------

.. code-block:: python

   from belso.schemas import Schema, BaseField

   class WeatherSchema(Schema):
       name = "WeatherSchema"
       fields = [
           BaseField(name="temperature", type=float, description="Temperature in Celsius"),
           BaseField(name="humidity", type=float, description="Humidity percentage"),
           BaseField(name="conditions", type=str, description="Weather conditions")
       ]

Nested Schema Example
---------------------

.. code-block:: python

   from belso.schemas import Schema, BaseField
   from belso.schemas.nested import NestedField

   class AddressSchema(Schema):
       name = "AddressSchema"
       fields = [
           BaseField(name="street", type=str, description="Street address"),
           BaseField(name="city", type=str, description="City name"),
           BaseField(name="zip_code", type=str, description="Postal code")
       ]

   class PersonSchema(Schema):
       name = "PersonSchema"
       fields = [
           BaseField(name="name", type=str, description="Person's name"),
           BaseField(name="age", type=int, description="Person's age"),
           NestedField(name="address", schema=AddressSchema, description="Person's address")
       ]
