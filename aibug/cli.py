"""
Command Line Interface for AIBugReport
"""

import argparse
import sys
from . import __version__


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
    
    if args.command == "report":
        print("Feature not yet implemented: Submitting a bug report")
        print(f"Would submit report with title: {args.title}")
        print(f"Description: {args.description}")
        if args.project:
            print(f"Project: {args.project}")
        if args.attach:
            print(f"Attachments: {args.attach}")
            
    elif args.command == "list":
        print("Feature not yet implemented: Listing bug reports")
        if args.project:
            print(f"Would filter by project: {args.project}")
        if args.status:
            print(f"Would filter by status: {args.status}")
            
    elif args.command == "view":
        print("Feature not yet implemented: Viewing bug report details")
        print(f"Would view bug report with ID: {args.id}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())