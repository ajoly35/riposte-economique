# Riposte économique

Source of the page https://ajoly35.github.io/riposte-economique/ (GitHub Pages, Jekyll) and of the riposte emails.

| File | What it holds | Who edits it |
|---|---|---|
| `_includes/latest.md` | the ripostes, newest first | daily routine (or by hand) |
| `ROUTINE.md` | instructions the daily routine follows | by hand |
| `contributeurs.txt` | GitHub accounts whose submissions are processed | by hand |
| `scripts/send_email.py`, `.github/workflows/email.yml` | the email sent when ripostes are added | by hand |

## How it works
1. Every morning a scheduled Claude routine reads `ROUTINE.md`, processes submissions and recent rival claims, and adds every verified riposte it finds to `_includes/latest.md`.
2. Each push that adds entries runs `.github/workflows/email.yml`, which emails only the new entries, in Bcc, from the mailbox set in the secrets.
3. Submissions: https://github.com/ajoly35/riposte-economique/issues/new?template=riposte.yml (link, optional note). Only accounts in `contributeurs.txt` are processed. Opening a submission fires a second routine at once (GitHub event `issues.opened`), which processes submissions only; it also sweeps them every Sunday at 17:00 UTC.

## Email setup (once)
Settings → Secrets and variables → Actions → New repository secret:

| Secret | Example |
|---|---|
| `SMTP_HOST` | `smtp.gmail.com` |
| `SMTP_PORT` | `587` (or `465`) |
| `SMTP_USER` | the sending address, e.g. a campaign Gmail |
| `SMTP_PASSWORD` | an app password for that address (Gmail: Google account → Security → 2-step verification → App passwords) |
| `MAIL_FROM_NAME` | optional, defaults to `Riposte économique` |
| `RECIPIENTS` | addresses separated by commas or new lines |

Test: Actions → Envoi des ripostes → Run workflow, with your own address in `test_to`. It sends every riposte on the page to that address only.

Adding or removing a recipient: edit the `RECIPIENTS` secret. Nothing is stored in the repository.
