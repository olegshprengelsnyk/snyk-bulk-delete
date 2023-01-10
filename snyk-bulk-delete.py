import sys, getopt, os, snyk
from yaspin import yaspin
from helperFunctions import *

helpString ='''--help/-h : Returns this page \n--orgs/-o : A set of orgs upon which to perform delete (use * for all orgs)\n--scatypes : Defines SCA type/s of projects to deletes \n--products : Defines product/s types of projects to delete \n* Please replace spaces with dashes(-) when entering orgs \n* If entering multiple values use the following format: "value-1 value-2 value-3"
            '''

userOrgs = []
client = snyk.SnykClient(os.getenv("SNYK_TOKEN"))
try:
    userOrgs = client.organizations.all()
except snyk.errors.SnykHTTPError as err:
    print("💥 Ran into an error while fetching account details, please check your API token")
    print( helpString)

def main(argv):
    inputOrgs = []
    products = []
    scaTypes = []
    
    #valid input arguments
    try:
        opts, args = getopt.getopt(argv, "ho:", ["help", "orgs=", "scatypes=", "products="] )
    except getopt.GetoptError:
        print(getopt.GetoptError)
        sys.exit(2)
    

    #process input
    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            print(helpString)
            sys.exit(2)
        if opt == '-o' or opt =='--orgs':
            if arg == "!":
                inputOrgs = [org.name for org in userOrgs]
            else:
                inputOrgs = arg.split()
        if opt == '--scatypes':
            scaTypes = [scaType.lower() for scaType in arg.split()]
        if opt == '--products':
            products =[product.lower() for product in arg.split()]
    
    if len(scaTypes) == 0 and len(products) == 0:
        print("No delete settings entered, exiting")
        print(helpString)
        sys.exit(2)
    
    if len(inputOrgs) == 0:
        print("No orgs to process entered, exiting")
        print(helpString)
    

    #delete functionality
    for currOrg in userOrgs:
        if currOrg.name in inputOrgs:
            inputOrgs.remove(currOrg.name)
            print("Processing" + """ \033[1;32m"{}" """.format(currOrg.name) + "\u001b[0morganization")
            for currProject in currOrg.projects.all():
                #if sca type matches user input
                if currProject.type in (scaTypes):
                    spinner = yaspin(text="Deleting\033[1;32m {}\u001b[0m since it is a \u001b[34m{}\u001b[0m project".format(currProject.name, currProject.type), color="yellow")
                    spinner.start()
                    try:
                        currProject.delete()
                        spinner.ok("✅ ")
                        spinner.stop()
                    except:
                        spinner.fail("💥 ")
                        spinner.stop()

                
                #if product matches user input
                if len(products):
                    productType = convertTypeToProduct(currProject.type)
                    spinner = yaspin(text="Deleting\033[1;32m {}\u001b[0m since it is a \u001b[34m{}\u001b[0m project".format(currProject.name, productType), color="yellow")

                    if productType in products:
                        spinner.start()
                        try:
                            currProject.delete()
                            spinner.ok("✅ ")
                            spinner.stop()
                        except exception as e:
                            spinner.fail("💥 ")
                            spinner.stop()
                        spinner.stop()
                    
        
     #process input orgs which didnt have a match
    if len(inputOrgs) != 0:
        print("\033[1;32m{}\u001b[0m are organizations which do not exist or you don't have access to them, please check your spelling and insure that spaces are replaced with dashes".format(inputOrgs))
                
       


                    
            
main(sys.argv[1:])


