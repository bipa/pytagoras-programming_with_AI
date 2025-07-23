#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "python-dotenv",
#     "supabase"
# ]
# ///

import urllib.request
import urllib.error
import json
import sys
import os
import sqlite3
import time
import random
import gzip
import base64
from supabase import create_client, Client


def _compress_large_json(data, compression_threshold=100000):
    """Compress JSON data if it exceeds the threshold size.
    
    Args:
        data: The data to potentially compress (string, list, or dict)
        compression_threshold: Size in bytes above which to compress (default 100KB)
        
    Returns:
        tuple: (compressed_data_string, is_compressed_boolean)
    """
    if data is None:
        return None, False
    
    # Convert to JSON string if not already
    if isinstance(data, (list, dict)):
        json_str = json.dumps(data)
    elif isinstance(data, str):
        json_str = data
    else:
        json_str = str(data)
    
    # Check if compression is needed
    if len(json_str.encode('utf-8')) > compression_threshold:
        try:
            # Compress and encode as base64
            compressed = gzip.compress(json_str.encode('utf-8'))
            compressed_b64 = base64.b64encode(compressed).decode('utf-8')
            # Add a prefix to indicate this is compressed
            return f"GZIP_B64:{compressed_b64}", True
        except Exception as e:
            print(f"Warning: Failed to compress large JSON data: {e}", file=sys.stderr)
            # Fall back to original data
            return json_str, False
    
    return json_str, False


def _decompress_json(data):
    """Decompress JSON data if it was compressed.
    
    Args:
        data: The data string that might be compressed
        
    Returns:
        The decompressed data (as string) or original data if not compressed
    """
    if data is None or not isinstance(data, str):
        return data
    
    # Check if data is compressed
    if data.startswith("GZIP_B64:"):
        try:
            # Remove prefix and decode
            compressed_b64 = data[9:]  # Remove "GZIP_B64:" prefix
            compressed = base64.b64decode(compressed_b64.encode('utf-8'))
            decompressed = gzip.decompress(compressed).decode('utf-8')
            return decompressed
        except Exception as e:
            print(f"Warning: Failed to decompress data: {e}", file=sys.stderr)
            # Return original data if decompression fails
            return data
    
    return data


def _prepare_event_record(event_data):
    """Extract and prepare event data fields with defaults for optional fields."""
    return {
        'source_app': event_data.get('source_app', ''),
        'type': event_data.get('type', 'feature'),
        'feature_name': event_data.get('feature_name', ''),
        'feature_number': event_data.get('feature_number', ""),
        'user': event_data.get('user', ''),
        'session_id': event_data.get('session_id', ''),
        'hook_event_type': event_data.get('hook_event_type', ''),
        'timestamp': event_data.get('timestamp', 0),
        'chat': event_data.get('chat', None),
        'summary': event_data.get('summary', None),
        'payload': event_data.get('payload', {})
    }


