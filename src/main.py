#!/usr/bin/env python

import argparse
from Comic_Scraper.app import Comic


# Get command line args
def get_args():
    parser = argparse.ArgumentParser(description='Downloads comic from xoxocomics.com')
    parser.add_argument("comic", type=str, help="The name of the comic")
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    comic = Comic(args.comic)
    comic.get_issue_links()
    path = comic.get_directory()
    comic.create_issues()
    comic.download_issues(path)
    return


if __name__ == "__main__":
    main()
