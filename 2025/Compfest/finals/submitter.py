#!/usr/bin/env python3
import requests
from exploitfarm.models.enums import FlagStatus

baseURL = 'https://api.ctf-compfest.com'
# baseURL = 'http://host.docker.internal:8000'

def submit(flags, secret: str = "", magic_number: int = 42, verbose: bool = False, other=None, http_timeout: int = 30):
    """
    Submit flags to CompFest protocol and yield (flag, FlagStatus, verdict_message) for each flag.
    """

    # Authenticate first
    try:
        auth_res = requests.post(
            baseURL + "/api/v2/authenticate",
            json={
                "email": "akuazril12@gmail.com",
                "password": "616ee8fd94830cb161ab1906e7e3731a",
            },
            verify=False,
            timeout=http_timeout
        )
    except Exception as e:
        msg = f"auth request failed: {e}"
        for flag in flags:
            yield (flag, FlagStatus.wait, msg)
        return

    if auth_res.status_code != 200:
        msg = f"auth failed: {auth_res.status_code} {auth_res.text}"
        for flag in flags:
            yield (flag, FlagStatus.wait, msg)
        return

    jwt = auth_res.json().get("data")
    if not jwt:
        msg = f"auth response missing token: {auth_res.text}"
        for flag in flags:
            yield (flag, FlagStatus.wait, msg)
        return

    # Submit flags
    try:
        res = requests.post(
            baseURL + "/api/v2/submit",
            json={"flags": flags},
            headers={"Authorization": f"Bearer {jwt}"},
            verify=False,
            timeout=http_timeout
        )
    except Exception as e:
        msg = f"submit request failed: {e}"
        for flag in flags:
            yield (flag, FlagStatus.wait, msg)
        return

    # Rate limit
    if res.status_code == 429:
        for flag in flags:
            yield (flag, FlagStatus.wait, "too many requests")
        return

    # Contest not started / finished / generic error
    if res.status_code != 200:
        try:
            body = res.json()
            msg = body.get("message", res.text)
        except Exception:
            msg = res.text

        lower = msg.lower()
        if "contest has not started" in lower:
            status = FlagStatus.wait
        elif "contest is over" in lower:
            status = FlagStatus.invalid
        else:
            status = FlagStatus.invalid

        for flag in flags:
            yield (flag, status, msg)
        return

    # Success response
    body = res.json()
    data = body.get("data", [])
    if not isinstance(data, list):
        for flag in flags:
            yield (flag, FlagStatus.wait, f"unexpected response: {body}")
        return

    for i, item in enumerate(data):
        flag_val = item.get("flag", flags[i] if i < len(flags) else None)
        verdict = item.get("verdict", "")

        verdict_lower = verdict.lower()

        # Map exactly as per docs
        if "correct" in verdict_lower:
            status = FlagStatus.ok
        elif "already submitted" in verdict_lower:
            status = FlagStatus.invalid
        elif "wrong" in verdict_lower or "expired" in verdict_lower:
            status = FlagStatus.invalid
        else:
            # fallback
            status = FlagStatus.wait

        yield (flag_val, status, verdict)