"""Resend email backend using httpx (no SDK dependency).

Fork-only — not part of upstream PR.

Usage:
    EMAIL_BACKEND=custom
    EMAIL_BACKEND_CLASS=app.cabinet.services.resend_backend:ResendBackend
    RESEND_API_KEY=re_xxxxx
"""

from __future__ import annotations

import os

import httpx
import structlog

from .email_backends import EmailMessage

logger = structlog.get_logger(__name__)

RESEND_API_KEY = os.environ.get('RESEND_API_KEY', '')


class ResendBackend:
    """Email backend that sends via Resend REST API."""

    def is_configured(self) -> bool:
        return bool(RESEND_API_KEY)

    def send(self, message: EmailMessage) -> bool:
        resp = httpx.post(
            'https://api.resend.com/emails',
            headers={'Authorization': f'Bearer {RESEND_API_KEY}'},
            json={
                'from': f'{message.from_name} <{message.from_email}>',
                'to': [message.to_email],
                'subject': message.subject,
                'html': message.body_html,
                'text': message.body_text,
            },
            timeout=30,
        )
        resp.raise_for_status()
        return True
