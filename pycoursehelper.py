import argparse
from oauth2client import tools
from command.gdrive import GDriveCommand


if __name__ == '__main__':
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    subparsers = parser.add_subparsers(dest='sub_command')

    driver_parser = subparsers.add_parser('gdrive', help='gdrive --help')
    driver_sub_parsers = driver_parser.add_subparsers(dest='gdrive')

    initialize_parser = driver_sub_parsers.add_parser('initialize', help='initialize --help')
    initialize_parser.add_argument('-y', '--year', help='Year of python course')
    initialize_parser.add_argument('-f', '--folder', help='Name of the folder to initialize')

    share_parser = driver_sub_parsers.add_parser('share', help='share --help')
    share_parser.add_argument('-f', '--file', help='CSV File which contains student details')
    share_parser.add_argument('-d', '--data', help='Details of student in CSV to create share folder')
    share_parser.add_argument('-y', '--year', help='Year of python course')
    share_parser.add_argument('-t', '--type',
                              help='Directory name under year folder to create share folders. Eg "class" or "mock1"')

    unshare_parser = driver_sub_parsers.add_parser('unshare', help='unshare --help')
    unshare_parser.add_argument('-f', '--file', help='CSV File which contains student details')
    unshare_parser.add_argument('-d', '--data', help='Details of student in CSV to create share folder')
    unshare_parser.add_argument('-y', '--year', help='Year of python course')
    unshare_parser.add_argument('-t', '--type',
                                help='Directory name under year folder to create share folders. Eg "class" or "mock1"')

    delete_parser = driver_sub_parsers.add_parser('delete', help='delte --help')
    delete_parser.add_argument('-f', '--file', help='CSV File which contains student details')
    delete_parser.add_argument('-d', '--data', help='Details of student in CSV to create share folder')
    delete_parser.add_argument('-a', '--all', action='store_true')
    delete_parser.add_argument('-y', '--year', help='Year of python course')
    delete_parser.add_argument('-t', '--type',
                               help='Directory name under year folder to create share folders. Eg "class" or "mock1"')

    args = parser.parse_args()

    if args.sub_command == 'gdrive':
        GDriveCommand(parser, args).parse_args()
    else:
        parser.error('Invalid sub command given')