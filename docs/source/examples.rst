Examples
========

Explore these practical examples to understand how Belso can be used in different scenarios.

Basic Schema Example
--------------------

.. code-block:: python

   from belso import Schema, Field

   class WeatherSchema(Schema):
       fields = [
           Field(name="temperature", type=float, description="Temperature in Celsius"),
           Field(name="humidity", type=float, description="Humidity percentage"),
           Field(name="conditions", type=str, description="Weather conditions")
       ]

Nested Schema Example
---------------------

.. code-block:: python

   from belso import Schema, Field

   class AddressSchema(Schema):
       fields = [
           Field(name="street", type=str, description="Street address"),
           Field(name="city", type=str, description="City name"),
           Field(name="zip_code", type=str, description="Postal code")
       ]

   class PersonSchema(Schema):
       fields = [
           Field(name="name", type=str, description="Person's name"),
           Field(name="age", type=int, description="Person's age"),
           Field(name="address", type=AddressSchema, description="Person's address")
       ]
