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
           Field(name="temperature", type_=float, description="Temperature in Celsius"),
           Field(name="humidity", type_=float, description="Humidity percentage"),
           Field(name="conditions", type_=str, description="Weather conditions")
       ]

Nested Schema Example
---------------------

.. code-block:: python

   from belso import Schema, Field

   class AddressSchema(Schema):
       name = "AddressSchema"
       fields = [
           Field(name="street", type_=str, description="Street address"),
           Field(name="city", type_=str, description="City name"),
           Field(name="zip_code", type_=str, description="Postal code")
       ]

   class PersonSchema(Schema):
       name = "PersonSchema"
       fields = [
           Field(name="name", type_=str, description="Person's name"),
           Field(name="age", type_=int, description="Person's age"),
           Field(name="address", type_=AddressSchema, description="Person's address")
       ]
