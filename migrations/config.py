TORTOISE_ORM = {
    "connections": {"default": "postgres://rentdb:rentdb@rent-postgres:5432/rent"},
    "apps": {
        "models": {
            "models": ["app.database", "aerich.models"],
            "default_connection": "default",
        },
    },
}