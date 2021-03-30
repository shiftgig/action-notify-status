import os
from datetime import datetime, timezone
from typing import Dict

import click
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class Config:
    @property
    def repository(self) -> str:
        return os.getenv("GITHUB_REPOSITORY")

    @property
    def actor(self) -> str:
        return os.getenv("GITHUB_ACTOR")

    @property
    def run_id(self) -> str:
        return os.getenv("GITHUB_RUN_ID")

    @property
    def workflow(self) -> str:
        return os.getenv("GITHUB_WORKFLOW")

    @property
    def job_id(self) -> str:
        return os.getenv("GITHUB_JOB")

    @property
    def ref(self) -> str:
        return os.getenv("GITHUB_REF", "")

    @property
    def branch(self) -> str:
        try:
            return self.ref.split("/", 2)[2]
        except IndexError:
            return "unknown branch"


config = Config()


def build_status_block(
    job_status: str, actor: str, flow: str, branch: str, run_id: str, repository: str
) -> Dict:
    if job_status.lower() == "success":
        message = ":white_check_mark: *Success*"
    elif job_status.lower() == "cancelled":
        message = ":large_blue_circle: *Cancelled*"
    else:
        message = ":x: *Failed*"

    message = (
        message
        + f" *{repository}* <https://github.com/{repository}/actions/runs/{run_id}|View Job>\n"
        + f"[ {flow} ] [ {branch} ]\n"
    )
    message = message + f"Triggered by {actor}"
    return {"type": "section", "text": {"type": "mrkdwn", "text": message}}


@click.command(context_settings=dict(ignore_unknown_options=True))
@click.option("--token", required=True, help="Slack token")
@click.option("--channel", required=True, help="Channel id")
@click.option("--job-status", required=True, help="Job status")
def send_to_slack(token: str, channel: str, job_status: str):
    client = WebClient(token=token)

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": datetime.now(tz=timezone.utc).strftime(
                    "%a %b %d %Y %H:%M:%S %Z"
                ),
            },
        },
        build_status_block(
            job_status,
            config.actor,
            config.job_id,
            config.branch,
            config.run_id,
            config.repository,
        ),
    ]

    try:
        result = client.chat_postMessage(
            channel=channel, text="Some text", blocks=blocks
        )
        # Print result, which includes information about the message (like TS)
        print(result)

    except SlackApiError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    send_to_slack()
