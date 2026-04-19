import os

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

from src.services.log_service import log_service


def init_sentry():

    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        integrations=[FastApiIntegration()],
        environment=os.getenv("ENVIRONMENT", "development"),
        release=os.getenv("RELEASE_VERSION", "dev"),
        traces_sample_rate=float(os.getenv("SENTRY_TRACES_RATE", "0.01")),
        send_default_pii=os.getenv("ENVIRONMENT") != "production",
        before_send=lambda event, hint: (
            None
            if hint.get("exc_info")
            and hasattr(hint["exc_info"][1], "status_code")
            and hint["exc_info"][1].status_code < 500
            else event
        ),
    )

    log_service.info("Sentry initialized")
