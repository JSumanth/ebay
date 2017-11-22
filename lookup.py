import json
import requests
import click

import cmd
import sys

from click import UsageError

API_ENDPOINT = 'http://svcs.ebay.com/services/search/FindingService/v1'


class FindItemByProduct(object):
    def __init__(self, upc_code):
        self.params = {
            'OPERATION-NAME': 'findItemsByProduct',
            'SERVICE-VERSION': '1.0.0',
            'SECURITY-APPNAME': 'sumanthj-sampleap-PRD-9134e8f72-7dfa9fa2',
            'RESPONSE-DATA-FORMAT': 'JSON',
            'productId.@type': 'UPC',
            'productId': upc_code
        }

    def Display(self):
        r = requests.get(API_ENDPOINT, params=self.params)
        print "Getting details from Ebay"
        if r.status_code == 200:
            print "Here are the results:"
            try:
                for i in json.loads(r.text)['findItemsByProductResponse'][0]['searchResult']:
                    for j in i.get('item'):
                        text = """
                                Title : {}
                                Price : {} {}
                        """.format(j['title'][0].encode('utf-8').strip(),
                                   j['sellingStatus'][0]['currentPrice'][0]['@currencyId'],
                                   j['sellingStatus'][0]['currentPrice'][0]['__value__'])
                        print text
            except:
                dict_obj = json.loads(r.text)['findItemsByProductResponse'][0]['errorMessage'][0]['error'][0]
                print "{} for {}".format(dict_obj['message'][0], dict_obj['parameter'][0])
        else:
            print "Unable to get the details"


class REPL(cmd.Cmd):
    def __init__(self, ctx):
        cmd.Cmd.__init__(self)
        self.ctx = ctx

    def default(self, line):
        subcommand = line.split()[0]
        args = line.split()[1:]

        subcommand = cli.commands.get(subcommand)
        if subcommand:
            try:
                subcommand.parse_args(self.ctx, args)
                self.ctx.forward(subcommand)
            except UsageError as e:
                print(e.format_message())
        else:
            return cmd.Cmd.default(self, line)


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        repl = REPL(ctx)
        repl.cmdloop()


@cli.command()
@click.option('--upc', required=True, help="enter Universal Product Code (UPC)")
def search(upc):
    print("searching for upc")
    obj = FindItemByProduct(upc)
    obj.Display()


@cli.command()
def exit(upc):
    print("exiting it form shell")
    sys.exit(1)


if __name__ == "__main__":
    print("Welcome to Ebay Product Search")
    details = """
       Commands:
         search:
               usage example: search --upc [number]

         exit: exit it from the command prompt    
    """
    print(details)
    cli()