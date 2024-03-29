import sentry_sdk
from api import api
from api.staff.v1.auth import ns as staff_auth_ns
from api.v1.auth import ns as auth_ns
from api.v1.authorization import ns as authorization_ns
from api.v1.captcha import ns as captcha_ns
from api.v1.oauth import ns as oauth_ns
from api.v1.users import ns as profile_ns
from core.db import init_session
from core.oauth import oauth
from core.utils import add_logstash_handler
from flask import Flask, request
from pydantic import BaseSettings, PostgresDsn, RedisDsn
from redis import Redis
from sentry_sdk.integrations.flask import FlaskIntegration
from services import Services


class Settings(BaseSettings):
    redis_dsn: RedisDsn
    postgres_dsn: PostgresDsn
    secret_key: str

    oauth_facebook_client_id: str
    oauth_facebook_client_secret: str
    sentry_dsn: str
    logstash_host: str
    logstash_port: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def create_app():
    settings = Settings()
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0,
    )

    app = Flask(__name__)

    app.config["SECRET_KEY"] = settings.secret_key
    app.config["ERROR_404_HELP"] = False

    app.config["FACEBOOK_CLIENT_ID"] = settings.oauth_facebook_client_id
    app.config["FACEBOOK_CLIENT_SECRET"] = settings.oauth_facebook_client_secret
    app.config[
        "FACEBOOK_ACCESS_TOKEN_URL"
    ] = "https://graph.facebook.com/oauth/access_token"
    app.config["FACEBOOK_AUTHORIZE_URL"] = "https://www.facebook.com/dialog/oauth"
    app.config["FACEBOOK_API_BASE_URL"] = "https://graph.facebook.com"
    app.config["FACEBOOK_CLIENT_KWARGS"] = {"scope": "public_profile, email"}

    session = init_session(f"{str(settings.postgres_dsn)}/auth")
    redis = Redis(host=settings.redis_dsn.host, port=settings.redis_dsn.port, db=1)

    oauth.init_app(app)
    oauth.register("facebook")

    api.init_app(app)
    api.add_namespace(profile_ns, "/api/v1/profile")
    api.add_namespace(auth_ns, "/api/v1/auth")
    api.add_namespace(oauth_ns, "/api/v1/oauth")
    api.add_namespace(staff_auth_ns, "/staff/api/v1/auth")
    api.add_namespace(authorization_ns, "/api/v1/authorization")
    api.add_namespace(captcha_ns, "/api/v1/captcha")

    services = Services(session, redis, settings.secret_key)
    app.extensions["services"] = services
    api.services = services

    return add_logstash_handler(app, settings)


app = create_app()


@app.after_request
def log_request_info(response):
    app.logger.info(f"{request.remote_addr} {request.method} {request.scheme} \
        {request.full_path} {request.get_data()} {response.status}")
    return response
