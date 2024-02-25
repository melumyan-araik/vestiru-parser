from vestiParser import VestiParser

def main():
    parser = VestiParser(isCreateDb=False, isCreateTable=False)
    parser.start()

main()
