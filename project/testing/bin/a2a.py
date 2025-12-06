import argparse
import requests
import json
from datetime import datetime
import sys
from contextlib import contextmanager, ExitStack
import csv

@contextmanager
def output_manager(out, formats):
    handles = {}
    stack = ExitStack()
    try:
        if not out or out == '-':
            for fmt in formats:
                handles[fmt] = sys.stdout
        else:
            if len(formats) == 1:
                handles[formats[0]] = stack.enter_context(open(out, 'w'))
            else:
                for fmt in formats:
                    handles[fmt] = stack.enter_context(open(f"{out}.{fmt}", 'w'))
        yield handles
    finally:
        stack.close()

def output_json(response, fh):
    response.raise_for_status()
    fh.write(json.dumps(response.json()) + '\n')
    fh.flush()

def output_csv(response, fh, request_payload):
    response.raise_for_status()
    request_id = request_payload.get('id')

    data = response.json()
    try:
        artifact = data["result"]["artifacts"][0]
        text = "".join(part["text"] for part in artifact["parts"])
        
        writer = csv.writer(fh)
        writer.writerow([request_id, text])
    except (KeyError, IndexError, TypeError):
        writer = csv.writer(fh)
        writer.writerow([request_id, "Error: Unexpected response format"])
    fh.flush()

def output_txt(response, fh, request_payload):
    response.raise_for_status()
    data = response.json()
    
    prompt_text = "N/A"
    if request_payload and "params" in request_payload and "message" in request_payload["params"] and \
       "parts" in request_payload["params"]["message"] and len(request_payload["params"]["message"]["parts"]) > 0 and \
       "text" in request_payload["params"]["message"]["parts"][0]:
        prompt_text = request_payload["params"]["message"]["parts"][0]["text"]

    output_text = ""
    try:
        if "result" in data and "artifacts" in data["result"] and len(data["result"]["artifacts"]) > 0:
            artifact = data["result"]["artifacts"][0]
            output_text = "".join(part["text"] for part in artifact["parts"])
        else:
            output_text = str(data) # Fallback for other responses or errors
    except Exception as e:
        output_text = f"Error parsing response: {str(e)}"

    fh.write(f"Prompt:\n {prompt_text}\n")
    fh.write("\n")
    fh.write(f"Response:\n {output_text}\n")
    fh.write("\n")
    fh.flush()

def process_response(response, handles, request_payload=None):
    for fmt, fh in handles.items():
        if fmt == 'json':
            output_json(response, fh)
        elif fmt == 'csv':
            if request_payload:
                output_csv(response, fh, request_payload)
            else:
                # For card requests, CSV output might not be applicable or needs a different format
                # For now, we'll just output a simple message. This should not happen for card requests with prompt, as request_payload will be None
                writer = csv.writer(fh)
                writer.writerow(["card_request", "success"])
        elif fmt == 'txt':
            output_txt(response, fh, request_payload)

def handle_card_request(url, handles):
    card_suffix = ".well-known/agent-card.json"
    if not url.endswith(card_suffix):
        if not url.endswith("/"):
            url += "/"
        url += card_suffix
    response = requests.get(url)
    process_response(response, handles)

def handle_prompt_request(url, prompt, task=None, context=None, message=None, handles={}):
    if message:
        message_id = message
    else:
        message_id = datetime.now().isoformat()

    print(f"Running test with message ID: {message_id}", file=sys.stderr)

    message_data = {
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
        message_data["taskId"] = task
    if context:
        message_data["contextId"] = context

    payload = {
        "jsonrpc": "2.0",
        "id": message_id,
        "method": "message/send",
        "params": {
            "message": message_data
        }
    }
    response = requests.post(url, json=payload)
    process_response(response, handles, payload)

def handle_infile(infile, handles):
    input_stream = open(infile, 'r') if infile != '-' else sys.stdin
    reader = csv.reader(input_stream)
    
    last_thread_key = None

    for row in reader:
        if len(row) >= 2:
            url, prompt = row[0], row[1]
            message = row[2] if len(row) > 2 else None
            task = row[3] if len(row) > 3 else None
            context = row[4] if len(row) > 4 else None
            
            # Logic for Thread Header
            if 'txt' in handles:
                current_thread_key = (url, context)
                if current_thread_key != last_thread_key:
                    fh = handles['txt']
                    fh.write("\n" + "=" * 40 + "\n")
                    fh.write(f"Thread ID: {context}\n")
                    fh.write(f"URL: {url}\n")
                    fh.write("=" * 40 + "\n\n")
                    last_thread_key = current_thread_key
                else:
                    fh.write("-" * 5 + "\n\n")

            handle_prompt_request(url, prompt, task or None, context or None, message or None, handles)
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
    parser.add_argument('--format', nargs='+', choices=['json', 'csv', 'txt'], help='The output format(s).')

    args = parser.parse_args()

    url = args.url
    card = args.card
    prompt = args.prompt
    task = args.task
    context = args.context
    message = args.message
    out = args.out
    infile = args.infile
    
    # Logic for format defaulting
    if args.format:
        out_formats = args.format
    elif out and out != '-':
        out_formats = ['json', 'csv', 'txt']
    else:
        out_formats = ['json']

    num_args = sum([1 for arg in [infile, card, prompt] if arg])
    if num_args > 1:
        parser.error("Only one of --in, --card, or --prompt can be specified.")

    if (card or prompt) and not url:
        parser.error("--url is required when using --card or --prompt.")

    with output_manager(out, out_formats) as handles:
        try:
            if infile:
                handle_infile(infile, handles)
            elif card:
                handle_card_request(url, handles)
            elif prompt:
                handle_prompt_request(url, prompt, task, context, message, handles)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
