Examples
========

Here are some examples of how to use belso in different scenarios.

Basic Schema Example
--------------------

.. code-block:: python

   from belso import Schema, Field

   class WeatherSchema(Schema):
       name = "WeatherSchema"
       fields = [
           Field(name="temperature", type_hint=float, description="Temperature in Celsius"),
           Field(name="humidity", type_hint=float, description="Humidity percentage"),
           Field(name="conditions", type_hint=str, description="Weather conditions")
       ]

Nested Schema Example
---------------------

.. code-block:: python

   from belso import Schema, Field

   class AddressSchema(Schema):
       name = "AddressSchema"
       fields = [
           Field(name="street", type_hint=str, description="Street address"),
           Field(name="city", type_hint=str, description="City name"),
           Field(name="zip_code", type_hint=str, description="Postal code")
       ]

   class PersonSchema(Schema):
       name = "PersonSchema"
       fields = [
           Field(name="name", type_hint=str, description="Person's name"),
           Field(name="age", type_hint=int, description="Person's age"),
           Field(name="address", type_hint=AddressSchema, description="Person's address")
       ]
