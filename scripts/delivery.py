import os
import json
import sys
import pycountry

def add_country(db, **params):
    '''Add a country to a pycountry database for the duration of this session. 
       This is useful to patch testing countries into a list of countries.''' 
    if not db._is_loaded:
        db._load()
    # Create an instance of the virtual country
    obj = db.data_class(**params)
    # Add it to the database
    db.objects.append(obj)
    # Update the indices
    for key, value in params.items():
        value = value.lower()
        if key in db.no_index:
            continue
        index = db.indices.setdefault(key, {})
        index[value] = obj

if __name__=='__main__':  
    
    try:
        with open('scripts/countries.json', 'r') as file:
            doc = json.load(file)
        print("Successfully loaded countries.json.")
    except FileNotFoundError:
        print("Error: 'countries.json' file not found.", file=sys.stderr)
        sys.exit(1) 
    except json.JSONDecodeError:
        print("Error: 'countries.json' contains invalid JSON.", file=sys.stderr)
        sys.exit(1) 
    
    add_country(pycountry.countries, alpha_2='XA', alpha_3='XXA', common_name='Test XA', 
                                     flag='😄', name='Test XA', numeric='23233', official_name='Test Country XA' ) 
    add_country(pycountry.countries, alpha_2='XB', alpha_3='XXB', common_name='Test XA', 
                                     flag='😄', name='Test XXB', numeric='2929', official_name='Test Country XB' )
    add_country(pycountry.countries, alpha_2='XY', alpha_3='XXY', common_name='Test XY', 
                                     flag='😄', name='Test XY', numeric='9989', official_name='Test Country XY' )
    add_country(pycountry.countries, alpha_2='XX', alpha_3='XXX', common_name='Test XA', 
                                     flag='😄', name='Test XX', numeric='9990', official_name='Test Country XX' )
    add_country(pycountry.countries, alpha_2='XL', alpha_3='XCL', common_name='Test LAC (XL, XCL)',
                                     flag='😄', name='Test XL', numeric='9991', official_name='Test Country XL' )
    add_country(pycountry.countries, alpha_2='XO', alpha_3='XXO', common_name='Test XO',
                                     flag='😄', name='Test XO', numeric='9992', official_name='Test Country XO' )
    add_country(pycountry.countries, alpha_2='TS', alpha_3='TSI', common_name='Test TS',
                                     flag='😄', name='Test TS', numeric='9993', official_name='Test Country TS' )
    add_country(pycountry.countries, alpha_2='XM', alpha_3='XML', common_name='Test XM',
                                     flag='😄', name='Test XM', numeric='9994', official_name='Test Country XM' )
    add_country(pycountry.countries, alpha_2='XC', alpha_3='XXC', common_name='Test XC',
                                     flag='😄', name='Test XC', numeric='9995', official_name='Test Country XC' )
    add_country(pycountry.countries, alpha_2='JA', alpha_3='XJA', common_name='Test JA',
                                     flag='😄', name='Test JA', numeric='9996', official_name='Test Country JA' )
    add_country(pycountry.countries, alpha_2='XD', alpha_3='XXD', common_name='Test XD',
                                     flag='😄', name='Test XD', numeric='9997', official_name='Test Country XD' )
    add_country(pycountry.countries, alpha_2='XE', alpha_3='XXE', common_name='Test XE',
                                     flag='😄', name='Test XE', numeric='9998', official_name='Test Country XE' )
    add_country(pycountry.countries, alpha_2='XG', alpha_3='XXG', common_name='Test XG',
                                     flag='😄', name='Test XG', numeric='9999', official_name='Test Country XG' )
    add_country(pycountry.countries, alpha_2='XH', alpha_3='XXH', common_name='Test XH',
                                     flag='😄', name='Test XH', numeric='8880', official_name='Test Country XH' )
    add_country(pycountry.countries, alpha_2='XF', alpha_3='XXF', common_name='Test XF',
                                     flag='😄', name='Test XF', numeric='8881', official_name='Test Country XF' )
    add_country(pycountry.countries, alpha_2='XJ', alpha_3='XXJ', common_name='Test XJ',
                                     flag='😄', name='Test XJ', numeric='8882', official_name='Test Country XJ' )
    add_country(pycountry.countries, alpha_2='XK', alpha_3='XXK', common_name='Test XK',
                                     flag='😄', name='Test XK', numeric='8883', official_name='Test Country XK' )
    add_country(pycountry.countries, alpha_2='XI', alpha_3='XXI', common_name='Test XI',
                                     flag='😄', name='Test XI', numeric='8884', official_name='Test Country XI' )
    add_country(pycountry.countries, alpha_2='XQ', alpha_3='XXQ', common_name='Test XQ',
                                     flag='😄', name='Test XQ', numeric='8885', official_name='Test Country XQ' )
    add_country(pycountry.countries, alpha_2='XN', alpha_3='XXN', common_name='Test XN',
                                     flag='😄', name='Test XN', numeric='8886', official_name='Test Country XN' )
    add_country(pycountry.countries, alpha_2='XD', alpha_3='XXL', common_name='Test XD',
                                     flag='😄', name='Test XD', numeric='8887', official_name='Test Country XD' )
    add_country(pycountry.countries, alpha_2='XM', alpha_3='XXM', common_name='Test XM',
                                     flag='😄', name='Test XM', numeric='8888', official_name='Test Country XM' )
    add_country(pycountry.countries, alpha_2='XP', alpha_3='XXP', common_name='Test XP',
                                     flag='😄', name='Test XP', numeric='8889', official_name='Test Country XP' )
    add_country(pycountry.countries, alpha_2='XS', alpha_3='XXS', common_name='Test XS',
                                     flag='😄', name='Test XS', numeric='8890', official_name='Test Country XS' )
    add_country(pycountry.countries, alpha_2='XT', alpha_3='XXT', common_name='Test XT',
                                     flag='😄', name='Test XT', numeric='8891', official_name='Test Country XT' )
    add_country(pycountry.countries, alpha_2='XU', alpha_3='XXU', common_name='Test XU',
                                     flag='😄', name='Test XU', numeric='8892', official_name='Test Country XU' )
    add_country(pycountry.countries, alpha_2='XV', alpha_3='XXV', common_name='Test XV',
                                     flag='😄', name='Test XV', numeric='8893', official_name='Test Country XV' )
    add_country(pycountry.countries, alpha_2='XW', alpha_3='XXW', common_name='Test XW',
                                     flag='😄', name='Test XW', numeric='8894', official_name='Test Country XW' )
    countries = list(pycountry.countries)
  
   

    branches = os.popen("git ls-remote --heads").read()
    print ("branches found:")
    print(branches)

    for country in countries:        
        cCode = country.alpha_2
        if country.alpha_3 in doc:
            cCode= country.alpha_3
        if cCode in doc: 
            try:
                branchName = country.alpha_3+"/onboardingRequest"
                
                if not branchName in branches:
                    os.system("echo Try onboarding for " + country.alpha_3)
                    
                    ################## Prepare the internal structure
                    os.system("rm -rf repo")
                    os.system("rm -rf temp")
                    os.system("mkdir temp")
                    os.system("echo '"+country.alpha_3 + "\n' > temp/country")
                    os.system("echo '"+doc[cCode]+ "' > temp/base64")
                    if os.system("python scripts/config.py") !=0:
                        raise Exception("Configuration Error")
                    
                    tt_api_access = cCode + "_TT_API_ACCESS"
                    
                    if tt_api_access in doc:
                        os.system("touch TT_API_ACCESS")
                      
                    if os.path.exists("sync"):  
                    ###############  Transitive Trust
                        os.system("./scripts/transitiveTrust.sh "+country.alpha_2)
                        if os.system("python scripts/onboardingRequest.py ./transit/"+os.environ.get("ENV")+"/countries/"+country.alpha_2) != 0: 
                                raise Exception("Onboarding Request failed.")
                    else:
                        try:       
                            if os.system("python scripts/repo.py") != 0:
                                raise Exception("Repository Cloning failed.")
                            
                            os.system("./scripts/verify.sh 1> /dev/null")
                            
                            if os.system("python scripts/onboardingRequest.py repo") != 0:
                                raise Exception("Onboarding Request failed.")
                        except Exception as Error:
                            os.system("echo 'Error occoured for onboarding request " + country.alpha_3 +": "+str(Error)+"'") 
               
                    ######### Create PR 
                    os.system("./scripts/createPR.sh "+country.alpha_3)
                
                    os.system("git checkout main > /dev/null 2>&1")
                    os.system("git reset --hard && git clean -f -d > /dev/null 2>&1")
                else:
                    os.system("echo Skip "+country.alpha_3 + "Branch already exist merge the branch or delete the branch.")
            except Exception as Error:
                os.system("echo 'Error occoured for onboarding " + country.alpha_3 +": "+ str(Error)+"'")
