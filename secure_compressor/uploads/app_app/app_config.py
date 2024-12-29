import os

class Config:
    # MySQL database configuration
    SQLALCHEMY_DATABASE_URI =  "mysql+pymysql://admin:.rlXI0}1mq}gf+(Gp$DGA7<%#-.7@mariadb-container/studybeam"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    AUTH_REDIRECT_URL = "http://localhost:5000/google/auth_callback"
    AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"

    # Google OAuth configuration
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

    # Microsoft OAuth configuration
    MS_CLIENT_ID = os.getenv('MS_CLIENT_ID')
    MS_CLIENT_SECRET = os.getenv('MS_CLIENT_SECRET')
    MS_AUTHORITY = "https://login.microsoftonline.com/common"
    MS_SCOPE = ["User.Read", "Tasks.ReadWrite", "Calendars.ReadWrite"]
    MS_REDIRECT_URI = "http://localhost:5000/ms/callback"  # Your redirect URI after MS auth
