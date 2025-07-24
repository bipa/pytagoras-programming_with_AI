#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "openai",
#     "python-dotenv",
#     "supabase"
# ]
# ///

"""
Multi-Agent Observability Hook Script
Sends Claude Code hook events to the observability server.
"""

import json
import sys
import os
import argparse
from datetime import datetime
from dotenv import load_dotenv
from utils.summarizer import generate_event_summary
from utils.logger import (
    send_event_to_sqllite_database,
    send_event_to_file,
    send_event_to_server,
)

from utils.data_manager import (
    repo_root,
    current_branch,
    current_user,
    repo_folder_name,
    extract_feature_name,
    extract_feature_number,
    find_feature_log_path,
)








def main():
    # Check if logging is enabled from .env
    load_dotenv()
    
    
    # Check if logging is enabled from environment variable
    # First try to load .env file from the hooks folder
    hooks_env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(hooks_env_path):
        load_dotenv(dotenv_path=hooks_env_path)
    
    if os.environ.get("LOG_ENABLED", "true").lower() == "false":
        return
    
    # Parse command line arguments
    # Check if this event is a feature event
    log_path = find_feature_log_path()
    if not log_path:                                   # no matching folder → done
        return
    
    parser = argparse.ArgumentParser(description='Send Claude Code hook events to observability server')
    parser.add_argument('--source-app', default=repo_folder_name(), help='Source application name')
    parser.add_argument('--event-type', required=True, help='Hook event type (PreToolUse, PostToolUse, etc.)')
    parser.add_argument('--server-url', default='http://localhost:4000/events', help='Server URL')
    parser.add_argument('--add-chat', action='store_true', help='Include chat transcript if available')
    parser.add_argument('--summarize', action='store_true', help='Generate AI summary of the event')
    
    if True:
        args = parser.parse_args()
    else:
        class MockArgs:
            def __init__(self):
                self.source_app = repo_folder_name()
                self.event_type = "TestEvent"
                self.server_url = "http://localhost:4000/events"
                self.add_chat = False
                self.summarize = True

        args = MockArgs()
        input_data = {
            "session_id": "test-session-id",
            "transcript_path": "/tmp/test_transcript.jsonl",
            "hook_event_name": "TestEvent",
            "payload": {"test": "data", "summary": "test summary"}
        }
        
        # print(f"Error parsing arguments: {e}", file=sys.stderr)
        # sys.exit(1)
    if True:
        try:
            # Read hook data from stdin
            input_data = json.load(sys.stdin)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON input: {e}", file=sys.stderr)
            sys.exit(1)
    
    # Prepare event data for server
    event_data = {
        'source_app': args.source_app,
        'type': 'feature',
        'feature_name': extract_feature_name(current_branch()),
        'feature_number': extract_feature_number(current_branch()),
        'user': current_user(),
        'session_id': input_data.get('session_id', 'unknown'),
        'hook_event_type': args.event_type,
        'payload': input_data,
        'timestamp': int(datetime.now().timestamp() * 1000)
    }
    
    # Handle --add-chat option
    if args.add_chat and 'transcript_path' in input_data:
        transcript_path = input_data['transcript_path']
        if os.path.exists(transcript_path):
            # Read .jsonl file and convert to JSON array
            chat_data = []
            try:
                with open(transcript_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                chat_data.append(json.loads(line))
                            except json.JSONDecodeError:
                                pass  # Skip invalid lines
                
                # Add chat to event data
                event_data['chat'] = chat_data
            except Exception as e:
                print(f"Failed to read transcript: {e}", file=sys.stderr)
    
    # Generate summary if requested
    if args.summarize:
        summary = generate_event_summary(event_data)
        if summary:
            event_data['summary'] = summary
        # Continue even if summary generation fails
    
    # Send to database
    success = send_event_to_sqllite_database(event_data, "./planning/dashboard/log.sqlite")
    
    if not success:
        print(f"Failed to send event to database: {event_data}", file=sys.stderr)
    
    send_event_to_file(event_data, log_path)
    
    # Always exit with 0 to not block Claude Code operations
    sys.exit(0)

if __name__ == '__main__':
    main()