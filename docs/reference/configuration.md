# Configuration Reference

FastMango uses a Django-style settings object to configure your application. This allows you to keep all of your configuration in a single, easy-to-manage file.

## The `settings.py` File

By convention, you should define your settings in a file named `settings.py` in your project's root directory. This file should contain a `Settings` class that defines your application's configuration.

Here's an example of what a `settings.py` file might look like:

```python
import os

class Settings:
    """
    Your project's settings.
    """

    # A secret key used for cryptographic signing.
    SECRET_KEY: str = os.getenv("SECRET_KEY", "a-default-secret-key")

    # The connection string for your database.
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///db.sqlite3")

    # A boolean that turns on/off debug mode.
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # A list of allowed hosts.
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"]

# An instance of the Settings class that will be used by your application.
settings = Settings()
```

## Using Environment Variables

As you can see in the example above, it's a good practice to use environment variables to configure your application in different environments (e.g., development, staging, production).

You can use `os.getenv()` to read the value of an environment variable, and provide a default value for when the environment variable is not set.

## Common Settings

Here are some of the common settings that you might want to configure in your application:

-   **`SECRET_KEY`**: A long, random string that is used for cryptographic signing. This should be kept secret in production.
-   **`DATABASE_URL`**: The connection string for your database.
-   **`DEBUG`**: A boolean that turns on/off debug mode. This should be set to `False` in production.
-   **`ALLOWED_HOSTS`**: A list of strings representing the host/domain names that your FastMango site can serve.
-   **`CORS_ORIGINS`**: A list of origins that are allowed to make cross-site requests to your API.
-   **`JWT_SECRET_KEY`**: The secret key to use for signing JSON Web Tokens (JWTs).
-   **`JWT_ALGORITHM`**: The algorithm to use for signing JWTs.
-   **`JWT_EXPIRE_MINUTES`**: The number of minutes after which a JWT will expire.

## Accessing Settings in Your Application

To access your settings in your application, you can import the `settings` object from your `settings.py` file:

```python
from myproject.settings import settings

def my_function():
    if settings.DEBUG:
        print("Debug mode is on.")
```