def send_event_to_server(event_data, server_url='http://localhost:4000/events'):
    """Send event data to the observability server."""
    try:
        # Prepare the request
        req = urllib.request.Request(
            server_url,
            data=json.dumps(event_data).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Claude-Code-Hook/1.0'
            }
        )
        
        # Send the request
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                return True
            else:
                print(f"Server returned status: {response.status}", file=sys.stderr)
                return False
                
    except urllib.error.URLError as e:
        print(f"Failed to send event: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return False
    

def send_event_to_file(event_data, file_path):
    """Append the event_data to the end of a log json file."""
    try:        
        # Check if file exists and has content
        if file_path.exists() and file_path.stat().st_size > 0:
            try:
                # Read existing data
                existing_data = json.loads(file_path.read_text(encoding="utf-8"))
                if isinstance(existing_data, list):
                    # Append new event
                    existing_data.append(event_data)
                    file_path.write_text(json.dumps(existing_data, indent=2), encoding="utf-8")
                else:
                    # Not a list, overwrite with new list
                    file_path.write_text(json.dumps([event_data], indent=2), encoding="utf-8")
            except json.JSONDecodeError:
                # Invalid JSON, overwrite with new list
                file_path.write_text(json.dumps([event_data], indent=2), encoding="utf-8")
        else:
            # File doesn't exist or is empty, create new list
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(json.dumps([event_data], indent=2), encoding="utf-8")
        return True
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return False
    
    
def send_event_to_sqllite_database(event_data, path_to_db, max_retries=5):
    """Send event data to the observability database with retry logic for concurrent access."""
    
    # Check if the database file exists and create the directory if needed
    db_dir = os.path.dirname(path_to_db)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    for attempt in range(max_retries):
        conn = None
        try:
            # Connect with timeout and enable WAL mode for better concurrency
            conn = sqlite3.connect(path_to_db, timeout=10.0)
            cursor = conn.cursor()
            
            # Enable WAL mode for better concurrent write support
            cursor.execute("PRAGMA journal_mode=WAL;")
            
            # Create the table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS features (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT,
                    source_app TEXT,
                    feature_name TEXT,
                    feature_number TEXT,
                    user TEXT,
                    session_id TEXT,
                    hook_event_type TEXT,
                    timestamp INTEGER,
                    chat TEXT,
                    summary TEXT,
                    payload JSON
                )
            ''')

            # Prepare the record using the common helper
            record = _prepare_event_record(event_data)
            
            # Convert payload to JSON string for SQLite storage
            record['payload'] = json.dumps(record['payload'])
            
            # Handle chat field with compression for large data
            if record['chat'] is not None:
                compressed_chat, was_compressed = _compress_large_json(record['chat'])
                record['chat'] = compressed_chat
                if was_compressed:
                    print(f"Compressed large chat data to save space", file=sys.stderr)

            # Use UPSERT (INSERT OR REPLACE) to handle duplicate entries
            # We'll consider a record duplicate if it has the same session_id, hook_event_type, and timestamp
            cursor.execute('''
                INSERT OR REPLACE INTO features 
                (type, source_app, feature_name, feature_number, user, session_id, hook_event_type, 
                timestamp, chat, summary, payload) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                record['type'],
                record['source_app'],
                record['feature_name'],
                record['feature_number'],
                record['user'],
                record['session_id'],
                record['hook_event_type'],
                record['timestamp'],
                record['chat'],
                record['summary'],
                record['payload']
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.OperationalError as e:
            if conn:
                try:
                    conn.rollback()
                    conn.close()
                except:
                    pass
            
            # Handle database busy/locked errors with retry
            if "database is locked" in str(e).lower() or "database is busy" in str(e).lower():
                if attempt < max_retries - 1:
                    # Exponential backoff with jitter
                    wait_time = (2 ** attempt) * 0.1 + random.uniform(0, 0.1)
                    print(f"Database busy, retrying in {wait_time:.2f}s (attempt {attempt + 1}/{max_retries})", file=sys.stderr)
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"Database busy after {max_retries} attempts: {e}", file=sys.stderr)
                    return False
            else:
                print(f"SQLite operational error: {e}", file=sys.stderr)
                return False
                
        except json.JSONEncodeError as e:
            if conn:
                try:
                    conn.rollback()
                    conn.close()
                except:
                    pass
            print(f"JSON serialization error: {e}", file=sys.stderr)
            print(f"Failed to serialize chat or payload data", file=sys.stderr)
            return False
        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                    conn.close()
                except:
                    pass
            print(f"Unexpected database error: {e}", file=sys.stderr)
            return False
    
    return False


def send_event_to_supabase_database(event_data, supabase_url, supabase_key, table_name='features'):
    """Send event data to the Supabase database."""
    try:
        # Create Supabase client
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # Prepare the record using the common helper
        record = _prepare_event_record(event_data)
        
        # Insert the record into the database
        result = supabase.table(table_name).insert(record).execute()
        
        # Check if the insert was successful
        if result.data:
            return True
        else:
            print(f"Failed to insert record: {result}", file=sys.stderr)
            return False
            
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return False
    