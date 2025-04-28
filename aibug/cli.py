"""
Command Line Interface for AIBugReport
"""

import argparse
import sys
import os
from . import __version__
from .db import (
    initialize_database,
    get_or_create_project,
    insert_bug_report,
    list_bug_reports,
    get_bug_report,
    insert_attachment,
)
from .llm import LLMClient
from .pinata_client import PinataClient


def create_parser():
    """Create the command line parser."""
    parser = argparse.ArgumentParser(
        description="AIBugReport: Intelligent Bug Tracking CLI",
        prog="aibug"
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Report command
    report_parser = subparsers.add_parser("report", help="Submit a new bug report")
    report_parser.add_argument("--title", required=True, help="Title of the bug report")
    report_parser.add_argument("--description", required=True, help="Detailed description of the bug")
    report_parser.add_argument("--project", help="Project to associate the bug with")
    report_parser.add_argument("--attach", nargs="+", help="Path(s) to file(s) to attach")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List bug reports")
    list_parser.add_argument("--project", help="Filter by project")
    list_parser.add_argument("--status", help="Filter by status")
    
    # View command
    view_parser = subparsers.add_parser("view", help="View details of a bug report")
    view_parser.add_argument("id", help="ID of the bug report to view")
    
    return parser


def main():
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    # Ensure database tables exist
    try:
        initialize_database()
    except Exception as e:
        print(f"Database initialization error: {e}", file=sys.stderr)
        return 1
    
    if args.command == "report":
        # Handle project creation or lookup
        project_id = None
        if args.project:
            try:
                project_id = get_or_create_project(args.project)
            except Exception as e:
                print(f"Error creating/fetching project: {e}", file=sys.stderr)
                return 1
        # LLM suggestions
        category = None
        severity = None
        try:
            llm_client = LLMClient()
            suggestions = llm_client.suggest(args.description)
            category = suggestions.get("category")
            severity = suggestions.get("severity")
        except Exception as e:
            print(f"LLM suggestion warning: {e}", file=sys.stderr)
        # Insert bug report
        try:
            bug_id = insert_bug_report(
                args.title, args.description, category, severity, project_id
            )
        except Exception as e:
            print(f"Error inserting bug report: {e}", file=sys.stderr)
            return 1
        print(f"Bug report created with ID: {bug_id}")
        if category or severity:
            print("Suggestions:")
            if category:
                print(f"  Category: {category}")
            if severity:
                print(f"  Severity: {severity}")
        # Upload attachments
        if args.attach:
            try:
                pinata = PinataClient()
            except Exception as e:
                print(f"Pinata client error: {e}", file=sys.stderr)
                return 1
            for path in args.attach:
                if not os.path.isfile(path):
                    print(f"Attachment not found: {path}", file=sys.stderr)
                    continue
                try:
                    upload = pinata.upload_file(path)
                    insert_attachment(
                        bug_id,
                        upload["file_name"],
                        upload["ipfs_hash"],
                        upload["url"]
                    )
                    print(f"Uploaded attachment '{upload['file_name']}' to {upload['url']}")
                except Exception as e:
                    print(f"Error uploading attachment {path}: {e}", file=sys.stderr)
        return 0
            
    elif args.command == "list":
        try:
            reports = list_bug_reports(project=args.project, status=args.status)
        except Exception as e:
            print(f"Error listing bug reports: {e}", file=sys.stderr)
            return 1
        if not reports:
            print("No bug reports found.")
        else:
            # Table header
            print(
                f"{'ID':<5} {'Title':<30} {'Project':<20} {'Severity':<10} {'Category':<15} {'Status':<10} {'Created':<20}"
            )
            for r in reports:
                print(
                    f"{r['id']:<5} {r['title'][:29]:<30} {r.get('project') or '':<20} "
                    f"{r.get('severity') or '':<10} {r.get('category') or '':<15} {r.get('status') or '':<10} "
                    f"{r.get('created_at')}"
                )
        return 0
            
    elif args.command == "view":
        try:
            bug = get_bug_report(args.id)
        except Exception as e:
            print(f"Error fetching bug report: {e}", file=sys.stderr)
            return 1
        if not bug:
            print(f"Bug report with ID {args.id} not found.", file=sys.stderr)
            return 1
        # Display details
        print(f"ID: {bug['id']}")
        print(f"Title: {bug['title']}")
        print(f"Description: {bug['description']}")
        print(f"Category: {bug.get('category') or ''}")
        print(f"Severity: {bug.get('severity') or ''}")
        print(f"Status: {bug.get('status') or ''}")
        print(f"Project: {bug.get('project') or ''}")
        print(f"Created At: {bug.get('created_at')}")
        attachments = bug.get('attachments') or []
        if attachments:
            print("Attachments:")
            for a in attachments:
                print(f"  {a['file_name']}: {a['url']}")
        return 0
    
    return 0


if __name__ == "__main__":
    sys.exit(main())