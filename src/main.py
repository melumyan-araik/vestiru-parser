from vestiParser import VestiParser

def main():
    parser = VestiParser(isCreateDb=False, isCreateTable=True)
    parser.start() 

main()



