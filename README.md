# GitHub Action Send Job Status Notification


Purpose: send notifications on job status, initially via Slack.

## Inputs
### `job-status`

**Required** Job status.

### `slack-token`

**Required** Slack token used to send message.

### `channel-id`

**Required** Slack channel id.


## Outputs
There are no outputs.

## Example usage
```yaml
  build-dev:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Send notification
        if: always()
        uses: shiftgig/action-notify-status@v1
        with:
          job-status: ${{ job.status }}
          slack-token: ${{ secrets.SLACK_TOKEN }}
          channel-id: CXXX000
```


## Slack Setup
You will need a Slack app, [follow these steps](https://api.slack.com/start/overview#creating).
