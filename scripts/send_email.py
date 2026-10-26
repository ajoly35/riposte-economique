"""Send new ripostes by email.

Usage: python3 scripts/send_email.py added.md

added.md holds the entries added in a push ("### " blocks from _includes/latest.md).
Settings come from the environment (repository secrets): SMTP_HOST, SMTP_PORT,
SMTP_USER, SMTP_PASSWORD, RECIPIENTS (addresses separated by commas or new lines),
optional MAIL_FROM_NAME. TEST_TO, when set, replaces the recipient list.
Recipients go in Bcc only, so nobody sees the list.
"""
import os
import re
import smtplib
import sys
from email.message import EmailMessage
from email.utils import formataddr

import markdown

SITE = "https://ajoly35.github.io/riposte-economique/"
FORM = "https://github.com/ajoly35/riposte-economique/issues/new?template=riposte.yml"


def main(path):
    text = open(path, encoding="utf-8").read().strip()
    titles = re.findall(r"^### (.+)$", text, flags=re.M)
    if not titles:
        print("No new entry; nothing sent.")
        return

    test_to = os.environ.get("TEST_TO", "").strip()
    raw = test_to or os.environ.get("RECIPIENTS", "")
    recipients = [a.strip() for a in re.split(r"[,\n;]", raw) if a.strip()]
    if not recipients:
        print("No recipients set; nothing sent.")
        return

    user = os.environ["SMTP_USER"]
    sender_name = os.environ.get("MAIL_FROM_NAME", "").strip() or "Riposte économique"
    if len(titles) == 1:
        subject = f"Riposte économique : {titles[0]}"
    else:
        subject = f"Riposte économique : {len(titles)} nouvelles ripostes"

    footer_md = (
        f"Toutes les ripostes : [{SITE}]({SITE})  \n"
        f"Proposer une riposte : [formulaire]({FORM})"
    )
    readable = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", text)
    readable = re.sub(r"^### ", "", readable, flags=re.M).replace("**", "")
    readable = re.sub(r"^\*(.+)\*$", r"\1", readable, flags=re.M)
    plain = f"{readable}\n\n---\nToutes les ripostes : {SITE}\nProposer une riposte : {FORM}\n"
    body_html = markdown.markdown(text + "\n\n---\n\n" + footer_md)
    html = f"""<!doctype html><html lang="fr"><body style="margin:0;padding:0;background:#fbfaf7">
<div style="max-width:640px;margin:0 auto;padding:24px 16px;font:16px/1.6 Georgia,serif;color:#1f1d1a">
<style>h3{{font:600 17px/1.3 Helvetica,Arial,sans-serif;color:#7a2e1f;margin:28px 0 6px}} a{{color:#7a2e1f}} hr{{border:0;border-top:1px solid #e4e0d8;margin:28px 0 12px}}</style>
{body_html}
</div></body></html>"""

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr((sender_name, user))
    msg["To"] = formataddr((sender_name, user))
    msg.set_content(plain)
    msg.add_alternative(html, subtype="html")

    host = os.environ["SMTP_HOST"]
    port = int(os.environ.get("SMTP_PORT") or 587)
    if port == 465:
        server = smtplib.SMTP_SSL(host, port)
    else:
        server = smtplib.SMTP(host, port)
        server.starttls()
    with server:
        server.login(user, os.environ["SMTP_PASSWORD"])
        server.send_message(msg, from_addr=user, to_addrs=recipients)
    print(f"Sent \"{subject}\" to {len(recipients)} recipient(s).")


if __name__ == "__main__":
    main(sys.argv[1])
