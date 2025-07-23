#!/usr/bin/env python3
"""
Test script for log_feature.py SQLite database functionality.

This script creates mock event data and tests the SQLite database operations
to help debug and verify the hook's database functionality.

USAGE:
    python3 log_feature_test.py

WHAT IT DOES:
    1. Creates realistic mock event data (UserPromptSubmit, PreToolUse, PostToolUse, etc.)
    2. Tests the send_event_to_sqllite_database() function from utils/logger.py
    3. Creates a temporary SQLite database to verify data insertion
    4. Shows formatted output of all database contents
    5. Provides interactive query mode if run from terminal

OUTPUT:
    - Detailed event data for each test case
    - Success/failure status for each database insertion
    - Complete database schema and contents
    - Database file path for manual inspection

The script simulates the exact data structures and function calls that the
log_feature.py hook uses when processing Claude Code events.
"""

import sys
import os
import json
import sqlite3
import tempfile
from datetime import datetime
from pathlib import Path

# Add the utils directory to the path so we can import the logger
sys.path.append(str(Path(__file__).parent.parent / "utils"))

from logger import send_event_to_sqllite_database


def create_mock_event_data():
    """Create realistic mock event data for testing."""
    
    # Base event data structure
    base_event = {
        'source_app': 'studyguide-template',
        'feature_name': 'language',
        'feature_number': 1,
        'user': 'test_user',
        'session_id': 'test-session-12345',
        'timestamp': int(datetime.now().timestamp() * 1000)
    }
    
    # Create different types of events
    events = []
    
    # 1. UserPromptSubmit event
    user_prompt_event = base_event.copy()
    user_prompt_event.update({
        'hook_event_type': 'UserPromptSubmit',
        'payload': {
            'session_id': 'test-session-12345',
            'transcript_path': '/tmp/test_transcript.jsonl',
            'hook_event_name': 'UserPromptSubmit',
            'prompt': 'echo test command for debugging'
        }
    })
    events.append(('UserPromptSubmit', user_prompt_event))
    
    # 2. PreToolUse event
    pre_tool_event = base_event.copy()
    pre_tool_event.update({
        'hook_event_type': 'PreToolUse',
        'payload': {
            'tool_name': 'bash',
            'tool_input': {'command': 'ls -la'},
            'session_id': 'test-session-12345'
        }
    })
    events.append(('PreToolUse', pre_tool_event))
    
    # 3. PostToolUse event
    post_tool_event = base_event.copy()
    post_tool_event.update({
        'hook_event_type': 'PostToolUse',
        'payload': {
            'tool_name': 'bash',
            'tool_input': {'command': 'ls -la'},
            'tool_output': 'total 16\ndrwxr-xr-x 4 user user 4096 Jul 19 10:30 .',
            'session_id': 'test-session-12345',
            'success': True
        }
    })
    events.append(('PostToolUse', post_tool_event))
    
    # 4. Event with chat transcript
    chat_event = base_event.copy()
    chat_event.update({
        'hook_event_type': 'UserPromptSubmit',
        'payload': {
            'session_id': 'test-session-12345',
            'prompt': 'Help me debug this SQLite issue'
        },
        'chat': [
            {'role': 'user', 'content': 'I need help with SQLite database'},
            {'role': 'assistant', 'content': 'I can help you with SQLite. What specific issue are you facing?'},
            {'role': 'user', 'content': 'The INSERT statements are not working properly'}
        ]
    })
    events.append(('UserPromptSubmit with Chat', chat_event))
    
    # 5. Event with AI summary
    summary_event = base_event.copy()
    summary_event.update({
        'hook_event_type': 'UserPromptSubmit',
        'payload': {
            'session_id': 'test-session-12345',
            'prompt': 'Create a new feature for user authentication'
        },
        'summary': 'User requested implementation of authentication feature with database integration'
    })
    events.append(('UserPromptSubmit with Summary', summary_event))
    
    return events


def print_event_data(name, event_data):
    """Pretty print event data for debugging."""
    print(f"\n{'='*60}")
    print(f"Event: {name}")
    print('='*60)
    print(json.dumps(event_data, indent=2))
    print('='*60)


def create_test_database():
    """Create a temporary test database."""
    # Create a temporary file for the database
    fd, db_path = tempfile.mkstemp(suffix='.sqlite', prefix='test_log_feature_')
    os.close(fd)  # Close the file descriptor, we just need the path
    return db_path


