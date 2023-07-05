def test_valid_pem(cert):
    '''The certificates will be checked for a valid pem structure.
       Loading of the pem file happens during parametrization of the test cases. 
       This test checks whether there has been an error during that phase. 
    '''
    if not cert.error is None: 
        raise cert.error
