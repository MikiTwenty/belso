Examples
========

Here are some examples of how to use belso in different scenarios.

Basic Schema Example
--------------------

.. code-block:: python

   from belso.schemas import Schema, Field

   class WeatherSchema(Schema):
       name = "WeatherSchema"
       fields = [
           Field(name="temperature", type=float, description="Temperature in Celsius"),
           Field(name="humidity", type=float, description="Humidity percentage"),
           Field(name="conditions", type=str, description="Weather conditions")
       ]

Nested Schema Example
---------------------

.. code-block:: python

   from belso.schemas import Schema, Field
   from belso.schemas.nested import NestedField

   class AddressSchema(Schema):
       name = "AddressSchema"
       fields = [
           Field(name="street", type=str, description="Street address"),
           Field(name="city", type=str, description="City name"),
           Field(name="zip_code", type=str, description="Postal code")
       ]

   class PersonSchema(Schema):
       name = "PersonSchema"
       fields = [
           Field(name="name", type=str, description="Person's name"),
           Field(name="age", type=int, description="Person's age"),
           NestedField(name="address", schema=AddressSchema, description="Person's address")
       ]
