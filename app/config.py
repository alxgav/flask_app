class Config:
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///expenses.db"
    JWT_SECRET_KEY = "3afb314dfc68843fe25a261af3afbeea117eb1b960afadafedc249ae12312cab"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