def query_database(db_path):
    """Query the database and return all events."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get table schema
        cursor.execute("PRAGMA table_info(features)")
        schema = cursor.fetchall()
        
        # Get all events
        cursor.execute("SELECT * FROM features ORDER BY timestamp")
        events = cursor.fetchall()
        
        conn.close()
        return schema, events
    except Exception as e:
        print(f"Error querying database: {e}")
        return None, None


def print_database_contents(db_path):
    """Print the contents of the database for debugging."""
    schema, events = query_database(db_path)
    
    if schema is None:
        print("Failed to read database contents")
        return
    
    print(f"\n{'='*80}")
    print("DATABASE SCHEMA")
    print('='*80)
    for column in schema:
        print(f"  {column[1]:<20} {column[2]:<15} {'PRIMARY KEY' if column[5] else ''}")
    
    print(f"\n{'='*80}")
    print("DATABASE CONTENTS")
    print('='*80)
    
    if not events:
        print("No events found in database")
        return
    
    # Column headers
    headers = [col[1] for col in schema]
    print(f"{'ID':<5} {'App':<15} {'Feature':<12} {'#':<3} {'User':<12} {'Event Type':<15} {'Timestamp':<15}")
    print('-' * 80)
    
    for event in events:
        event_id, type_field, source_app, feature_name, feature_number, user, session_id, hook_event_type, timestamp, chat, summary, payload = event
        
        # Convert timestamp back to readable format
        dt = datetime.fromtimestamp(timestamp / 1000)
        timestamp_str = dt.strftime('%H:%M:%S')
        
        print(f"{event_id:<5} {source_app:<15} {feature_name:<12} {feature_number:<3} {user:<12} {hook_event_type:<15} {timestamp_str:<15}")
        
        # Show payload summary
        try:
            payload_obj = json.loads(payload)
            if 'prompt' in payload_obj:
                prompt = payload_obj['prompt'][:50] + '...' if len(payload_obj['prompt']) > 50 else payload_obj['prompt']
                print(f"      Prompt: {prompt}")
        except:
            pass
        
        if chat:
            try:
                chat_obj = json.loads(chat) if isinstance(chat, str) else chat
                print(f"      Chat: {len(chat_obj)} messages")
            except:
                print(f"      Chat: present but invalid")
        
        if summary:
            print(f"      Summary: {summary}")
        
        print()


def test_database_operations():
    """Main test function that creates events and tests database operations."""
    print("Starting log_feature SQLite Database Test")
    print("="*60)
    
    # Create test database
    db_path = create_test_database()
    print(f"Created test database: {db_path}")
    
    # Generate mock events
    events = create_mock_event_data()
    print(f"Generated {len(events)} test events")
    
    # Test database operations
    success_count = 0
    
    for event_name, event_data in events:
        print(f"\nTesting event: {event_name}")
        print_event_data(event_name, event_data)
        
        # Ensure chat field is JSON serialized if it's a list
        if 'chat' in event_data and isinstance(event_data['chat'], list):
            event_data['chat'] = json.dumps(event_data['chat'])
        
        # Test the database function
        success = send_event_to_sqllite_database(event_data, db_path)
        if success:
            print(f" Successfully inserted {event_name}")
            success_count += 1
        else:
            print(f"L Failed to insert {event_name}")
    
    print(f"\n{'='*60}")
    print(f"RESULTS: {success_count}/{len(events)} events inserted successfully")
    
    # Show database contents
    print_database_contents(db_path)
    
    print(f"\n{'='*60}")
    print("TEST COMPLETED")
    print(f"Test database saved at: {db_path}")
    print("You can inspect it manually with: sqlite3", db_path)
    print("="*60)
    
    return db_path


def interactive_query(db_path):
    """Interactive mode for querying the database."""
    print(f"\nInteractive Database Query Mode")
    print(f"Database: {db_path}")
    print("Available commands:")
    print("  count    - Show total number of events")
    print("  recent   - Show 5 most recent events")
    print("  types    - Show unique event types")
    print("  users    - Show unique users")
    print("  sessions - Show unique session IDs")
    print("  sql      - Execute custom SQL query")
    print("  quit     - Exit interactive mode")
    
    while True:
        try:
            command = input("\n> ").strip().lower()
            
            if command == 'quit':
                break
            elif command == 'count':
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM features")
                count = cursor.fetchone()[0]
                print(f"Total events: {count}")
                conn.close()
                
            elif command == 'recent':
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT hook_event_type, user, timestamp FROM features ORDER BY timestamp DESC LIMIT 5")
                events = cursor.fetchall()
                print("Recent events:")
                for event_type, user, timestamp in events:
                    dt = datetime.fromtimestamp(timestamp / 1000)
                    print(f"  {event_type} by {user} at {dt.strftime('%Y-%m-%d %H:%M:%S')}")
                conn.close()
                
            elif command == 'types':
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT hook_event_type, COUNT(*) FROM features GROUP BY hook_event_type")
                types = cursor.fetchall()
                print("Event types:")
                for event_type, count in types:
                    print(f"  {event_type}: {count}")
                conn.close()
                
            elif command == 'users':
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT user, COUNT(*) FROM features GROUP BY user")
                users = cursor.fetchall()
                print("Users:")
                for user, count in users:
                    print(f"  {user}: {count}")
                conn.close()
                
            elif command == 'sessions':
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT session_id, COUNT(*) FROM features GROUP BY session_id")
                sessions = cursor.fetchall()
                print("Sessions:")
                for session_id, count in sessions:
                    print(f"  {session_id}: {count}")
                conn.close()
                
            elif command == 'sql':
                sql_query = input("Enter SQL query: ").strip()
                try:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute(sql_query)
                    if sql_query.upper().startswith('SELECT'):
                        results = cursor.fetchall()
                        for row in results:
                            print(row)
                    else:
                        print(f"Query executed, {cursor.rowcount} rows affected")
                    conn.close()
                except Exception as e:
                    print(f"SQL Error: {e}")
                    
            else:
                print("Unknown command. Type 'quit' to exit.")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    import sys
    
    # Run the main test
    db_path = test_database_operations()
    
    # Check if running in interactive mode (terminal)
    if sys.stdin.isatty():
        # Ask if user wants interactive mode
        print(f"\nWould you like to enter interactive query mode? (y/n): ", end="")
        try:
            response = input().strip().lower()
            if response in ['y', 'yes']:
                interactive_query(db_path)
        except (EOFError, KeyboardInterrupt):
            print("\nSkipping interactive mode...")
    else:
        print("\nNon-interactive mode detected, skipping interactive query mode.")
    
    print(f"\nDatabase file: {db_path}")
    print("Test completed!")