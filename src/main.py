from vestiParser import VestiParser

def main():
    parser = VestiParser(isCreateDb=True, isCreateTable=True)
    parser.start() 

main()



