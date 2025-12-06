
import argparse
import requests
import json
from datetime import datetime
import sys
from contextlib import contextmanager
import csv

@contextmanager
def smart_open(filename=None):
    if filename and filename != '-':
        fh = open(filename, 'w')
    else:
        fh = sys.stdout

    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()

def output_json(response, fh):
    response.raise_for_status()
    fh.write(json.dumps(response.json(), indent=2))

def output_csv(response, fh, request_payload):
    response.raise_for_status()
    request_id = request_payload.get('id')

    data = response.json()
    artifact = data["result"]["artifacts"][0]
    text = "".join(part["text"] for part in artifact["parts"])

    writer = csv.writer(fh)
    writer.writerow([request_id, text])

def process_response(response, fh, out_format, request_payload=None):
    if out_format == 'json':
        output_json(response, fh)
    elif out_format == 'csv':
        if request_payload:
            output_csv(response, fh, request_payload)
        else:
            # For card requests, CSV output might not be applicable or needs a different format
            # For now, we'll just output a simple message
            writer = csv.writer(fh)
            writer.writerow(["card_request", "success"])

def handle_card_request(url, fh, out_format='json'):
    card_suffix = ".well-known/agent-card.json"
    if not url.endswith(card_suffix):
        if not url.endswith("/"):
            url += "/"
        url += card_suffix
    response = requests.get(url)
    process_response(response, fh, out_format)

def handle_prompt_request(url, prompt, task=None, context=None, message=None, fh=sys.stdout, out_format='json'):
    if message:
        message_id = message
    else:
        message_id = datetime.now().isoformat()
    message = {
        "role": "user",
        "messageId": message_id,
        "parts": [
            {
                "kind": "text",
                "text": prompt,
            }
        ],
    }
    if task:
        message["taskId"] = task
    if context:
        message["contextId"] = context

    payload = {
        "jsonrpc": "2.0",
        "id": message_id,
        "method": "message/send",
        "params": {
            "message": message
        }
    }
    response = requests.post(url, json=payload)
    process_response(response, fh, out_format, payload)

def handle_infile(infile, fh, out_format='csv'):
    input_stream = open(infile, 'r') if infile != '-' else sys.stdin
    reader = csv.reader(input_stream)
    for row in reader:
        url, prompt, message, task, context = row
        handle_prompt_request(url, prompt, task or None, context or None, message or None, fh, out_format)
    if input_stream is not sys.stdin:
        input_stream.close()

def main():
    parser = argparse.ArgumentParser(description='Make a request using A2A to an agent.')
    parser.add_argument('--url', type=str, help='The base URL for the agent')
    parser.add_argument('--card', action='store_true', help='Get the agent card.')
    parser.add_argument('--prompt', type=str, help='The prompt to send.')
    parser.add_argument('--task', type=str, help='An optional task id.')
    parser.add_argument('--context', type=str, help='An optional context id.')
    parser.add_argument('--message', type=str, help='An optional message id.')
    parser.add_argument('--out', type=str, help='The output file, or - for stdout.')
    parser.add_argument('--in', dest='infile', type=str, help='A CSV file to process, or - for stdin.')
    parser.add_argument('--format', choices=['json', 'csv'], default='json', help='The output format.')

    args = parser.parse_args()

    url = args.url
    card = args.card
    prompt = args.prompt
    task = args.task
    context = args.context
    message = args.message
    out = args.out
    infile = args.infile
    out_format = args.format

    num_args = sum([1 for arg in [infile, card, prompt] if arg])
    if num_args > 1:
        parser.error("Only one of --in, --card, or --prompt can be specified.")

    if (card or prompt) and not url:
        parser.error("--url is required when using --card or --prompt.")

    with smart_open(out) as fh:
        try:
            if infile:
                handle_infile(infile, fh, out_format)
            elif card:
                handle_card_request(url, fh, out_format)
            elif prompt:
                handle_prompt_request(url, prompt, task, context, message, fh, out_format)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
